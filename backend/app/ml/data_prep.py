import os
import pandas as pd
import numpy as np
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent.parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

def clean_data():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    print("--- Starting Data Cleaning & Feature Engineering Pipeline ---")
    
    # 1. Load Raw Datasets
    print("Loading raw CSV files...")
    try:
        customers = pd.read_csv(RAW_DIR / "olist_customers_dataset.csv")
        products = pd.read_csv(RAW_DIR / "olist_products_dataset.csv")
        orders = pd.read_csv(RAW_DIR / "olist_orders_dataset.csv")
        order_items = pd.read_csv(RAW_DIR / "olist_order_items_dataset.csv")
        payments = pd.read_csv(RAW_DIR / "olist_order_payments_dataset.csv")
        translation = pd.read_csv(RAW_DIR / "product_category_name_translation.csv")
    except Exception as e:
        print(f"Error loading raw CSVs: {e}")
        return

    # 2. Clean Customers
    print("Cleaning customers...")
    # Keep: customer_id, customer_city, customer_state
    cleaned_customers = customers[["customer_id", "customer_city", "customer_state"]].copy()
    
    # 3. Clean Products
    print("Cleaning products...")
    # Translate product_category_name to English using translation file
    # product_category_name_translation has: product_category_name, product_category_name_english
    products_translated = products.merge(translation, on="product_category_name", how="left")
    # Replace NaN category names and translations with 'unknown'
    products_translated["product_category_name_english"] = products_translated["product_category_name_english"].fillna("unknown")
    
    cleaned_products = pd.DataFrame({
        "product_id": products_translated["product_id"],
        "product_category": products_translated["product_category_name_english"]
    })

    # 4. Clean Orders
    print("Cleaning orders...")
    # Convert dates to datetime
    orders["order_purchase_timestamp"] = pd.to_datetime(orders["order_purchase_timestamp"])
    orders["order_delivered_customer_date"] = pd.to_datetime(orders["order_delivered_customer_date"])
    
    # Rename columns to match PostgreSQL
    cleaned_orders = pd.DataFrame({
        "order_id": orders["order_id"],
        "customer_id": orders["customer_id"],
        "order_status": orders["order_status"],
        "order_purchase_timestamp": orders["order_purchase_timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S"),
        "order_delivered_timestamp": orders["order_delivered_customer_date"].dt.strftime("%Y-%m-%d %H:%M:%S")
    })
    
    # 5. Clean Order Items (Aggregate Duplicates)
    print("Cleaning and deduplicating order items...")
    # group by order_id, product_id and sum price and freight_value to satisfy PostgreSQL unique primary key (order_id, product_id)
    cleaned_order_items = order_items.groupby(["order_id", "product_id"], as_index=False).agg({
        "price": "sum",
        "freight_value": "sum"
    })

    # 6. Clean Payments
    print("Cleaning payments...")
    cleaned_payments = payments[["order_id", "payment_type", "payment_value"]].copy()

    # Save Cleaned CSVs matching Database Schema
    print("Saving cleaned files for DB ingestion...")
    cleaned_customers.to_csv(PROCESSED_DIR / "cleaned_customers.csv", index=False)
    cleaned_products.to_csv(PROCESSED_DIR / "cleaned_products.csv", index=False)
    cleaned_orders.to_csv(PROCESSED_DIR / "cleaned_orders.csv", index=False)
    cleaned_order_items.to_csv(PROCESSED_DIR / "cleaned_order_items.csv", index=False)
    cleaned_payments.to_csv(PROCESSED_DIR / "cleaned_payments.csv", index=False)

    print("DB files saved successfully.")

    # 7. Generate Daily Sales Feature for Forecasting
    print("Generating daily sales features for forecasting...")
    # Join orders and order items to get prices and timestamps
    # Filter for non-canceled, non-unavailable orders
    valid_orders = orders[~orders["order_status"].isin(["canceled", "unavailable"])].copy()
    sales_merged = valid_orders.merge(order_items, on="order_id", how="inner")
    
    # Filter for the stable timeline: 2017-01-01 to 2018-08-31
    sales_merged = sales_merged[
        (sales_merged["order_purchase_timestamp"] >= "2017-01-01") & 
        (sales_merged["order_purchase_timestamp"] <= "2018-08-31")
    ]
    
    # Extract date and group by day
    sales_merged["date"] = sales_merged["order_purchase_timestamp"].dt.date
    daily_sales = sales_merged.groupby("date")["price"].sum().reset_index()
    daily_sales.columns = ["ds", "y"]
    
    # Save daily_sales
    daily_sales.to_csv(PROCESSED_DIR / "daily_sales.csv", index=False)
    print(f"Daily sales features saved. Shape: {daily_sales.shape}")

    # 8. Generate RFM Features for Customer Segmentation
    print("Generating RFM features for customer segmentation...")
    # We need to map order items price or payments value to customer_unique_id
    # Link order_items and orders, then customers
    # Group by customer_unique_id
    
    # Calculate recency, frequency, monetary
    # 1. Monetory and Frequency: from orders
    # Filter valid orders
    orders_valid = orders[~orders["order_status"].isin(["canceled", "unavailable"])].copy()
    
    # Merge order items prices to get total order value
    order_values = order_items.groupby("order_id")["price"].sum().reset_index()
    orders_with_value = orders_valid.merge(order_values, on="order_id", how="inner")
    
    # Merge customers to get customer_unique_id
    customers_mapped = orders_with_value.merge(customers, on="customer_id", how="inner")
    
    # Compute max purchase timestamp in dataset to act as baseline date
    baseline_date = orders_valid["order_purchase_timestamp"].max() + pd.Timedelta(days=1)
    print(f"RFM Baseline date (max date + 1 day): {baseline_date}")
    
    # RFM Aggregations per customer_unique_id
    rfm = customers_mapped.groupby("customer_unique_id").agg({
        "order_purchase_timestamp": lambda x: (baseline_date - x.max()).days, # Recency
        "order_id": "nunique",                                               # Frequency
        "price": "sum"                                                       # Monetary
    }).reset_index()
    
    rfm.columns = ["customer_unique_id", "recency", "frequency", "monetary"]
    
    # Now, we also want to keep the mapping of customer_id to customer_unique_id 
    # to output a row-by-row customer_id segmentation mapping.
    # So we will output rfm_data.csv containing this basic table, and we'll save customer mapping separately or inside it.
    # To keep features clean, let's output rfm_data.csv containing the customer_unique_id RFM table.
    rfm.to_csv(PROCESSED_DIR / "rfm_data.csv", index=False)
    
    # Also save a mapping of customer_id -> customer_unique_id so the training script can export results by customer_id
    cust_map = customers[["customer_id", "customer_unique_id"]].copy()
    cust_map.to_csv(PROCESSED_DIR / "customer_id_map.csv", index=False)
    
    print(f"RFM feature data saved. Unique customers: {rfm.shape[0]}")
    print("--- Data Prep Pipeline Completed Successfully ---")

if __name__ == "__main__":
    clean_data()

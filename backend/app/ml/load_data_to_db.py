import os
import sys
from pathlib import Path
import pandas as pd
from sqlalchemy import text

# Setup paths to ensure we can import 'app' and locate the data
BASE_DIR = Path(__file__).parent.parent.parent.parent
BACKEND_DIR = BASE_DIR / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

try:
    from app.database import engine, DATABASE_URL
except ImportError as e:
    print(f"Error importing database configuration: {e}")
    sys.exit(1)


def safe_str(e):
    try:
        return str(e)
    except Exception:
        try:
            return repr(e)
        except Exception:
            return "Unknown database error (could not decode error message)"


def load_data():
    print("--- Starting Data Load to PostgreSQL ---")
    
    # 1. Verify connection
    print(f"Connecting to database using DATABASE_URL configuration...")
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Successfully connected to the database.")
    except Exception as e:
        print(f"\n[ERROR] Connection failed: {safe_str(e)}")
        print("\nPlease check that:")
        print("1. Your PostgreSQL server is running locally.")
        print("2. The database 'smartcommerce' exists.")
        print(f"3. The connection URL matches your setup (configured: {DATABASE_URL}).")
        sys.exit(1)
        
    # 2. Run database/init.sql
    init_sql_path = BASE_DIR / "database" / "init.sql"
    print(f"\nReading initialization schema from {init_sql_path}...")
    if not init_sql_path.exists():
        print(f"[ERROR] init.sql not found at {init_sql_path}")
        sys.exit(1)
        
    try:
        with open(init_sql_path, "r", encoding="utf-8") as f:
            sql_commands = f.read()
        
        with engine.connect() as conn:
            raw_conn = conn.connection
            with raw_conn.cursor() as cur:
                cur.execute(sql_commands)
            raw_conn.commit()
        print("Database tables initialized successfully (created if they did not exist).")
    except Exception as e:
        print(f"[ERROR] Failed running init.sql: {safe_str(e)}")
        sys.exit(1)
        
    # 3. Truncate tables to safely re-run the script
    print("\nTruncating existing data to prevent primary key or foreign key duplicates...")
    try:
        with engine.begin() as conn:
            conn.execute(text("TRUNCATE TABLE payments, order_items, orders, customers, products CASCADE;"))
        print("Existing data truncated successfully.")
    except Exception as e:
        print(f"[ERROR] Failed truncating tables: {safe_str(e)}")
        sys.exit(1)

    # 4. Load CSVs and insert in respect of FK order
    data_dir = BASE_DIR / "data" / "processed"
    
    # Define files and tables in correct insertion order
    # (customers and products first, then orders, then order_items and payments)
    datasets = [
        {"file": "cleaned_customers.csv", "table": "customers", "parse_dates": []},
        {"file": "cleaned_products.csv", "table": "products", "parse_dates": []},
        {"file": "cleaned_orders.csv", "table": "orders", "parse_dates": ["order_purchase_timestamp", "order_delivered_timestamp"]},
        {"file": "cleaned_order_items.csv", "table": "order_items", "parse_dates": []},
        {"file": "cleaned_payments.csv", "table": "payments", "parse_dates": []}
    ]
    
    print("\nStarting data insertion from processed CSVs...")
    for dataset in datasets:
        csv_path = data_dir / dataset["file"]
        table_name = dataset["table"]
        
        print(f"\nProcessing {dataset['file']}...")
        if not csv_path.exists():
            print(f"[ERROR] Processed CSV file not found at {csv_path}")
            sys.exit(1)
            
        try:
            # Read CSV
            df = pd.read_csv(csv_path)
            
            # Convert date columns to proper datetime objects for SQLAlchemy
            for col in dataset["parse_dates"]:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
            
            print(f"Inserting {len(df)} rows into table '{table_name}'...")
            # Insert to DB using pandas to_sql
            df.to_sql(
                name=table_name,
                con=engine,
                if_exists="append",
                index=False,
                chunksize=10000
            )
            print(f"Successfully loaded table '{table_name}'.")
            
        except Exception as e:
            print(f"[ERROR] Failed loading table '{table_name}' from {dataset['file']}: {safe_str(e)}")
            sys.exit(1)
            
    # 5. Verify row counts by querying the DB
    print("\n--- Verification: Row Counts in Database ---")
    try:
        with engine.connect() as conn:
            for dataset in datasets:
                table_name = dataset["table"]
                res = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                count = res.scalar()
                print(f"Table '{table_name}': {count} rows")
        print("\nAll data loaded and verified successfully!")
    except Exception as e:
        print(f"[ERROR] Verification failed: {safe_str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    load_data()

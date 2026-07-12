from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Order, OrderItem, Product

router = APIRouter()


@router.get("/summary")
def get_kpis_summary(db: Session = Depends(get_db)):
    """
    Retourne les KPIs principaux du dashboard :
    chiffre d'affaires, nombre de commandes, nombre de clients, top produits.
    """
    # 1. Revenue: sum of price across all order_items for non-canceled orders
    revenue_val = db.query(func.sum(OrderItem.price))\
                    .join(Order, OrderItem.order_id == Order.order_id)\
                    .filter(Order.order_status != "canceled")\
                    .scalar()
    revenue = round(float(revenue_val), 2) if revenue_val is not None else 0.0

    # 2. Orders count: count of distinct non-canceled orders
    orders_count = db.query(Order.order_id)\
                     .filter(Order.order_status != "canceled")\
                     .count()

    # 3. Customers count: count of distinct customers who have placed a non-canceled order
    customers_count = db.query(func.count(Order.customer_id.distinct()))\
                        .filter(Order.order_status != "canceled")\
                        .scalar() or 0

    # 4. Top products: top 5 products by total revenue
    top_products_query = db.query(
        OrderItem.product_id,
        Product.product_category,
        func.sum(OrderItem.price).label("revenue")
    ).join(
        Order, OrderItem.order_id == Order.order_id
    ).outerjoin(
        Product, OrderItem.product_id == Product.product_id
    ).filter(
        Order.order_status != "canceled"
    ).group_by(
        OrderItem.product_id,
        Product.product_category
    ).order_by(
        func.sum(OrderItem.price).desc()
    ).limit(5).all()

    top_products = [
        {
            "product_id": row.product_id,
            "product_category": row.product_category if row.product_category else "unknown",
            "revenue": round(float(row.revenue), 2) if row.revenue is not None else 0.0
        }
        for row in top_products_query
    ]

    return {
        "revenue": revenue,
        "orders_count": orders_count,
        "customers_count": customers_count,
        "top_products": top_products,
    }


@router.get("/sales-evolution")
def get_sales_evolution(db: Session = Depends(get_db)):
    """
    Retourne l'évolution des ventes dans le temps (pour le graphique du dashboard).
    """
    sales_query = db.query(
        func.date(Order.order_purchase_timestamp).label("date"),
        func.sum(OrderItem.price).label("revenue")
    ).join(
        OrderItem, OrderItem.order_id == Order.order_id
    ).filter(
        Order.order_status != "canceled"
    ).group_by(
        func.date(Order.order_purchase_timestamp)
    ).order_by(
        func.date(Order.order_purchase_timestamp)
    ).all()

    sales_evolution = [
        {
            "date": row.date.isoformat() if hasattr(row.date, "isoformat") else str(row.date),
            "revenue": round(float(row.revenue), 2) if row.revenue is not None else 0.0
        }
        for row in sales_query if row.date is not None
    ]

    return {"data": sales_evolution}


from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

router = APIRouter()


@router.get("")
@router.get("/")
def get_kpis(db: Session = Depends(get_db)):
    """
    Retourne les KPIs généraux pour le dashboard.
    """
    return {
        "revenue": 0,
        "orders_count": 0,
        "avg_order_value": 0,
        "sales_over_time": [{"date": "2024-01-01", "revenue": 0}],
        "top_products": [{"name": "", "revenue": 0, "units_sold": 0}]
    }


@router.get("/summary")
def get_kpis_summary(db: Session = Depends(get_db)):
    """
    Retourne les KPIs principaux du dashboard :
    chiffre d'affaires, nombre de commandes, nombre de clients, top produits.
    TODO: remplacer par de vraies requêtes SQL sur les tables orders/order_items/customers.
    """
    return {
        "revenue": 0,
        "orders_count": 0,
        "customers_count": 0,
        "top_products": [],
    }


@router.get("/sales-evolution")
def get_sales_evolution(db: Session = Depends(get_db)):
    """
    Retourne l'évolution des ventes dans le temps (pour le graphique du dashboard).
    TODO: agrégation SQL par jour/semaine/mois.
    """
    return {"data": []}


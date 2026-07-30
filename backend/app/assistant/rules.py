"""
Moteur de règles pour l'assistant décisionnel léger.
Chaque question prédéfinie est associée à une fonction qui :
1. interroge les données (SQL / résultats ML déjà calculés)
2. applique une règle métier simple
3. remplit un template de réponse (voir templates.py)
"""
import pandas as pd
from pathlib import Path
from datetime import timedelta
from sqlalchemy import func
from app.models import Order, OrderItem, Product
from app.ml.anomaly_detector import detect_anomalies_rolling
from app.assistant.templates import (
    SALES_DROP_TEMPLATE,
    SALES_STABLE_TEMPLATE,
    STOCK_RISK_TEMPLATE,
    AT_RISK_CUSTOMERS_TEMPLATE,
)

BASE_DIR = Path(__file__).parent.parent.parent.parent
SALES_PATH = BASE_DIR / "data" / "processed" / "daily_sales.csv"
SEGMENTS_PATH = BASE_DIR / "data" / "processed" / "customer_segments.csv"


def why_sales_dropped(db):
    """
    Détermine si une baisse récente a eu lieu et identifie la catégorie de produit
    ayant le plus contribué à cette baisse de chiffre d'affaires.
    """
    if not SALES_PATH.exists():
        raise FileNotFoundError(f"Fichier des ventes journalières introuvable à : {SALES_PATH}")

    # 1. Charger et préparer la série temporelle
    df = pd.read_csv(SALES_PATH)
    df["ds"] = pd.to_datetime(df["ds"])
    df["y"] = pd.to_numeric(df["y"])
    series = df.set_index("ds")["y"].sort_index()

    # 2. Détecter les anomalies glissantes (seuil = 2.0, 30 derniers jours vs 90 jours de référence)
    anomalies_df = detect_anomalies_rolling(
        series, 
        threshold=2.0, 
        window_size=30, 
        baseline_size=90
    )

    # Filtrer uniquement les baisses de vente (déviation négative)
    drops = anomalies_df[anomalies_df["deviation_pct"] < 0]

    if drops.empty:
        return SALES_STABLE_TEMPLATE

    # 3. Analyser la baisse la plus récente
    drops_sorted = drops.sort_values(by="date", ascending=False)
    target_anomaly = drops_sorted.iloc[0]
    anomalous_date_str = target_anomaly["date"]
    anomalous_date = pd.to_datetime(anomalous_date_str).date()

    # Définir les fenêtres temporelles de référence et de l'anomalie
    baseline_start = anomalous_date - timedelta(days=90)
    baseline_end = anomalous_date - timedelta(days=1)

    baseline_start_dt = pd.to_datetime(baseline_start)
    baseline_end_dt = pd.to_datetime(baseline_end) + timedelta(hours=23, minutes=59, seconds=59)

    anomaly_start_dt = pd.to_datetime(anomalous_date)
    anomaly_end_dt = pd.to_datetime(anomalous_date) + timedelta(hours=23, minutes=59, seconds=59)

    # 4. Requêter le CA moyen quotidien par catégorie lors de la période de référence
    baseline_query = db.query(
        Product.product_category,
        func.sum(OrderItem.price).label("revenue")
    ).outerjoin(
        Product, OrderItem.product_id == Product.product_id
    ).join(
        Order, OrderItem.order_id == Order.order_id
    ).filter(
        Order.order_status != "canceled",
        Order.order_purchase_timestamp >= baseline_start_dt,
        Order.order_purchase_timestamp <= baseline_end_dt
    ).group_by(
        Product.product_category
    ).all()

    baseline_daily_avg = {
        (row.product_category or "inconnue"): float(row.revenue or 0.0) / 90.0
        for row in baseline_query
    }

    # 5. Requêter le CA par catégorie sur la journée d'anomalie
    anomalous_query = db.query(
        Product.product_category,
        func.sum(OrderItem.price).label("revenue")
    ).outerjoin(
        Product, OrderItem.product_id == Product.product_id
    ).join(
        Order, OrderItem.order_id == Order.order_id
    ).filter(
        Order.order_status != "canceled",
        Order.order_purchase_timestamp >= anomaly_start_dt,
        Order.order_purchase_timestamp <= anomaly_end_dt
    ).group_by(
        Product.product_category
    ).all()

    anomalous_revenues = {
        (row.product_category or "inconnue"): float(row.revenue or 0.0)
        for row in anomalous_query
    }

    # 6. Calculer la baisse absolue de CA par catégorie pour identifier la principale baisse
    decreases = {}
    for category, base_avg in baseline_daily_avg.items():
        anom_rev = anomalous_revenues.get(category, 0.0)
        decrease = base_avg - anom_rev
        decreases[category] = (decrease, base_avg)

    if not decreases:
        return SALES_STABLE_TEMPLATE

    # Trouver la catégorie avec la baisse la plus importante
    top_decrease_category = None
    max_decrease = -float("inf")
    for category, (dec, base_avg) in decreases.items():
        if dec > max_decrease:
            max_decrease = dec
            top_decrease_category = category

    if top_decrease_category is None or max_decrease <= 0:
        return SALES_STABLE_TEMPLATE

    # Calculer le pourcentage de baisse pour cette catégorie par rapport à sa propre moyenne
    base_avg_cat = baseline_daily_avg[top_decrease_category]
    drop_pct = (max_decrease / base_avg_cat) * 100

    return SALES_DROP_TEMPLATE.format(
        category=top_decrease_category,
        drop_pct=round(drop_pct, 1)
    )


def stock_risk(db):
    """
    Identifie les produits à forte demande (top 50) dans les 30 derniers jours
    dont le rythme de vente s'accélère par rapport aux 30 jours précédents.
    Il s'agit d'une heuristique de vélocité de ventes (proxy de risque de stock).
    """
    max_date = db.query(func.max(Order.order_purchase_timestamp))\
                 .join(OrderItem, OrderItem.order_id == Order.order_id)\
                 .filter(Order.order_status != "canceled")\
                 .scalar()
    if not max_date:
        return "Aucune donnée de commande disponible pour évaluer le risque de stock."

    recent_start = max_date - timedelta(days=30)
    prev_start = max_date - timedelta(days=60)

    # 1. Identifier le Top 50 des produits vendus récemment (30 derniers jours)
    recent_sales = db.query(
        OrderItem.product_id,
        Product.product_category,
        func.count(OrderItem.order_id).label("count")
    ).outerjoin(
        Product, OrderItem.product_id == Product.product_id
    ).join(
        Order, OrderItem.order_id == Order.order_id
    ).filter(
        Order.order_status != "canceled",
        Order.order_purchase_timestamp >= recent_start
    ).group_by(
        OrderItem.product_id,
        Product.product_category
    ).order_by(
        func.count(OrderItem.order_id).desc()
    ).limit(50).all()

    if not recent_sales:
        return "Aucune vente récente détectée sur les 30 derniers jours pour analyser le risque."

    top_product_ids = [row.product_id for row in recent_sales]

    # 2. Requêter les volumes de vente de ces mêmes produits sur les 30 jours précédents
    prev_sales_query = db.query(
        OrderItem.product_id,
        func.count(OrderItem.order_id).label("count")
    ).join(
        Order, OrderItem.order_id == Order.order_id
    ).filter(
        Order.order_status != "canceled",
        Order.order_purchase_timestamp >= prev_start,
        Order.order_purchase_timestamp < recent_start,
        OrderItem.product_id.in_(top_product_ids)
    ).group_by(
        OrderItem.product_id
    ).all()

    prev_counts = {row.product_id: row.count for row in prev_sales_query}

    # 3. Filtrer les produits présentant une accélération de demande (recent_count > prev_count)
    at_risk_products = []
    for row in recent_sales:
        pid = row.product_id
        cat = row.product_category or "inconnue"
        recent_c = row.count
        prev_c = prev_counts.get(pid, 0)

        if recent_c > prev_c:
            at_risk_products.append({
                "product_id": pid,
                "category": cat,
                "recent_count": recent_c,
                "prev_count": prev_c
            })

    count_at_risk = len(at_risk_products)
    if count_at_risk == 0:
        return (
            "Aucun produit à forte demande ne présente d'accélération de ventes "
            "particulière sur les 30 derniers jours (les stocks semblent stables)."
        )

    # Le produit prioritaire est celui avec les ventes récentes les plus élevées parmi ceux qui accélèrent
    top_p = at_risk_products[0]
    top_product_str = f"{top_p['product_id']} (catégorie : {top_p['category']})"

    return STOCK_RISK_TEMPLATE.format(
        count=count_at_risk,
        top_product=top_product_str
    )


def at_risk_customers(db=None):
    """
    Retourne le nombre de clients dans le segment "À risque" (Module Segmentation).
    """
    if not SEGMENTS_PATH.exists():
        raise FileNotFoundError(f"Fichier de segmentation clients introuvable à : {SEGMENTS_PATH}")

    df = pd.read_csv(SEGMENTS_PATH, usecols=["segment_label"])
    count = int((df["segment_label"] == "À risque").sum())

    return AT_RISK_CUSTOMERS_TEMPLATE.format(count=count)


RULES = {
    "why_sales_dropped": why_sales_dropped,
    "stock_risk": stock_risk,
    "at_risk_customers": at_risk_customers,
}

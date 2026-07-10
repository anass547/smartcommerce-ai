"""
Moteur de règles pour l'assistant décisionnel léger.
Chaque question prédéfinie est associée à une fonction qui :
1. interroge les données (SQL / résultats ML déjà calculés)
2. applique une règle métier simple
3. remplit un template de réponse (voir templates.py)
"""


def why_sales_dropped():
    # TODO: comparer les ventes de la période courante à la moyenne historique,
    # identifier la catégorie la plus impactée.
    raise NotImplementedError


def stock_risk():
    # TODO: identifier les produits dont (stock / vitesse de vente) < seuil.
    raise NotImplementedError


def at_risk_customers():
    # TODO: retourner les clients du segment "À risque" (issus du module segmentation).
    raise NotImplementedError


RULES = {
    "why_sales_dropped": why_sales_dropped,
    "stock_risk": stock_risk,
    "at_risk_customers": at_risk_customers,
}

"""
Templates de réponses en langage naturel pour l'assistant décisionnel léger.
"""

SALES_DROP_TEMPLATE = (
    "Les ventes diminuent principalement à cause d'une baisse des commandes "
    "dans la catégorie {category} ({drop_pct}% par rapport à la moyenne). "
    "Une promotion ciblée est recommandée."
)

STOCK_RISK_TEMPLATE = (
    "{count} produits risquent une rupture de stock dans les prochains jours, "
    "dont {top_product} en priorité."
)

AT_RISK_CUSTOMERS_TEMPLATE = (
    "{count} clients présentent un risque de désengagement (segment \"À risque\"). "
    "Une campagne de réactivation est recommandée."
)

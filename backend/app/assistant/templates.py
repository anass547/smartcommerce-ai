"""
Templates de réponses en langage naturel pour l'assistant décisionnel léger.
"""

SALES_DROP_TEMPLATE = (
    "Les ventes diminuent principalement à cause d'une baisse des commandes "
    "dans la catégorie {category} ({drop_pct}% par rapport à la moyenne). "
    "Une promotion ciblée est recommandée."
)

SALES_STABLE_TEMPLATE = (
    "Les ventes sont stables récemment. Aucune baisse de chiffre d'affaires "
    "significative n'a été détectée dans l'historique de ventes récent."
)

STOCK_RISK_TEMPLATE = (
    "{count} produits risquent une rupture de stock dans les prochains jours (estimation basée sur une accélération "
    "de la demande sur les 30 derniers jours), dont le produit {top_product} en priorité. "
    "Attention : il s'agit d'une estimation basée sur la vélocité des ventes et non sur un inventaire réel."
)

AT_RISK_CUSTOMERS_TEMPLATE = (
    "{count} clients présentent un risque de désengagement (segment \"À risque\"). "
    "Une campagne de réactivation est recommandée."
)

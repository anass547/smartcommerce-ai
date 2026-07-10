from fastapi import APIRouter, Query

router = APIRouter()


@router.get("/sales")
def predict_sales(horizon: str = Query("week", enum=["day", "week", "month"])):
    """
    Retourne la prévision des ventes pour l'horizon demandé (jour/semaine/mois).
    TODO: charger le modèle Prophet entraîné (app/ml/saved_models/) et générer la prédiction.
    """
    return {"horizon": horizon, "predictions": []}

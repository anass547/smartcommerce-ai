from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_anomalies():
    """
    Retourne les anomalies détectées récemment (baisses/pics inhabituels).
    TODO: appeler app.ml.anomaly_detector pour calculer les écarts (z-score)
    et générer des messages du type "Les ventes ont chuté de 35%...".
    """
    return {"anomalies": []}

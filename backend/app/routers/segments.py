from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_customer_segments():
    """
    Retourne la répartition des clients par segment RFM :
    VIP / Fidèles / Occasionnels / À risque.
    TODO: charger le modèle K-Means entraîné et les scores RFM précalculés.
    """
    return {
        "segments": [
            {"name": "VIP", "count": 0},
            {"name": "Fidèles", "count": 0},
            {"name": "Occasionnels", "count": 0},
            {"name": "À risque", "count": 0},
        ]
    }

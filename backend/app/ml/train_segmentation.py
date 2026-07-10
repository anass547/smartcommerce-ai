"""
Script offline de segmentation client (RFM + K-Means).
À exécuter séparément :

    python -m app.ml.train_segmentation

Sauvegarde le modèle entraîné dans app/ml/saved_models/segmentation_model.pkl
"""
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pickle
from pathlib import Path

SAVED_MODELS_DIR = Path(__file__).parent / "saved_models"


def compute_rfm(orders_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcule les scores Recency, Frequency, Monetary par client.
    TODO: implémenter à partir des données orders/order_items.
    """
    raise NotImplementedError


def train():
    orders_df = None  # TODO: charger depuis data/processed/
    rfm = compute_rfm(orders_df)

    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm[["recency", "frequency", "monetary"]])

    kmeans = KMeans(n_clusters=4, random_state=42)
    rfm["cluster"] = kmeans.fit_predict(rfm_scaled)

    SAVED_MODELS_DIR.mkdir(exist_ok=True)
    with open(SAVED_MODELS_DIR / "segmentation_model.pkl", "wb") as f:
        pickle.dump({"kmeans": kmeans, "scaler": scaler}, f)

    print("Modèle de segmentation entraîné et sauvegardé.")


if __name__ == "__main__":
    train()

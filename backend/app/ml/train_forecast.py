"""
Script offline d'entraînement du modèle de prévision des ventes (Prophet).
À exécuter séparément (pas au runtime de l'API) :

    python -m app.ml.train_forecast

Sauvegarde le modèle entraîné dans app/ml/saved_models/forecast_model.pkl
"""
import pandas as pd
from prophet import Prophet
import pickle
from pathlib import Path

SAVED_MODELS_DIR = Path(__file__).parent / "saved_models"


def load_sales_data() -> pd.DataFrame:
    # TODO: charger depuis data/processed/ (ex: ventes agrégées par jour)
    # Format attendu par Prophet : colonnes "ds" (date) et "y" (valeur)
    raise NotImplementedError


def train():
    df = load_sales_data()
    model = Prophet()
    model.fit(df)

    SAVED_MODELS_DIR.mkdir(exist_ok=True)
    with open(SAVED_MODELS_DIR / "forecast_model.pkl", "wb") as f:
        pickle.dump(model, f)

    print("Modèle Prophet entraîné et sauvegardé.")


if __name__ == "__main__":
    train()

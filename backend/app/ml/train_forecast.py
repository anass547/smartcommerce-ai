"""
Script offline d'entraînement du modèle de prévision des ventes (XGBRegressor).
À exécuter séparément (pas au runtime de l'API) :

    python -m app.ml.train_forecast

Sauvegarde le modèle entraîné dans app/ml/saved_models/forecast_model.pkl
"""
import pandas as pd
import pickle
from pathlib import Path
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error

BASE_DIR = Path(__file__).parent.parent.parent.parent
SAVED_MODELS_DIR = Path(__file__).parent / "saved_models"


def load_sales_data() -> pd.DataFrame:
    """
    Loads daily sales aggregated data from data/processed/daily_sales.csv.
    Format expected: 'ds' (date) and 'y' (daily revenue).
    """
    csv_path = BASE_DIR / "data" / "processed" / "daily_sales.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"Processed daily sales file not found at: {csv_path}. Please run data_prep first.")
    
    df = pd.read_csv(csv_path)
    df["ds"] = pd.to_datetime(df["ds"])
    df["y"] = pd.to_numeric(df["y"])
    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Engineers features for sales forecasting:
    - Time features: day_of_week, day_of_month, month
    - Lag features: lag_1, lag_7, rolling_mean_7 (7-day rolling average of previous sales)
    """
    df = df.copy()
    df = df.sort_values("ds").reset_index(drop=True)
    
    # 1. Time-based features
    df["day_of_week"] = df["ds"].dt.dayofweek
    df["day_of_month"] = df["ds"].dt.day
    df["month"] = df["ds"].dt.month
    
    # 2. Lag features
    df["lag_1"] = df["y"].shift(1)
    df["lag_7"] = df["y"].shift(7)
    
    # 3. Rolling window feature: 7-day rolling average of *previous* sales (excluding current day)
    df["rolling_mean_7"] = df["y"].shift(1).rolling(window=7).mean()
    
    return df


def train():
    print("Loading daily sales data...")
    df_original = load_sales_data()
    print(f"Data loaded. Shape: {df_original.shape}. Date range: {df_original['ds'].min()} to {df_original['ds'].max()}")
    
    print("Engineering features...")
    df_features = engineer_features(df_original)
    
    # Keep track of which features we are using
    feature_cols = ["day_of_week", "day_of_month", "month", "lag_1", "lag_7", "rolling_mean_7"]
    
    # Drop rows with NaN created by lag/rolling calculations
    df_clean = df_features.dropna(subset=feature_cols).copy()
    print(f"Cleaned data shape after removing NaNs: {df_clean.shape}")
    
    X = df_clean[feature_cols]
    y = df_clean["y"]
    
    # Split chronologically (no shuffling) into train/test, roughly 85/15
    split_idx = int(len(df_clean) * 0.85)
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
    
    print(f"Train size: {len(X_train)}, Test size: {len(X_test)}")
    
    print("Training XGBRegressor...")
    model = XGBRegressor(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.05,
        reg_lambda=150.0,
        random_state=42
    )
    model.fit(X_train, y_train)
    
    # Evaluate with MAE on both train and test sets
    train_preds = model.predict(X_train)
    test_preds = model.predict(X_test)
    train_mae = mean_absolute_error(y_train, train_preds)
    test_mae = mean_absolute_error(y_test, test_preds)
    print(f"Train Mean Absolute Error (MAE): {train_mae:.2f}")
    print(f"Test Mean Absolute Error (MAE): {test_mae:.2f}")
    
    # Save model bundle
    SAVED_MODELS_DIR.mkdir(exist_ok=True, parents=True)
    model_path = SAVED_MODELS_DIR / "forecast_model.pkl"
    
    # We save the last 14 rows of the original sales data to bootstrap lag calculations at inference time
    historical_data = df_original[["ds", "y"]].tail(14).copy()
    
    bundle = {
        "model": model,
        "features": feature_cols,
        "historical_data": historical_data
    }
    
    with open(model_path, "wb") as f:
        pickle.dump(bundle, f)
        
    print(f"Model successfully saved to {model_path}.")


if __name__ == "__main__":
    train()

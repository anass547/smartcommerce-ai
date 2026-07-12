import pickle
import pandas as pd
from pathlib import Path
from fastapi import APIRouter, Query, HTTPException

router = APIRouter()

# Locate the saved model bundle
CURRENT_DIR = Path(__file__).parent
MODEL_PATH = CURRENT_DIR.parent / "ml" / "saved_models" / "forecast_model.pkl"


@router.get("/sales")
def predict_sales(horizon: str = Query("week", enum=["day", "week", "month"])):
    """
    Retourne la prévision des ventes pour l'horizon demandé (jour/semaine/mois).
    Génère des prédictions récursives basées sur le modèle RandomForestRegressor.
    """
    if not MODEL_PATH.exists():
        raise HTTPException(
            status_code=500, 
            detail="Forecast model is not trained yet. Please run training first."
        )
    
    # Load the saved model bundle
    try:
        with open(MODEL_PATH, "rb") as f:
            bundle = pickle.load(f)
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to load forecast model: {str(e)}"
        )
        
    model = bundle["model"]
    feature_names = bundle["features"]
    history = bundle["historical_data"].copy()
    
    # Map horizon to forecast days
    horizon_days = {
        "day": 1,
        "week": 7,
        "month": 30
    }
    num_days = horizon_days[horizon]
    
    # Ensure history datatypes are set correctly for date and sales columns
    history["ds"] = pd.to_datetime(history["ds"])
    history["y"] = pd.to_numeric(history["y"])
    history = history.sort_values("ds").reset_index(drop=True)
    
    predictions = []
    
    # Generate predictions recursively, one day at a time
    for _ in range(num_days):
        # 1. Compute next date
        next_date = history["ds"].max() + pd.Timedelta(days=1)
        
        # 2. Extract date components as features
        day_of_week = next_date.dayofweek
        day_of_month = next_date.day
        month = next_date.month
        
        # 3. Extract lag features from the updated history (real + predicted)
        if len(history) < 7:
            raise HTTPException(
                status_code=500, 
                detail="Insufficient history data to compute lag features."
            )
            
        lag_1 = history["y"].iloc[-1]
        lag_7 = history["y"].iloc[-7]
        rolling_mean_7 = history["y"].iloc[-7:].mean()
        
        # 4. Construct feature dictionary matching the model columns
        feature_values = {
            "day_of_week": [day_of_week],
            "day_of_month": [day_of_month],
            "month": [month],
            "lag_1": [lag_1],
            "lag_7": [lag_7],
            "rolling_mean_7": [rolling_mean_7]
        }
        
        X_pred = pd.DataFrame(feature_values)[feature_names]
        
        # 5. Predict using the RandomForest model
        pred_y = float(model.predict(X_pred)[0])
        
        date_str = next_date.strftime("%Y-%m-%d")
        
        # 6. Append to list of predictions
        predictions.append({
            "date": date_str,
            "predicted_sales": pred_y
        })
        
        # 7. Append prediction to the history for subsequent lag computations
        new_row = pd.DataFrame({"ds": [next_date], "y": [pred_y]})
        history = pd.concat([history, new_row], ignore_index=True)
        
    return {"horizon": horizon, "predictions": predictions}

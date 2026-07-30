from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
from pathlib import Path

from app.database import get_db
from app.models import AnomalyLog
from app.ml.anomaly_detector import detect_anomalies_rolling

router = APIRouter()

# Locate the daily_sales CSV
BASE_DIR = Path(__file__).parent.parent.parent.parent
SALES_PATH = BASE_DIR / "data" / "processed" / "daily_sales.csv"


@router.get("/")
def get_anomalies(db: Session = Depends(get_db)):
    """
    Retourne les anomalies détectées récemment (baisses/pics inhabituels).
    Charge daily_sales.csv, exécute la détection d'anomalies sur fenêtre glissante,
    enregistre les anomalies dans la table 'anomalies_log' et les renvoie.
    """
    if not SALES_PATH.exists():
        raise HTTPException(
            status_code=500,
            detail=f"Daily sales file not found at: {SALES_PATH}. Please run data preparation first."
        )

    try:
        # Load daily sales aggregated data
        df = pd.read_csv(SALES_PATH)
        df["ds"] = pd.to_datetime(df["ds"])
        df["y"] = pd.to_numeric(df["y"])
        series = df.set_index("ds")["y"].sort_index()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to read daily sales data: {str(e)}"
        )

    try:
        # Run rolling anomaly detection (last 30 days vs 90 days baseline)
        anomalies_df = detect_anomalies_rolling(
            series, 
            threshold=2.0, 
            window_size=30, 
            baseline_size=90
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Anomaly detection failed: {str(e)}"
        )

    # Clean existing anomalies in DB for metric 'daily_sales' to prevent duplicate accumulations
    try:
        db.query(AnomalyLog).filter(AnomalyLog.metric == "daily_sales").delete()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to clear existing anomalies in database: {str(e)}"
        )

    # Process each anomaly, generate messages, save to DB, and build response
    response_anomalies = []
    for _, row in anomalies_df.iterrows():
        date_str = row["date"]
        val = row["value"]
        deviation_pct = float(row["deviation_pct"])
        
        # Determine movement
        movement = "augmenté" if deviation_pct > 0 else "chuté"
        abs_dev = abs(deviation_pct)
        
        # Format the French message
        message = (
            f"⚠ Les ventes du {date_str} ont {movement} de {abs_dev:.1f}% "
            f"par rapport à la moyenne des 90 jours précédents."
        )
        
        # Save to DB
        anomaly_record = AnomalyLog(
            metric="daily_sales",
            deviation_pct=deviation_pct,
            message=message
        )
        db.add(anomaly_record)
        
        response_anomalies.append({
            "date": date_str,
            "deviation_pct": deviation_pct,
            "message": message
        })

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save anomalies to database: {str(e)}"
        )

    return {"anomalies": response_anomalies}

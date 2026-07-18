import pandas as pd
from pathlib import Path
from fastapi import APIRouter, HTTPException

router = APIRouter()

# Locate the segments file
BASE_DIR = Path(__file__).parent.parent.parent.parent
SEGMENTS_PATH = BASE_DIR / "data" / "processed" / "customer_segments.csv"


@router.get("/")
def get_customer_segments():
    """
    Retourne la répartition des clients par segment RFM :
    VIP / Fidèles / Occasionnels / À risque.
    """
    if not SEGMENTS_PATH.exists():
        raise HTTPException(
            status_code=500,
            detail="Customer segments file is missing. Please run train_segmentation first."
        )

    try:
        # Load only the segment_label column to optimize memory and speed
        df = pd.read_csv(SEGMENTS_PATH, usecols=["segment_label"])
        counts = df["segment_label"].value_counts().to_dict()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to read customer segments data: {str(e)}"
        )

    return {
        "segments": [
            {"name": "VIP", "count": int(counts.get("VIP", 0))},
            {"name": "Fidèles", "count": int(counts.get("Fidèles", 0))},
            {"name": "Occasionnels", "count": int(counts.get("Occasionnels", 0))},
            {"name": "À risque", "count": int(counts.get("À risque", 0))},
        ]
    }

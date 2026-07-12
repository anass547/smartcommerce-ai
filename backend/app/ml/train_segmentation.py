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

BASE_DIR = Path(__file__).parent.parent.parent.parent
SAVED_MODELS_DIR = Path(__file__).parent / "saved_models"


def compute_rfm(orders_df: pd.DataFrame) -> pd.DataFrame:
    """
    In this offline workflow, RFM is pre-calculated by data_prep.py and loaded directly.
    We keep this function signature to match the project skeleton and return the loaded data.
    """
    rfm_path = BASE_DIR / "data" / "processed" / "rfm_data.csv"
    if not rfm_path.exists():
        raise FileNotFoundError(f"Processed RFM file not found at: {rfm_path}. Please run data_prep first.")
    return pd.read_csv(rfm_path)


def train():
    print("Loading precalculated RFM data...")
    rfm = compute_rfm(None)
    print(f"Data loaded. Shape: {rfm.shape}")

    # Scale RFM features
    print("Scaling RFM features...")
    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm[["recency", "frequency", "monetary"]])

    # Train KMeans (4 clusters)
    print("Training K-Means (k=4)...")
    kmeans = KMeans(n_clusters=4, random_state=42)
    rfm["cluster"] = kmeans.fit_predict(rfm_scaled)

    # Save trained scaler and model
    SAVED_MODELS_DIR.mkdir(exist_ok=True)
    model_path = SAVED_MODELS_DIR / "segmentation_model.pkl"
    with open(model_path, "wb") as f:
        pickle.dump({"kmeans": kmeans, "scaler": scaler}, f)
    print(f"Model and scaler saved to {model_path}.")

    # Programmatic cluster labeling based on centroids
    print("Labeling clusters based on centroids...")
    means = rfm.groupby("cluster")[["recency", "frequency", "monetary"]].mean()
    
    # 1. VIP: highest monetary value
    vip_cluster = means["monetary"].idxmax()
    
    # 2. À risque: highest recency (excluding VIP)
    remaining_clusters = [c for c in range(4) if c != vip_cluster]
    at_risk_cluster = means.loc[remaining_clusters, "recency"].idxmax()
    
    # 3. Fidèles vs Occasionnels among remaining two
    last_two = [c for c in remaining_clusters if c != at_risk_cluster]
    c1, c2 = last_two[0], last_two[1]
    if means.loc[c1, "frequency"] > means.loc[c2, "frequency"]:
        loyal_cluster = c1
        occasional_cluster = c2
    else:
        loyal_cluster = c2
        occasional_cluster = c1

    cluster_labels = {
        vip_cluster: "VIP",
        loyal_cluster: "Fidèles",
        occasional_cluster: "Occasionnels",
        at_risk_cluster: "À risque"
    }
    
    rfm["segment_name"] = rfm["cluster"].map(cluster_labels)

    # Print summary of clusters
    print("\nTraining summary:")
    for cluster_id, label in cluster_labels.items():
        count = len(rfm[rfm["cluster"] == cluster_id])
        print(f"  Segment: {label} (Cluster {cluster_id}) -> Count: {count}")
        print(f"    Mean Recency: {means.loc[cluster_id, 'recency']:.1f} days")
        print(f"    Mean Frequency: {means.loc[cluster_id, 'frequency']:.2f} orders")
        print(f"    Mean Monetary: {means.loc[cluster_id, 'monetary']:.2f} €")

    # Map back to transactional customer_id for database and API use
    print("\nMapping segments to transactional customer IDs...")
    map_path = BASE_DIR / "data" / "processed" / "customer_id_map.csv"
    if not map_path.exists():
        raise FileNotFoundError(f"Customer ID mapping file not found at: {map_path}")
        
    cust_map = pd.read_csv(map_path)
    # Merge RFM results with mapping
    customer_segments = cust_map.merge(rfm, on="customer_unique_id", how="inner")
    
    # Save the full mapped segments CSV
    segments_output_path = BASE_DIR / "data" / "processed" / "customer_segments.csv"
    customer_segments.to_csv(segments_output_path, index=False)
    print(f"Customer segment mappings saved to {segments_output_path}. Total rows: {customer_segments.shape[0]}")
    print("Modèle de segmentation entraîné et sauvegardé.")


if __name__ == "__main__":
    train()

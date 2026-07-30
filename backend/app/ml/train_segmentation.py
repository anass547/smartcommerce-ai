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

    # Programmatic cluster labeling based on centroids
    print("Labeling clusters based on centroids...")
    
    # 1. Compute the mean recency, frequency, monetary per cluster
    means = rfm.groupby("cluster")[["recency", "frequency", "monetary"]].mean()
    
    # 2. Build a composite score per cluster: rank(monetary) + rank(frequency) + rank(-recency)
    # We rank clusters' means across the 4 clusters. Higher rank means better (more monetary, more frequency, less recency).
    # Since recency is lower-is-better, we invert it (using -recency) to make lower recency values get higher ranks.
    monetary_rank = means["monetary"].rank(ascending=True)
    frequency_rank = means["frequency"].rank(ascending=True)
    recency_rank = (-means["recency"]).rank(ascending=True)
    
    composite_score = monetary_rank + frequency_rank + recency_rank
    
    # Sort clusters by this score descending
    sorted_clusters = composite_score.sort_values(ascending=False).index.tolist()
    
    # Assign labels in order: "VIP" (best score), "Fidèles", "Occasionnels", "À risque" (worst score)
    labels = ["VIP", "Fidèles", "Occasionnels", "À risque"]
    cluster_to_label = dict(zip(sorted_clusters, labels))

    # Save trained scaler, model, and cluster_to_label mapping dict
    SAVED_MODELS_DIR.mkdir(parents=True, exist_ok=True)
    model_path = SAVED_MODELS_DIR / "segmentation_model.pkl"
    with open(model_path, "wb") as f:
        pickle.dump({
            "kmeans": kmeans, 
            "scaler": scaler,
            "cluster_to_label": cluster_to_label
        }, f)
    print(f"Model, scaler and mapping dict saved to {model_path}.")
    
    rfm["segment_label"] = rfm["cluster"].map(cluster_to_label)

    # Print summary of clusters
    print("\nTraining summary (counts per segment label):")
    for label in labels:
        count = len(rfm[rfm["segment_label"] == label])
        # Find which cluster ID corresponds to this label
        cluster_id = [cid for cid, lbl in cluster_to_label.items() if lbl == label][0]
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
    
    # Keep only the requested columns
    customer_segments = customer_segments[[
        "customer_id",
        "customer_unique_id",
        "recency",
        "frequency",
        "monetary",
        "cluster",
        "segment_label"
    ]]
    
    # Save the full mapped segments CSV
    segments_output_path = BASE_DIR / "data" / "processed" / "customer_segments.csv"
    customer_segments.to_csv(segments_output_path, index=False)
    print(f"Customer segment mappings saved to {segments_output_path}. Total rows: {customer_segments.shape[0]}")
    print("Modèle de segmentation entraîné et sauvegardé.")


if __name__ == "__main__":
    train()

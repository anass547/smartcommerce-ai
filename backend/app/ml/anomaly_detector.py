"""
Détection d'anomalies simple par z-score sur les ventes journalières.
"""
import pandas as pd


def detect_anomalies(series: pd.Series, threshold: float = 2.0) -> pd.DataFrame:
    """
    Retourne les points de la série dont le z-score dépasse le seuil
    (baisse brutale ou pic inhabituel).

    :param series: série temporelle des ventes (index = date)
    :param threshold: seuil en écarts-types (2.0 par défaut)
    :return: DataFrame avec colonnes 'date', 'value', 'deviation_pct'
    """
    mean = series.mean()
    std = series.std()
    
    if pd.isna(mean) or pd.isna(std) or std == 0:
        return pd.DataFrame(columns=["date", "value", "deviation_pct"])
        
    z_scores = (series - mean) / std
    anomalies = series[z_scores.abs() > threshold]
    
    dates = []
    for d in anomalies.index:
        if hasattr(d, "strftime"):
            dates.append(d.strftime("%Y-%m-%d"))
        else:
            dates.append(str(d)[:10])
            
    result = pd.DataFrame(
        {
            "date": dates,
            "value": [float(v) for v in anomalies.values],
            "deviation_pct": [round(float(v), 1) for v in ((anomalies - mean) / mean * 100).values],
        }
    )
    return result


def detect_anomalies_rolling(
    series: pd.Series,
    threshold: float = 2.0,
    window_size: int = 30,
    baseline_size: int = 90
) -> pd.DataFrame:
    """
    Détecte les anomalies récentes (les derniers `window_size` jours) en utilisant
    les `baseline_size` jours précédents comme base de comparaison pour chaque jour.

    :param series: série temporelle des ventes (index = date)
    :param threshold: seuil en écarts-types (2.0 par défaut)
    :param window_size: nombre de jours récents à analyser (par défaut 30)
    :param baseline_size: taille de la fenêtre de référence précédente (par défaut 90)
    :return: DataFrame avec colonnes 'date', 'value', 'deviation_pct'
    """
    n = len(series)
    if n < window_size + baseline_size:
        raise ValueError(
            f"La série doit contenir au moins {window_size + baseline_size} points "
            f"(reçus: {n})."
        )
    
    anomaly_dates = []
    anomaly_values = []
    anomaly_deviations = []
    
    start_idx = n - window_size
    for i in range(start_idx, n):
        val = series.iloc[i]
        date = series.index[i]
        
        # Fenêtre de référence : les `baseline_size` points précédant le point courant
        baseline = series.iloc[i - baseline_size : i]
        mean_base = baseline.mean()
        std_base = baseline.std()
        
        if pd.isna(mean_base) or pd.isna(std_base) or std_base == 0:
            continue
            
        z_score = (val - mean_base) / std_base
        
        if abs(z_score) > threshold:
            if hasattr(date, "strftime"):
                date_str = date.strftime("%Y-%m-%d")
            else:
                date_str = str(date)[:10]
                
            deviation_pct = ((val - mean_base) / mean_base) * 100
            
            anomaly_dates.append(date_str)
            anomaly_values.append(float(val))
            anomaly_deviations.append(round(deviation_pct, 1))
            
    return pd.DataFrame(
        {
            "date": anomaly_dates,
            "value": anomaly_values,
            "deviation_pct": anomaly_deviations,
        }
    )

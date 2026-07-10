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
    """
    mean = series.mean()
    std = series.std()
    z_scores = (series - mean) / std

    anomalies = series[z_scores.abs() > threshold]
    result = pd.DataFrame(
        {
            "date": anomalies.index,
            "value": anomalies.values,
            "deviation_pct": ((anomalies - mean) / mean * 100).round(1).values,
        }
    )
    return result

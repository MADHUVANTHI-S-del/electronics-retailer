import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from typing import List, Dict, Any
from src.utils.logger import logger

class SKUAnomalyDetector:
    """Anomaly detection engine for identifying sudden return rate spikes by SKU."""

    def __init__(self, contamination: float = 0.05, z_threshold: float = 2.5):
        self.contamination = contamination
        self.z_threshold = z_threshold
        self.iso_forest = IsolationForest(contamination=contamination, random_state=42)

    def detect_sku_anomalies(self, master_df: pd.DataFrame) -> pd.DataFrame:
        """Calculates SKU baseline vs current return rates and flags anomalies."""
        sku_stats = master_df.groupby("sku").agg(
            total_returns=("return_id", "count"),
            defect_count=("ground_truth_reason", lambda x: (x == "PRODUCT_DEFECT").sum()),
            compat_count=("ground_truth_reason", lambda x: (x == "COMPATIBILITY_ISSUE").sum()),
            listing_count=("ground_truth_reason", lambda x: (x == "LISTING_MISMATCH").sum()),
            shipping_count=("ground_truth_reason", lambda x: (x == "SHIPPING_DAMAGE").sum()),
            dominant_reason=("ground_truth_reason", lambda x: x.mode()[0] if not x.empty else "PRODUCT_DEFECT"),
            product_name=("product_name", "first"),
            product_category=("product_category", "first"),
            price=("price", "first")
        ).reset_index()

        mean_returns = sku_stats["total_returns"].mean()
        std_returns = sku_stats["total_returns"].std() if sku_stats["total_returns"].std() > 0 else 1.0

        sku_stats["historical_baseline"] = round(mean_returns, 1)
        sku_stats["z_score"] = (sku_stats["total_returns"] - mean_returns) / std_returns

        # Isolation Forest anomaly scoring
        features = sku_stats[["total_returns", "defect_count", "compat_count", "z_score"]].fillna(0)
        sku_stats["iso_anomaly"] = self.iso_forest.fit_predict(features) == -1
        sku_stats["is_anomaly"] = (sku_stats["z_score"] >= self.z_threshold) | sku_stats["iso_anomaly"]

        anomalies_df = sku_stats[sku_stats["is_anomaly"]].copy()
        anomalies_df["volume_difference"] = anomalies_df["total_returns"] - anomalies_df["historical_baseline"]

        logger.info(f"Detected {len(anomalies_df)} SKU return anomalies out of {len(sku_stats)} SKUs.")
        return anomalies_df

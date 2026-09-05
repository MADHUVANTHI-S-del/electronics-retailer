import pandas as pd
import numpy as np

PRE_INSPECTION_OPS_COLS = [
    "days_since_purchase", "support_contact_count", "attempted_troubleshooting",
    "carrier_delay_hours", "backlog_size"
]

POST_INSPECTION_COLS = [
    "physical_damage", "missing_accessories", "packaging_damage",
    "water_damage", "battery_health", "compatibility_verified", "fault_confirmed"
]

def extract_operational_features(df: pd.DataFrame, include_post_inspection: bool = False) -> pd.DataFrame:
    """Extracts operational and customer action features."""
    feats = pd.DataFrame(index=df.index)

    feats["days_since_purchase"] = pd.to_numeric(df.get("days_since_purchase", 7), errors="coerce").fillna(7)
    feats["support_contact_count"] = pd.to_numeric(df.get("support_contact_count", 0), errors="coerce").fillna(0)
    feats["attempted_troubleshooting"] = df.get("attempted_troubleshooting", False).astype(int)
    feats["carrier_delay_hours"] = pd.to_numeric(df.get("carrier_delay_hours", 0.0), errors="coerce").fillna(0.0)
    feats["backlog_size"] = pd.to_numeric(df.get("backlog_size", 0), errors="coerce").fillna(0)

    if include_post_inspection:
        feats["physical_damage"] = df.get("physical_damage", False).astype(int)
        feats["missing_accessories"] = df.get("missing_accessories", False).astype(int)
        feats["packaging_damage"] = df.get("packaging_damage", False).astype(int)
        feats["water_damage"] = df.get("water_damage", False).astype(int)
        feats["battery_health"] = pd.to_numeric(df.get("battery_health", 100), errors="coerce").fillna(100)
        feats["compatibility_verified"] = df.get("compatibility_verified", True).astype(int)
        feats["fault_confirmed"] = df.get("fault_confirmed", False).astype(int)

    return feats

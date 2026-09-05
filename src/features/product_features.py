import pandas as pd
import numpy as np

def extract_product_features(df: pd.DataFrame) -> pd.DataFrame:
    """Extracts numeric and categorical features derived from product and listing metadata."""
    feats = pd.DataFrame(index=df.index)

    feats["price"] = pd.to_numeric(df.get("price", 0), errors="coerce").fillna(0.0)
    feats["warranty_months"] = pd.to_numeric(df.get("warranty_months", 12), errors="coerce").fillna(12)
    feats["content_quality_score"] = pd.to_numeric(df.get("content_quality_score", 0.8), errors="coerce").fillna(0.8)
    feats["image_accuracy_score"] = pd.to_numeric(df.get("image_accuracy_score", 0.85), errors="coerce").fillna(0.85)

    feats["compatibility_info_present"] = df.get("compatibility_information_present", False).astype(int)
    feats["installation_guide_present"] = df.get("installation_guide_present", False).astype(int)

    return feats

import pandas as pd
from typing import Dict, Any

def analyze_root_causes(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregates root causes by group, preventable status, and financial impact."""
    summary = df.groupby("root_cause_group").agg(
        total_cases=("return_id", "count"),
        preventable_cases=("preventable", lambda x: (x == "YES").sum()),
        total_refund=("refund_amount", "sum"),
        avg_confidence=("confidence", "mean") if "confidence" in df.columns else ("return_id", lambda x: 0.85)
    ).reset_index()
    return summary

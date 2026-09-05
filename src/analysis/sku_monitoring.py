import pandas as pd

def monitor_sku_health(df: pd.DataFrame) -> pd.DataFrame:
    """Generates SKU-level risk monitoring summary table."""
    sku_health = df.groupby("sku").agg(
        return_count=("return_id", "count"),
        product_name=("product_name", "first"),
        category=("product_category", "first"),
        total_refund=("refund_amount", "sum"),
        dominant_reason=("ground_truth_reason", lambda x: x.mode()[0] if not x.empty else "N/A"),
        preventable_count=("preventable", lambda x: (x == "YES").sum())
    ).reset_index()

    sku_health["preventable_pct"] = round((sku_health["preventable_count"] / sku_health["return_count"]) * 100.0, 1)
    return sku_health.sort_values(by="return_count", ascending=False)

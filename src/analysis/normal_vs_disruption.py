import pandas as pd
import numpy as np
from pathlib import Path
from src.utils.logger import logger
from src.utils.helpers import get_project_root

def run_normal_vs_disruption_experiment(master_df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes comparative metrics across operational scenarios:
    NORMAL, CAPACITY_LOSS, DELIVERY_DELAY, URGENT_DEMAND.
    """
    results = []

    for scenario, group in master_df.groupby("scenario"):
        total_returns = len(group)
        avg_capacity = round(float(group["processing_capacity"].mean()), 1)
        avg_processing_time = round(float(group["average_processing_minutes"].mean()), 1)
        avg_backlog = round(float(group["backlog_size"].mean()), 1)
        shipping_dmg_pct = round(float((group["ground_truth_reason"] == "SHIPPING_DAMAGE").mean() * 100.0), 1)
        preventable_pct = round(float((group["preventable"] == "YES").mean() * 100.0), 1)
        total_refund_exp = round(float(group["refund_amount"].sum()), 2)
        high_prio_alerts = int((group["severity"].isin(["HIGH", "CRITICAL"])).sum())

        results.append({
            "Scenario": scenario,
            "Total Returns": total_returns,
            "Avg Processing Capacity": avg_capacity,
            "Avg Processing Time (min)": avg_processing_time,
            "Avg Backlog Size": avg_backlog,
            "Shipping Damage %": shipping_dmg_pct,
            "Preventable Return %": preventable_pct,
            "High Priority Alerts": high_prio_alerts,
            "Total Refund Exposure ($)": total_refund_exp
        })

    exp_df = pd.DataFrame(results)
    root = get_project_root()
    output_path = root / "reports" / "normal_vs_disruption.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    exp_df.to_csv(output_path, index=False)
    logger.info(f"Normal vs Disruption experiment saved to {output_path}")
    return exp_df

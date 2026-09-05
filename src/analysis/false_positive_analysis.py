import pandas as pd
import numpy as np
from typing import Dict, Any, List

def analyze_false_positives(df: pd.DataFrame, target_col="ground_truth_reason", pred_col="predicted_reason") -> pd.DataFrame:
    """
    Identifies and analyzes False Positive occurrences per label.
    Example FP: Model predicts PRODUCT_DEFECT but actual ground truth is NO_FAULT_FOUND or CUSTOMER_ORDER_ERROR.
    """
    fp_records = []
    for idx, row in df.iterrows():
        actual = row[target_col]
        predicted = row[pred_col]

        if actual != predicted:
            fp_records.append({
                "return_id": row.get("return_id", f"RET-{idx}"),
                "actual_label": actual,
                "predicted_label": predicted,
                "confidence": row.get("confidence", 0.75),
                "return_text": row.get("return_text", ""),
                "error_type": "False Positive for " + str(predicted),
                "likely_error_reason": f"Ambiguous text or keyword overlap between {actual} and {predicted}"
            })

    fp_df = pd.DataFrame(fp_records)
    return fp_df

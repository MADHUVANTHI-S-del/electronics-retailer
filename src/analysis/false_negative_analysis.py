import pandas as pd
import numpy as np

def analyze_false_negatives(df: pd.DataFrame, target_col="ground_truth_reason", pred_col="predicted_reason") -> pd.DataFrame:
    """
    Identifies and analyzes False Negative occurrences per critical label.
    Example FN: Actual ground truth is PRODUCT_DEFECT but model predicts CUSTOMER_ORDER_ERROR or NO_FAULT_FOUND.
    """
    fn_records = []
    for idx, row in df.iterrows():
        actual = row[target_col]
        predicted = row[pred_col]

        if actual != predicted:
            fn_records.append({
                "return_id": row.get("return_id", f"RET-{idx}"),
                "actual_label": actual,
                "predicted_label": predicted,
                "confidence": row.get("confidence", 0.75),
                "return_text": row.get("return_text", ""),
                "error_type": "False Negative for " + str(actual),
                "likely_error_reason": f"Customer phrasing missed critical failure keywords for {actual}"
            })

    fn_df = pd.DataFrame(fn_records)
    return fn_df

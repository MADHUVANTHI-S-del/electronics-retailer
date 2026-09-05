import numpy as np
import pandas as pd
from typing import Dict, Any
from src.utils.logger import logger

def optimize_confidence_threshold(y_true, y_pred_proba, classes, min_precision: float = 0.85) -> Dict[str, Any]:
    """
    Optimizes confidence threshold on validation data targeting high-priority precision >= min_precision.
    Returns optimal threshold dict.
    """
    max_confidences = np.max(y_pred_proba, axis=1)
    pred_class_indices = np.argmax(y_pred_proba, axis=1)
    predicted_labels = [classes[idx] for idx in pred_class_indices]

    best_threshold = 0.80
    best_stats = {}

    threshold_candidates = np.linspace(0.50, 0.95, 10)

    for th in threshold_candidates:
        accepted_mask = max_confidences >= th
        if np.sum(accepted_mask) == 0:
            continue

        acc_y_true = np.array(y_true)[accepted_mask]
        acc_y_pred = np.array(predicted_labels)[accepted_mask]

        precision = float(np.mean(acc_y_true == acc_y_pred))
        review_rate = float(np.mean(~accepted_mask))
        coverage = float(np.mean(accepted_mask))

        if precision >= min_precision:
            best_threshold = float(th)
            best_stats = {
                "threshold": round(best_threshold, 2),
                "precision": round(precision, 4),
                "review_rate": round(review_rate, 4),
                "coverage": round(coverage, 4)
            }
            break

    if not best_stats:
        best_threshold = 0.80
        best_stats = {
            "threshold": 0.80,
            "precision": float(np.mean(np.array(y_true) == np.array(predicted_labels))),
            "review_rate": float(np.mean(max_confidences < 0.80)),
            "coverage": float(np.mean(max_confidences >= 0.80))
        }

    logger.info(f"Threshold Optimization Result: {best_stats}")
    return best_stats

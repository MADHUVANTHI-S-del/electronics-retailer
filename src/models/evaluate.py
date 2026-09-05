import pandas as pd
import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
)
from typing import Dict, Any

def evaluate_predictions(y_true, y_pred, model_name: str = "Model") -> Dict[str, Any]:
    """Calculates comprehensive classification metrics for model evaluation."""
    acc = accuracy_score(y_true, y_pred)
    prec_macro = precision_score(y_true, y_pred, average="macro", zero_division=0)
    rec_macro = recall_score(y_true, y_pred, average="macro", zero_division=0)
    f1_macro = f1_score(y_true, y_pred, average="macro", zero_division=0)
    f1_weighted = f1_score(y_true, y_pred, average="weighted", zero_division=0)
    cm = confusion_matrix(y_true, y_pred)

    return {
        "Model": model_name,
        "Accuracy": round(float(acc), 4),
        "Macro Precision": round(float(prec_macro), 4),
        "Macro Recall": round(float(rec_macro), 4),
        "Macro F1": round(float(f1_macro), 4),
        "Weighted F1": round(float(f1_weighted), 4),
        "Confusion_Matrix": cm.tolist()
    }

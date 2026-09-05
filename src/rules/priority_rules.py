from typing import Tuple, Dict

SEVERITY_WEIGHTS = {"CRITICAL": 100, "HIGH": 75, "MEDIUM": 50, "LOW": 25}
PREVENTABILITY_WEIGHTS = {"YES": 100, "UNCERTAIN": 50, "NO": 0}

def calculate_priority_score(
    severity: str,
    refund_amount: float,
    preventable: str,
    confidence: float,
    sku_frequency_score: float = 50.0,
    config_weights: Dict[str, float] = None
) -> float:
    """
    Calculates operational priority score (0-100) using weighted formula:
    priority_score = 0.30*severity + 0.25*frequency + 0.20*financial + 0.15*preventability + 0.10*confidence
    """
    if config_weights is None:
        config_weights = {
            "severity": 0.30,
            "frequency": 0.25,
            "financial": 0.20,
            "preventability": 0.15,
            "confidence": 0.10
        }

    sev_val = SEVERITY_WEIGHTS.get(severity, 25)
    fin_val = min(100.0, (refund_amount / 1000.0) * 100.0)
    prev_val = PREVENTABILITY_WEIGHTS.get(preventable, 50)
    conf_val = confidence * 100.0

    score = (
        config_weights["severity"] * sev_val +
        config_weights["frequency"] * sku_frequency_score +
        config_weights["financial"] * fin_val +
        config_weights["preventability"] * prev_val +
        config_weights["confidence"] * conf_val
    )
    return round(float(np.clip(score, 0.0, 100.0)), 2)

import numpy as np

def get_priority_level(priority_score: float) -> str:
    """Maps 0-100 priority score to P1, P2, P3, P4 levels."""
    if priority_score >= 80.0:
        return "P1"
    elif priority_score >= 60.0:
        return "P2"
    elif priority_score >= 40.0:
        return "P3"
    else:
        return "P4"

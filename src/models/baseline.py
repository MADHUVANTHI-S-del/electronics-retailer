import pandas as pd
import numpy as np
from src.utils.constants import RETURN_REASONS

class KeywordBaselineClassifier:
    """Model 1: Rule & Keyword-based return reason baseline classifier."""

    def predict_single(self, text: str) -> str:
        t = str(text).lower()

        if any(w in t for w in ["crack", "broken", "damaged", "dented", "shattered"]):
            if "shipping" in t or "transit" in t or "arrived" in t or "box" in t:
                return "SHIPPING_DAMAGE"
            elif "dropped" in t or "spilled" in t or "coffee" in t:
                return "CUSTOMER_DAMAGE"
            return "SHIPPING_DAMAGE"

        if any(w in t for w in ["missing", "absent", "not included", "without charger"]):
            return "MISSING_ACCESSORY"

        if any(w in t for w in ["compatible", "connect", "pair", "fit", "iphone", "mac"]):
            return "COMPATIBILITY_ISSUE"

        if any(w in t for w in ["description", "advertised", "wrong model", "wrong color", "wrong size"]):
            return "LISTING_MISMATCH"

        if any(w in t for w in ["battery", "charging", "overheat", "heat", "short circuit", "flicker", "static"]):
            return "PRODUCT_DEFECT"

        if any(w in t for w in ["manual", "instructions", "setup", "software"]):
            return "SETUP_DIFFICULTY"

        if any(w in t for w in ["ordered wrong", "accidental", "mistake", "changed mind"]):
            return "CUSTOMER_ORDER_ERROR"

        if any(w in t for w in ["warranty", "half year", "months"]):
            return "WARRANTY_FAILURE"

        if any(w in t for w in ["works fine", "no fault", "tested fine"]):
            return "NO_FAULT_FOUND"

        if any(w in t for w in ["quality", "expectation", "hoped", "grainy"]):
            return "PERFORMANCE_EXPECTATION"

        if any(w in t for w in ["packaging", "torn", "seal"]):
            return "PACKAGING_ISSUE"

        return "OTHER"

    def predict(self, texts) -> list:
        return [self.predict_single(t) for t in texts]

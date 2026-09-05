import json
import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, List

from src.rules.preventability_rules import determine_preventability
from src.rules.business_rules import get_root_cause_and_owner
from src.rules.priority_rules import calculate_priority_score, get_priority_level
from src.explainability.evidence_builder import build_evidence_package
from src.utils.logger import logger
from src.utils.helpers import get_project_root

class ReturnPredictor:
    """End-to-end Return Insight Prediction & Evidence Engine."""

    def __init__(self):
        root = get_project_root()
        model_path = root / "models" / "return_reason_model.pkl"
        pipeline_path = root / "models" / "feature_pipeline.pkl"
        meta_path = root / "models" / "metadata.json"

        self.is_loaded = False
        if model_path.exists() and pipeline_path.exists():
            try:
                self.model = joblib.load(model_path)
                self.pipeline = joblib.load(pipeline_path)
                with open(meta_path, "r", encoding="utf-8") as f:
                    self.metadata = json.load(f)
                self.is_loaded = True
                logger.info("Loaded trained ML model and feature pipeline.")
            except Exception as e:
                logger.warning(f"Could not load ML model: {e}. Falling back to baseline rules.")

    def predict_single_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Predicts structured return reason, root cause, preventability, confidence, priority, and evidence."""
        df_single = pd.DataFrame([record])

        if self.is_loaded:
            try:
                X_mat = self.pipeline.transform(df_single)
                probs = self.model.predict_proba(X_mat)[0]
                classes = self.model.classes_
                best_idx = np.argmax(probs)
                predicted_reason = str(classes[best_idx])
                confidence = float(probs[best_idx])
            except Exception as e:
                logger.error(f"ML inference error: {e}. Using fallback rule prediction.")
                from src.models.baseline import KeywordBaselineClassifier
                predicted_reason = KeywordBaselineClassifier().predict_single(record.get("return_text", ""))
                confidence = 0.70
        else:
            from src.models.baseline import KeywordBaselineClassifier
            predicted_reason = KeywordBaselineClassifier().predict_single(record.get("return_text", ""))
            confidence = 0.70

        # Handle Edge Case 1: Ambiguous text "doesn't work" -> low confidence & manual review
        text_clean = str(record.get("return_text", "")).lower().strip()
        if text_clean in ["doesn't work", "not working", "bad product", "not fit", "just return it"]:
            confidence = min(confidence, 0.58)

        # Rules mapping
        root_cause_group, default_owner = get_root_cause_and_owner(predicted_reason)
        preventable, owner = determine_preventability(predicted_reason)

        # Build evidence
        evidence_pkg = build_evidence_package(record, predicted_reason, confidence)

        # Priority calculation
        refund_amt = float(record.get("refund_amount", 50.0))
        severity = "CRITICAL" if predicted_reason == "PRODUCT_DEFECT" and refund_amt > 400 else (
            "HIGH" if predicted_reason in ["PRODUCT_DEFECT", "WARRANTY_FAILURE", "LISTING_MISMATCH"] else (
                "MEDIUM" if predicted_reason in ["SHIPPING_DAMAGE", "COMPATIBILITY_ISSUE", "MISSING_ACCESSORY"] else "LOW"
            )
        )

        prio_score = calculate_priority_score(
            severity=severity,
            refund_amount=refund_amt,
            preventable=preventable,
            confidence=confidence
        )
        priority_level = get_priority_level(prio_score)

        # Decision threshold status
        if confidence >= 0.85 and not evidence_pkg.get("has_conflicts"):
            review_status = "AUTO_ACCEPT"
        elif confidence >= 0.65 and not evidence_pkg.get("has_conflicts"):
            review_status = "REVIEW_RECOMMENDED"
        else:
            review_status = "MANUAL_REVIEW_REQUIRED"

        # Recommended Action text
        action_map = {
            "PRODUCT_DEFECT": "Escalate to Product Quality team and supplier to inspect hardware batch.",
            "SHIPPING_DAMAGE": "Review carrier handling and transit packaging standards with Logistics.",
            "PACKAGING_ISSUE": "Notify Warehouse operations to inspect carton seal and box protection.",
            "MISSING_ACCESSORY": "Audit supplier packaging line and issue replacement accessory.",
            "LISTING_MISMATCH": "Update product title, description, and specifications on web store.",
            "COMPATIBILITY_ISSUE": "Add explicit compatibility matrix and device support list on listing page.",
            "SETUP_DIFFICULTY": "Enhance quick-start guide and publish video setup tutorial.",
            "CUSTOMER_ORDER_ERROR": "Simplify product model variants on storefront to prevent customer confusion.",
            "CUSTOMER_DAMAGE": "Process return per customer-damage policy (non-preventable).",
            "PERFORMANCE_EXPECTATION": "Adjust product marketing claims to match real-world specifications.",
            "WARRANTY_FAILURE": "Process warranty claim and log defect telemetry with engineering.",
            "NO_FAULT_FOUND": "Review troubleshooting guides with customer support team."
        }
        rec_action = action_map.get(predicted_reason, "Inspect return record and update case notes.")

        return {
            "return_id": record.get("return_id", "RET-NEW"),
            "sku": record.get("sku", "UNKNOWN"),
            "predicted_reason": predicted_reason,
            "confidence": round(confidence, 4),
            "root_cause_group": root_cause_group,
            "preventable": preventable,
            "recommended_owner": owner,
            "severity": severity,
            "priority_score": prio_score,
            "priority": priority_level,
            "review_status": review_status,
            "evidence": evidence_pkg,
            "recommended_action": rec_action
        }

predictor = ReturnPredictor()

import uuid
import datetime
import pandas as pd
from sqlalchemy.orm import Session
from pathlib import Path

from app.models import ReviewRecord, PredictionRecord, AuditLogRecord
from app.schemas import HumanReviewSubmission
from src.utils.logger import logger
from src.utils.helpers import get_project_root

def submit_human_review(db: Session, review_sub: HumanReviewSubmission) -> dict:
    """Processes human override/acceptance, stores review audit record, and logs feedback dataset."""
    pred = db.query(PredictionRecord).filter(PredictionRecord.return_id == review_sub.return_id).first()

    orig_reason = pred.predicted_reason if pred else "UNKNOWN"
    orig_conf = pred.confidence if pred else 0.70

    review_id = f"REV-{uuid.uuid4().hex[:8].upper()}"

    # Update prediction review status in DB
    if pred:
        if review_sub.decision == "ACCEPTED":
            pred.review_status = "ACCEPTED"
        elif review_sub.decision == "OVERRIDDEN":
            pred.review_status = "OVERRIDDEN"
            if review_sub.corrected_label:
                pred.predicted_reason = review_sub.corrected_label
            if review_sub.corrected_root_cause:
                pred.root_cause_group = review_sub.corrected_root_cause
            if review_sub.corrected_preventable:
                pred.preventable = review_sub.corrected_preventable
            if review_sub.corrected_priority:
                pred.priority = review_sub.corrected_priority
        elif review_sub.decision == "ESCALATED":
            pred.review_status = "ESCALATED"

    # Save ReviewRecord
    new_rev = ReviewRecord(
        review_id=review_id,
        return_id=review_sub.return_id,
        original_prediction=orig_reason,
        original_confidence=orig_conf,
        human_decision=review_sub.decision,
        corrected_label=review_sub.corrected_label,
        reviewer=review_sub.reviewer,
        review_notes=review_sub.review_notes,
        review_timestamp=datetime.datetime.utcnow()
    )
    db.add(new_rev)

    # Save AuditLogRecord
    audit = AuditLogRecord(
        entity_name="PredictionRecord",
        entity_id=review_sub.return_id,
        action=f"HUMAN_REVIEW_{review_sub.decision}",
        performed_by=review_sub.reviewer,
        details=f"Original: {orig_reason}, Corrected: {review_sub.corrected_label}, Notes: {review_sub.review_notes}"
    )
    db.add(audit)

    db.commit()

    # Append to human feedback dataset in data/processed/human_feedback.csv
    root = get_project_root()
    fb_path = root / "data" / "processed" / "human_feedback.csv"
    fb_path.parent.mkdir(parents=True, exist_ok=True)

    fb_data = {
        "review_id": [review_id],
        "return_id": [review_sub.return_id],
        "original_prediction": [orig_reason],
        "human_decision": [review_sub.decision],
        "corrected_label": [review_sub.corrected_label or orig_reason],
        "reviewer": [review_sub.reviewer],
        "review_notes": [review_sub.review_notes],
        "timestamp": [datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")]
    }
    fb_df = pd.DataFrame(fb_data)
    if fb_path.exists():
        fb_df.to_csv(fb_path, mode="a", header=False, index=False)
    else:
        fb_df.to_csv(fb_path, index=False)

    logger.info(f"Recorded human review {review_id} for return {review_sub.return_id}.")
    return {
        "status": "SUCCESS",
        "review_id": review_id,
        "return_id": review_sub.return_id,
        "decision": review_sub.decision
    }

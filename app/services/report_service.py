import pandas as pd
from sqlalchemy.orm import Session
from pathlib import Path

from app.models import PredictionRecord, AlertRecord, ReviewRecord, ReturnRecord
from src.utils.helpers import get_project_root

def export_all_reports(db: Session) -> dict:
    """Generates downloadable CSV reports in the reports/ directory."""
    root = get_project_root()
    reports_dir = root / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    # 1. Analysed Returns CSV
    preds = db.query(PredictionRecord).all()
    pred_data = [{
        "return_id": p.return_id,
        "predicted_reason": p.predicted_reason,
        "confidence": p.confidence,
        "root_cause_group": p.root_cause_group,
        "preventable": p.preventable,
        "recommended_owner": p.recommended_owner,
        "severity": p.severity,
        "priority": p.priority,
        "priority_score": p.priority_score,
        "review_status": p.review_status,
        "recommended_action": p.recommended_action
    } for p in preds]
    df_preds = pd.DataFrame(pred_data)
    df_preds.to_csv(reports_dir / "analysed_returns.csv", index=False)

    # 2. High Priority Alerts CSV
    alerts = db.query(AlertRecord).filter(AlertRecord.priority.isin(["P1", "P2"])).all()
    alert_data = [{
        "alert_id": a.alert_id,
        "sku": a.sku,
        "alert_type": a.alert_type,
        "priority": a.priority,
        "title": a.title,
        "description": a.description,
        "status": a.status
    } for a in alerts]
    df_alerts = pd.DataFrame(alert_data)
    df_alerts.to_csv(reports_dir / "high_priority_alerts.csv", index=False)

    # 3. Manual Review Records CSV
    reviews = db.query(ReviewRecord).all()
    rev_data = [{
        "review_id": r.review_id,
        "return_id": r.return_id,
        "original_prediction": r.original_prediction,
        "original_confidence": r.original_confidence,
        "human_decision": r.human_decision,
        "corrected_label": r.corrected_label,
        "reviewer": r.reviewer,
        "review_notes": r.review_notes,
        "review_timestamp": str(r.review_timestamp)
    } for r in reviews]
    df_revs = pd.DataFrame(rev_data)
    df_revs.to_csv(reports_dir / "review_records.csv", index=False)

    return {
        "status": "SUCCESS",
        "generated_files": [
            "analysed_returns.csv",
            "high_priority_alerts.csv",
            "review_records.csv",
            "normal_vs_disruption.csv",
            "model_comparison.csv"
        ]
    }

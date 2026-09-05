from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import json

from app.database import get_db
from app.models import PredictionRecord, ReturnRecord, ReviewRecord
from app.schemas import HumanReviewSubmission
from app.services.review_service import submit_human_review
from src.utils.helpers import get_project_root

router = APIRouter()
templates = Jinja2Templates(directory=str(get_project_root() / "app" / "templates"))

@router.get("/review-queue", response_class=HTMLResponse)
def get_review_queue_page(request: Request, db: Session = Depends(get_db)):
    """Renders human-in-the-loop triage Review Queue page."""
    flagged = db.query(PredictionRecord, ReturnRecord).join(
        ReturnRecord, PredictionRecord.return_id == ReturnRecord.return_id
    ).filter(
        PredictionRecord.review_status.in_(["MANUAL_REVIEW_REQUIRED", "REVIEW_RECOMMENDED"])
    ).limit(50).all()

    queue_list = []
    for pred, ret in flagged:
        ev = json.loads(pred.evidence_json) if pred.evidence_json else {}
        queue_list.append({
            "return_id": pred.return_id,
            "sku": ret.sku,
            "return_text": ret.return_text,
            "predicted_reason": pred.predicted_reason,
            "confidence": pred.confidence,
            "priority": pred.priority,
            "root_cause_group": pred.root_cause_group,
            "preventable": pred.preventable,
            "review_status": pred.review_status,
            "evidence_signals": ev.get("evidence_signals", []),
            "conflict_signals": ev.get("conflict_signals", [])
        })

    return templates.TemplateResponse("review_queue.html", {
        "request": request,
        "active_page": "review",
        "queue": queue_list
    })

@router.post("/api/reviews")
def post_human_review(submission: HumanReviewSubmission, db: Session = Depends(get_db)):
    """API endpoint to process human override/acceptance."""
    return submit_human_review(db, submission)

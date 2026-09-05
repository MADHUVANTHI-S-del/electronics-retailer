from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import json

from app.database import get_db
from app.models import PredictionRecord, ReturnRecord, AlertRecord, ProductRecord, OperationRecord
from src.analysis.kpi_calculator import calculate_business_kpis
from src.utils.helpers import get_project_root

router = APIRouter()
templates = Jinja2Templates(directory=str(get_project_root() / "app" / "templates"))

@router.get("/", response_class=HTMLResponse)
@router.get("/dashboard", response_class=HTMLResponse)
def get_dashboard_page(request: Request, db: Session = Depends(get_db)):
    """Renders main executive dashboard view."""
    preds = db.query(PredictionRecord).all()
    returns = db.query(ReturnRecord).all()

    # Calculate KPIs
    kpi_dict = {
        "total_returns": len(returns),
        "preventable_pct": round(float(sum(1 for p in preds if p.preventable == "YES") / max(1, len(preds))) * 100.0, 1),
        "high_priority_count": db.query(PredictionRecord).filter(PredictionRecord.priority.isin(["P1", "P2"])).count(),
        "manual_review_count": db.query(PredictionRecord).filter(PredictionRecord.review_status == "MANUAL_REVIEW_REQUIRED").count(),
        "avg_confidence": round(float(sum(p.confidence for p in preds) / max(1, len(preds))) * 100.0, 1),
        "total_refund_exposure": round(float(sum(r.refund_amount for r in returns)), 2),
        "top_problem_sku": "SKU-SMA-1001"
    }

    # Chart 1: Return reasons distribution
    reason_counts = {}
    for p in preds:
        reason_counts[p.predicted_reason] = reason_counts.get(p.predicted_reason, 0) + 1

    # Chart 2: Preventability distribution
    prev_counts = {}
    for p in preds:
        prev_counts[p.preventable] = prev_counts.get(p.preventable, 0) + 1

    # Recent alerts
    recent_alerts = db.query(AlertRecord).order_by(AlertRecord.created_at.desc()).limit(5).all()

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "active_page": "dashboard",
        "kpis": kpi_dict,
        "reason_counts_json": json.dumps(reason_counts),
        "prev_counts_json": json.dumps(prev_counts),
        "recent_alerts": recent_alerts
    })

@router.get("/api/dashboard")
def get_dashboard_api(db: Session = Depends(get_db)):
    """API endpoint returning executive dashboard metrics."""
    preds = db.query(PredictionRecord).all()
    returns = db.query(ReturnRecord).all()
    return {
        "total_returns": len(returns),
        "total_predictions": len(preds),
        "high_priority_count": db.query(PredictionRecord).filter(PredictionRecord.priority.isin(["P1", "P2"])).count(),
        "manual_review_queue_size": db.query(PredictionRecord).filter(PredictionRecord.review_status == "MANUAL_REVIEW_REQUIRED").count()
    }

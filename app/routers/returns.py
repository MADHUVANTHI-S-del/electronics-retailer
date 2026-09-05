from fastapi import APIRouter, Depends, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import json

from app.database import get_db
from app.models import ReturnRecord, PredictionRecord, ProductRecord, ListingRecord, CustomerActionRecord, InspectionRecord
from src.utils.helpers import get_project_root

router = APIRouter()
templates = Jinja2Templates(directory=str(get_project_root() / "app" / "templates"))

@router.get("/returns", response_class=HTMLResponse)
def get_returns_page(
    request: Request,
    db: Session = Depends(get_db),
    sku: str = None,
    reason: str = None,
    priority: str = None
):
    """Returns list view page with filtering capabilities."""
    query = db.query(ReturnRecord, PredictionRecord).join(
        PredictionRecord, ReturnRecord.return_id == PredictionRecord.return_id
    )

    if sku:
        query = query.filter(ReturnRecord.sku == sku)
    if reason:
        query = query.filter(PredictionRecord.predicted_reason == reason)
    if priority:
        query = query.filter(PredictionRecord.priority == priority)

    results = query.limit(100).all()

    returns_list = []
    for ret, pred in results:
        returns_list.append({
            "return_id": ret.return_id,
            "sku": ret.sku,
            "return_date": ret.return_date,
            "return_text": ret.return_text,
            "predicted_reason": pred.predicted_reason,
            "confidence": pred.confidence,
            "preventable": pred.preventable,
            "priority": pred.priority,
            "review_status": pred.review_status
        })

    return templates.TemplateResponse("returns.html", {
        "request": request,
        "active_page": "returns",
        "returns": returns_list
    })

@router.get("/returns/{return_id}", response_class=HTMLResponse)
def get_return_detail_page(return_id: str, request: Request, db: Session = Depends(get_db)):
    """360 degree Return Detail page."""
    ret = db.query(ReturnRecord).filter(ReturnRecord.return_id == return_id).first()
    pred = db.query(PredictionRecord).filter(PredictionRecord.return_id == return_id).first()
    prod = db.query(ProductRecord).filter(ProductRecord.sku == ret.sku).first() if ret else None
    listing = db.query(ListingRecord).filter(ListingRecord.sku == ret.sku).first() if ret else None
    action = db.query(CustomerActionRecord).filter(CustomerActionRecord.return_id == return_id).first()
    inspection = db.query(InspectionRecord).filter(InspectionRecord.return_id == return_id).first()

    evidence_dict = json.loads(pred.evidence_json) if (pred and pred.evidence_json) else {}

    return templates.TemplateResponse("return_detail.html", {
        "request": request,
        "active_page": "returns",
        "return": ret,
        "prediction": pred,
        "product": prod,
        "listing": listing,
        "action": action,
        "inspection": inspection,
        "evidence": evidence_dict
    })

@router.get("/api/returns")
def get_returns_api(db: Session = Depends(get_db), limit: int = 50):
    """API endpoint for return records."""
    returns = db.query(ReturnRecord).limit(limit).all()
    return [{"return_id": r.return_id, "sku": r.sku, "return_text": r.return_text} for r in returns]

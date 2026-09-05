from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import json

from app.database import get_db
from app.models import AlertRecord
from src.utils.helpers import get_project_root

router = APIRouter()
templates = Jinja2Templates(directory=str(get_project_root() / "app" / "templates"))

@router.get("/alerts", response_class=HTMLResponse)
def get_alerts_page(request: Request, db: Session = Depends(get_db)):
    """Renders operational Alerts page."""
    alerts = db.query(AlertRecord).order_by(AlertRecord.created_at.desc()).all()
    alert_list = []
    for a in alerts:
        alert_list.append({
            "alert_id": a.alert_id,
            "sku": a.sku,
            "alert_type": a.alert_type,
            "priority": a.priority,
            "title": a.title,
            "description": a.description,
            "evidence": json.loads(a.evidence_json) if a.evidence_json else {},
            "status": a.status,
            "created_at": str(a.created_at)
        })

    return templates.TemplateResponse("alerts.html", {
        "request": request,
        "active_page": "alerts",
        "alerts": alert_list
    })

@router.get("/api/alerts")
def get_alerts_api(db: Session = Depends(get_db)):
    """API endpoint returning alerts."""
    return db.query(AlertRecord).all()

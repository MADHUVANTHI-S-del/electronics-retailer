from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import pandas as pd

from app.database import get_db
from app.models import ProductRecord, ReturnRecord, PredictionRecord, ListingRecord
from src.analysis.sku_monitoring import monitor_sku_health
from src.utils.helpers import get_project_root

router = APIRouter()
templates = Jinja2Templates(directory=str(get_project_root() / "app" / "templates"))

@router.get("/products", response_class=HTMLResponse)
def get_products_page(request: Request, db: Session = Depends(get_db)):
    """Renders Product Root Cause Intelligence Page."""
    query = db.query(
        ReturnRecord.sku,
        ReturnRecord.return_id,
        ReturnRecord.refund_amount,
        ReturnRecord.ground_truth_reason,
        PredictionRecord.preventable,
        PredictionRecord.confidence,
        ProductRecord.product_name,
        ProductRecord.product_category
    ).join(
        PredictionRecord, ReturnRecord.return_id == PredictionRecord.return_id
    ).join(
        ProductRecord, ReturnRecord.sku == ProductRecord.sku
    )

    results = query.all()
    if results:
        df = pd.DataFrame(results, columns=[
            "sku", "return_id", "refund_amount", "ground_truth_reason",
            "preventable", "confidence", "product_name", "product_category"
        ])
        sku_health = monitor_sku_health(df).to_dict(orient="records")
    else:
        sku_health = []

    return templates.TemplateResponse("products.html", {
        "request": request,
        "active_page": "products",
        "sku_list": sku_health[:50]
    })

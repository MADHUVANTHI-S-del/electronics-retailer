from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import pandas as pd

from app.database import get_db
from app.services.report_service import export_all_reports
from src.utils.helpers import get_project_root

router = APIRouter()
templates = Jinja2Templates(directory=str(get_project_root() / "app" / "templates"))

@router.get("/reports", response_class=HTMLResponse)
def get_reports_page(request: Request, db: Session = Depends(get_db)):
    """Renders Reports & Downloads page."""
    export_all_reports(db)
    return templates.TemplateResponse("reports.html", {
        "request": request,
        "active_page": "reports"
    })

@router.get("/reports/download/{filename}")
def download_report_file(filename: str):
    """File response for downloading generated report CSVs."""
    root = get_project_root()
    filepath = root / "reports" / filename
    if filepath.exists():
        return FileResponse(path=filepath, filename=filename, media_type="text/csv")
    return {"error": "Report file not found."}

@router.get("/operations-comparison", response_class=HTMLResponse)
def get_operations_comparison_page(request: Request):
    """Renders Normal vs Disruption Operations Comparison Page."""
    root = get_project_root()
    path = root / "reports" / "normal_vs_disruption.csv"
    if path.exists():
        exp_df = pd.read_csv(path)
        records = exp_df.to_dict(orient="records")
    else:
        records = []

    return templates.TemplateResponse("comparison.html", {
        "request": request,
        "active_page": "operations",
        "scenarios": records
    })

@router.get("/model-performance", response_class=HTMLResponse)
def get_model_performance_page(request: Request):
    """Renders Model Evaluation & FP/FN Analysis Page."""
    root = get_project_root()
    comp_path = root / "reports" / "model_comparison.csv"
    comp_records = pd.read_csv(comp_path).to_dict(orient="records") if comp_path.exists() else []

    return templates.TemplateResponse("model_performance.html", {
        "request": request,
        "active_page": "model_performance",
        "models": comp_records
    })

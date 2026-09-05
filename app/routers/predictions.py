import io
import pandas as pd
from fastapi import APIRouter, Depends, Request, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import ReturnAnalysisRequest
from app.services.prediction_service import analyze_and_store_return
from src.utils.helpers import get_project_root

router = APIRouter()
templates = Jinja2Templates(directory=str(get_project_root() / "app" / "templates"))

@router.get("/analyser", response_class=HTMLResponse)
def get_analyser_page(request: Request):
    """Renders interactive Return Reason Analyser page."""
    return templates.TemplateResponse("analysis.html", {
        "request": request,
        "active_page": "analyser"
    })

@router.post("/api/analyse")
def analyse_single_return(req: ReturnAnalysisRequest, db: Session = Depends(get_db)):
    """API endpoint to run prediction engine on single return payload."""
    record_dict = req.dict()
    result = analyze_and_store_return(db, record_dict)
    return result

@router.post("/api/upload")
async def upload_csv_returns(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Batch processes return records uploaded via CSV."""
    if not file.filename.endswith(".csv"):
        return JSONResponse(status_code=400, content={"error": "File must be a CSV."})

    contents = await file.read()
    df = pd.read_csv(io.BytesIO(contents))

    results = []
    for idx, row in df.iterrows():
        rec_dict = row.to_dict()
        if "return_id" not in rec_dict or pd.isna(rec_dict["return_id"]):
            rec_dict["return_id"] = f"RET-BATCH-{1000 + idx}"
        res = analyze_and_store_return(db, rec_dict)
        results.append(res)

    return {
        "status": "SUCCESS",
        "processed_count": len(results),
        "sample_result": results[0] if results else {}
    }

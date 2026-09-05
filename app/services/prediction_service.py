import json
from sqlalchemy.orm import Session
from app.models import PredictionRecord, ReturnRecord, ProductRecord, ListingRecord
from src.models.predict import predictor
from src.utils.logger import logger

def analyze_and_store_return(db: Session, record_dict: dict) -> dict:
    """Runs prediction engine and stores/updates prediction in database."""
    # Enhance record with database product/listing metadata if available
    sku = record_dict.get("sku")
    if sku:
        prod = db.query(ProductRecord).filter(ProductRecord.sku == sku).first()
        if prod:
            record_dict["price"] = prod.price
            record_dict["warranty_months"] = prod.warranty_months
            record_dict["product_category"] = prod.product_category
            record_dict["product_name"] = prod.product_name

        list_rec = db.query(ListingRecord).filter(ListingRecord.sku == sku).first()
        if list_rec:
            record_dict["content_quality_score"] = list_rec.content_quality_score
            record_dict["compatibility_information_present"] = list_rec.compatibility_information_present
            record_dict["installation_guide_present"] = list_rec.installation_guide_present

    result = predictor.predict_single_record(record_dict)

    # Save/Update in SQLite database
    ret_id = result["return_id"]
    existing_pred = db.query(PredictionRecord).filter(PredictionRecord.return_id == ret_id).first()

    if existing_pred:
        existing_pred.predicted_reason = result["predicted_reason"]
        existing_pred.confidence = result["confidence"]
        existing_pred.root_cause_group = result["root_cause_group"]
        existing_pred.preventable = result["preventable"]
        existing_pred.recommended_owner = result["recommended_owner"]
        existing_pred.severity = result["severity"]
        existing_pred.priority_score = result["priority_score"]
        existing_pred.priority = result["priority"]
        existing_pred.review_status = result["review_status"]
        existing_pred.recommended_action = result["recommended_action"]
        existing_pred.evidence_json = json.dumps(result["evidence"])
    else:
        new_pred = PredictionRecord(
            return_id=ret_id,
            predicted_reason=result["predicted_reason"],
            confidence=result["confidence"],
            root_cause_group=result["root_cause_group"],
            preventable=result["preventable"],
            recommended_owner=result["recommended_owner"],
            severity=result["severity"],
            priority_score=result["priority_score"],
            priority=result["priority"],
            review_status=result["review_status"],
            recommended_action=result["recommended_action"],
            evidence_json=json.dumps(result["evidence"])
        )
        db.add(new_pred)

    db.commit()
    return result

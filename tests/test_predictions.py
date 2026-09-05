import pytest
from src.models.predict import predictor

def test_predict_single_record():
    record = {
        "return_id": "TEST-RET-01",
        "sku": "SKU-TEST-101",
        "return_text": "charger missing from package box",
        "refund_amount": 29.99,
        "product_category": "Chargers"
    }
    result = predictor.predict_single_record(record)
    assert result["predicted_reason"] in ["MISSING_ACCESSORY", "PRODUCT_DEFECT"]
    assert "confidence" in result
    assert result["preventable"] == "YES"
    assert "evidence" in result

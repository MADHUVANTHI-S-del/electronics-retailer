import pytest
from src.models.predict import predictor
from src.explainability.evidence_builder import build_evidence_package

def test_edge_case_1_ambiguous_text():
    """EDGE CASE 1: Ambiguous text ('doesn't work') -> low confidence & manual review."""
    rec = {"return_id": "RET-EC-1", "sku": "SKU-SMA-1001", "return_text": "doesn't work"}
    res = predictor.predict_single_record(rec)
    assert res["confidence"] <= 0.65
    assert res["review_status"] == "MANUAL_REVIEW_REQUIRED"

def test_edge_case_2_contradictory_evidence():
    """EDGE CASE 2: Customer says defective but inspection says No Fault Found -> conflict flagged."""
    rec = {
        "return_id": "RET-EC-2",
        "return_text": "device defective and won't turn on",
        "inspection_outcome": "No Fault Found",
        "fault_confirmed": False
    }
    pkg = build_evidence_package(rec, "PRODUCT_DEFECT", 0.90)
    assert pkg["has_conflicts"] == True
    assert len(pkg["conflict_signals"]) > 0

def test_edge_case_3_listing_induced_compatibility():
    """EDGE CASE 3: Listing missing compatibility details -> COMPATIBILITY_ISSUE, preventable YES."""
    rec = {
        "return_id": "RET-EC-3",
        "return_text": "won't connect to my iPhone 15",
        "compatibility_information_present": False
    }
    res = predictor.predict_single_record(rec)
    assert res["predicted_reason"] == "COMPATIBILITY_ISSUE"
    assert res["preventable"] == "YES"
    assert res["root_cause_group"] == "CONTENT"

def test_edge_case_4_repeated_product_defect():
    """EDGE CASE 4: Battery failure for high-value SKU -> CRITICAL/HIGH priority."""
    rec = {
        "return_id": "RET-EC-4",
        "sku": "SKU-LAP-1004",
        "return_text": "battery gets extremely hot and shorted out",
        "refund_amount": 1200.0
    }
    res = predictor.predict_single_record(rec)
    assert res["severity"] == "CRITICAL"
    assert res["priority"] in ["P1", "P2"]

def test_edge_case_5_missing_accessory():
    """EDGE CASE 5: Charger missing from box -> MISSING_ACCESSORY, preventable YES, owner Supplier."""
    rec = {
        "return_id": "RET-EC-5",
        "return_text": "charger was not inside sealed box",
        "missing_accessories": True
    }
    res = predictor.predict_single_record(rec)
    assert res["predicted_reason"] == "MISSING_ACCESSORY"
    assert res["preventable"] == "YES"
    assert res["recommended_owner"] == "Supplier"

def test_edge_case_6_customer_damage():
    """EDGE CASE 6: Dropped screen with physical impact mark -> CUSTOMER_DAMAGE, preventable NO."""
    rec = {
        "return_id": "RET-EC-6",
        "return_text": "dropped phone on tile floor screen cracked",
        "physical_damage": True
    }
    res = predictor.predict_single_record(rec)
    assert res["predicted_reason"] == "CUSTOMER_DAMAGE"
    assert res["preventable"] == "NO"
    assert res["recommended_owner"] == "Customer"

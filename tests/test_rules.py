import pytest
from src.rules.preventability_rules import determine_preventability
from src.rules.business_rules import get_root_cause_and_owner
from src.rules.priority_rules import calculate_priority_score, get_priority_level

def test_preventability_rules():
    prev, owner = determine_preventability("LISTING_MISMATCH")
    assert prev == "YES"
    assert owner == "Content Team"

    prev_dmg, owner_dmg = determine_preventability("CUSTOMER_DAMAGE")
    assert prev_dmg == "NO"
    assert owner_dmg == "Customer"

def test_priority_calculation():
    score = calculate_priority_score(
        severity="CRITICAL",
        refund_amount=500.0,
        preventable="YES",
        confidence=0.90
    )
    prio_level = get_priority_level(score)
    assert score >= 60.0
    assert prio_level in ["P1", "P2"]

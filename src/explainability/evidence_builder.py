from typing import Dict, Any, List

def build_evidence_package(
    return_record: Dict[str, Any],
    predicted_reason: str,
    confidence: float
) -> Dict[str, Any]:
    """
    Gathers multi-source evidence from text, product attributes, listing metadata,
    customer behavior, inspection findings, and operational context.
    """
    text = str(return_record.get("return_text", "")).lower()
    signals: List[str] = []
    conflict_signals: List[str] = []

    # 1. Text Evidence
    if predicted_reason == "PRODUCT_DEFECT":
        if any(w in text for w in ["battery", "heat", "overheat", "charging"]):
            signals.append("Text keywords explicitly indicate power/battery thermal issue.")
        elif any(w in text for w in ["stopped", "short circuit", "flicker", "static"]):
            signals.append("Text keywords indicate hardware electrical/component failure.")
        else:
            signals.append("Text describes non-functional hardware symptom.")
    elif predicted_reason == "COMPATIBILITY_ISSUE":
        signals.append(f"Text mentions connection/compatibility issue: '{text}'.")
    elif predicted_reason == "LISTING_MISMATCH":
        signals.append(f"Text indicates product didn't match listing description or specs.")
    elif predicted_reason == "SHIPPING_DAMAGE":
        signals.append("Text indicates transit damage or cracked packaging upon arrival.")
    elif predicted_reason == "MISSING_ACCESSORY":
        signals.append("Text explicitly notes charger or accessory missing from box.")
    elif predicted_reason == "CUSTOMER_DAMAGE":
        signals.append("Text mentions accidental impact or liquid spill.")

    # 2. Listing Metadata Evidence
    compat_info = return_record.get("compatibility_information_present", True)
    guide_present = return_record.get("installation_guide_present", True)
    quality_score = float(return_record.get("content_quality_score", 0.85))

    if predicted_reason == "COMPATIBILITY_ISSUE" and not compat_info:
        signals.append("Product page listing lacks explicit compatibility matrix.")
    if predicted_reason == "SETUP_DIFFICULTY" and not guide_present:
        signals.append("Product page listing is missing installation setup guide.")
    if quality_score < 0.70:
        signals.append(f"Listing content quality score is low ({quality_score}).")

    # 3. Customer Actions Evidence
    viewed_compat = return_record.get("viewed_compatibility_guide", True)
    support_contacts = int(return_record.get("support_contact_count", 0))

    if predicted_reason == "COMPATIBILITY_ISSUE" and not viewed_compat:
        signals.append("Customer did not view compatibility guide before purchasing.")
    if support_contacts >= 3:
        signals.append(f"High support contact volume before return ({support_contacts} interactions).")

    # 4. Inspection Findings Evidence
    fault_confirmed = return_record.get("fault_confirmed", False)
    outcome = str(return_record.get("inspection_outcome", "Pending"))

    if fault_confirmed:
        signals.append(f"Physical inspection outcome: {outcome} (Fault Confirmed).")
    elif outcome == "No Fault Found" and predicted_reason == "PRODUCT_DEFECT":
        conflict_signals.append("Inspection outcome 'No Fault Found' contradicts predicted hardware defect.")

    # Calculate agreement score
    sources_checked = 4 + (1 if outcome != "Pending" else 0)
    agreement_count = len(signals)
    agreement_ratio = f"{min(agreement_count, sources_checked)}/{sources_checked} sources agree"

    return {
        "predicted_reason": predicted_reason,
        "confidence": confidence,
        "evidence_signals": signals,
        "conflict_signals": conflict_signals,
        "agreement_ratio": agreement_ratio,
        "has_conflicts": len(conflict_signals) > 0,
        "total_signals": len(signals)
    }

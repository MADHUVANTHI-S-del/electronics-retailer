from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class ReturnAnalysisRequest(BaseModel):
    return_id: Optional[str] = "RET-MANUAL-001"
    order_id: Optional[str] = "ORD-9999"
    customer_id: Optional[str] = "CUST-101"
    sku: str = "SKU-SMA-1001"
    product_category: Optional[str] = "Smartphones"
    return_text: str = "battery getting extremely hot and switching off"
    customer_selected_reason: Optional[str] = "battery issue"
    refund_amount: Optional[float] = 499.99
    days_since_purchase: Optional[int] = 14
    store_channel: Optional[str] = "ONLINE"
    viewed_compatibility_guide: Optional[bool] = True
    support_contact_count: Optional[int] = 1

class HumanReviewSubmission(BaseModel):
    return_id: str
    decision: str = Field(..., description="ACCEPTED, OVERRIDDEN, or ESCALATED")
    reviewer: str = "ops_manager_01"
    corrected_label: Optional[str] = None
    corrected_root_cause: Optional[str] = None
    corrected_preventable: Optional[str] = None
    corrected_priority: Optional[str] = None
    review_notes: Optional[str] = None

class PredictionResponse(BaseModel):
    return_id: str
    sku: str
    predicted_reason: str
    confidence: float
    root_cause_group: str
    preventable: str
    recommended_owner: str
    severity: str
    priority_score: float
    priority: str
    review_status: str
    evidence: Dict[str, Any]
    recommended_action: str

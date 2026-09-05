import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey
from app.database import Base

class ReturnRecord(Base):
    __tablename__ = "returns"

    id = Column(Integer, primary_key=True, index=True)
    return_id = Column(String, unique=True, index=True)
    order_id = Column(String, index=True)
    customer_id = Column(String)
    sku = Column(String, index=True)
    return_date = Column(String)
    purchase_date = Column(String)
    return_text = Column(Text)
    customer_selected_reason = Column(String)
    return_type = Column(String)
    refund_amount = Column(Float)
    quantity = Column(Integer)
    store_channel = Column(String)
    return_channel = Column(String)
    warranty_claim = Column(Boolean)
    days_since_purchase = Column(Integer)
    return_status = Column(String)
    ground_truth_reason = Column(String, nullable=True)

class ProductRecord(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, unique=True, index=True)
    product_name = Column(String)
    brand = Column(String)
    product_category = Column(String, index=True)
    subcategory = Column(String)
    model = Column(String)
    price = Column(Float)
    warranty_months = Column(Integer)
    launch_date = Column(String)
    weight = Column(Float)
    colour = Column(String)
    battery_capacity = Column(Integer)
    connector_type = Column(String)
    operating_system = Column(String)
    compatibility = Column(String)
    supplier_id = Column(String)
    packaging_type = Column(String)

class ListingRecord(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, unique=True, index=True)
    listing_title = Column(String)
    listing_description = Column(Text)
    listed_compatibility = Column(String)
    listed_accessories = Column(String)
    listed_dimensions = Column(String)
    listed_colour = Column(String)
    listing_last_updated = Column(String)
    content_quality_score = Column(Float)
    compatibility_information_present = Column(Boolean)
    installation_guide_present = Column(Boolean)
    image_accuracy_score = Column(Float)

class CustomerActionRecord(Base):
    __tablename__ = "customer_actions"

    id = Column(Integer, primary_key=True, index=True)
    return_id = Column(String, unique=True, index=True)
    viewed_product_page = Column(Boolean)
    viewed_compatibility_guide = Column(Boolean)
    viewed_size_guide = Column(Boolean)
    viewed_manual = Column(Boolean)
    contacted_support = Column(Boolean)
    support_contact_count = Column(Integer)
    attempted_troubleshooting = Column(Boolean)
    replacement_requested = Column(Boolean)
    refund_requested = Column(Boolean)
    days_before_contact = Column(Integer)
    customer_action_notes = Column(Text)

class InspectionRecord(Base):
    __tablename__ = "inspections"

    id = Column(Integer, primary_key=True, index=True)
    return_id = Column(String, unique=True, index=True)
    inspection_date = Column(String)
    inspector_id = Column(String)
    physical_damage = Column(Boolean)
    functional_test = Column(String)
    missing_accessories = Column(Boolean)
    packaging_damage = Column(Boolean)
    water_damage = Column(Boolean)
    battery_health = Column(Integer)
    compatibility_verified = Column(Boolean)
    fault_confirmed = Column(Boolean)
    inspection_notes = Column(Text)
    inspection_outcome = Column(String)

class PredictionRecord(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    return_id = Column(String, unique=True, index=True)
    predicted_reason = Column(String)
    confidence = Column(Float)
    root_cause_group = Column(String)
    preventable = Column(String)
    recommended_owner = Column(String)
    severity = Column(String)
    priority_score = Column(Float)
    priority = Column(String)
    review_status = Column(String)
    recommended_action = Column(Text)
    evidence_json = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class AlertRecord(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(String, unique=True, index=True)
    sku = Column(String, index=True)
    alert_type = Column(String)
    priority = Column(String)
    title = Column(String)
    description = Column(Text)
    evidence_json = Column(Text)
    status = Column(String, default="ACTIVE")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class ReviewRecord(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    review_id = Column(String, unique=True, index=True)
    return_id = Column(String, index=True)
    original_prediction = Column(String)
    original_confidence = Column(Float)
    human_decision = Column(String)  # ACCEPTED, OVERRIDDEN, ESCALATED
    corrected_label = Column(String, nullable=True)
    reviewer = Column(String)
    review_notes = Column(Text, nullable=True)
    review_timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class AuditLogRecord(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    entity_name = Column(String)
    entity_id = Column(String)
    action = Column(String)
    performed_by = Column(String)
    details = Column(Text)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class OperationRecord(Base):
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, unique=True, index=True)
    scenario = Column(String)
    returns_received = Column(Integer)
    staff_available = Column(Integer)
    normal_staff_capacity = Column(Integer)
    processing_capacity = Column(Integer)
    average_processing_minutes = Column(Float)
    backlog_size = Column(Integer)
    carrier_delay_hours = Column(Float)
    urgent_demand_index = Column(Float)
    inspection_capacity = Column(Integer)
    system_status = Column(String)

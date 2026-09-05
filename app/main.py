import pandas as pd
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from pathlib import Path

from app.database import engine, Base, SessionLocal
from app.models import ReturnRecord, ProductRecord, ListingRecord, CustomerActionRecord, InspectionRecord, PredictionRecord, OperationRecord
from app.routers import dashboard, returns, predictions, review, products, alerts, reports
from app.services.prediction_service import analyze_and_store_return
from app.services.alert_service import generate_sku_anomaly_alerts
from src.utils.logger import logger
from src.utils.helpers import get_project_root

app = FastAPI(
    title="Return Insight API",
    description="AI-Powered Electronics Return & Warranty Root Cause Intelligence Platform",
    version="1.0.0"
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Mount Static Files
root = get_project_root()
app.mount("/static", StaticFiles(directory=str(root / "app" / "static")), name="static")

# Include Page & API Routers
app.include_router(dashboard.router)
app.include_router(returns.router)
app.include_router(predictions.router)
app.include_router(review.router)
app.include_router(products.router)
app.include_router(alerts.router)
app.include_router(reports.router)

@app.on_event("startup")
def startup_db_seed():
    """Seeds SQLite database from cleaned master datasets on application startup if empty."""
    db = SessionLocal()
    try:
        if db.query(ReturnRecord).count() == 0:
            logger.info("Database empty. Seeding SQLite database from data/cleaned/...")

            cleaned_dir = root / "data" / "cleaned"
            master_path = cleaned_dir / "master_returns_dataset.csv"

            if master_path.exists():
                master_df = pd.read_csv(master_path)
                products_df = pd.read_csv(cleaned_dir / "products_cleaned.csv")
                listings_df = pd.read_csv(cleaned_dir / "listings_cleaned.csv")
                actions_df = pd.read_csv(cleaned_dir / "customer_actions_cleaned.csv")
                inspections_df = pd.read_csv(cleaned_dir / "inspections_cleaned.csv")
                ops_df = pd.read_csv(cleaned_dir / "operations_cleaned.csv")

                # 1. Seed Products
                for _, r in products_df.iterrows():
                    db.add(ProductRecord(
                        sku=r["sku"],
                        product_name=r["product_name"],
                        brand=r["brand"],
                        product_category=r["product_category"],
                        subcategory=r["subcategory"],
                        model=r["model"],
                        price=r["price"],
                        warranty_months=r["warranty_months"],
                        launch_date=r["launch_date"],
                        weight=r["weight"],
                        colour=r["colour"],
                        battery_capacity=r["battery_capacity"],
                        connector_type=r["connector_type"],
                        operating_system=r["operating_system"],
                        compatibility=r["compatibility"],
                        supplier_id=r["supplier_id"],
                        packaging_type=r["packaging_type"]
                    ))

                # 2. Seed Listings
                for _, r in listings_df.iterrows():
                    db.add(ListingRecord(
                        sku=r["sku"],
                        listing_title=r["listing_title"],
                        listing_description=r["listing_description"],
                        listed_compatibility=r["listed_compatibility"],
                        listed_accessories=r["listed_accessories"],
                        listed_dimensions=r["listed_dimensions"],
                        listed_colour=r["listed_colour"],
                        listing_last_updated=r["listing_last_updated"],
                        content_quality_score=r["content_quality_score"],
                        compatibility_information_present=bool(r["compatibility_information_present"]),
                        installation_guide_present=bool(r["installation_guide_present"]),
                        image_accuracy_score=r["image_accuracy_score"]
                    ))

                # 3. Seed Operations
                for _, r in ops_df.iterrows():
                    db.add(OperationRecord(
                        date=r["date"],
                        scenario=r["scenario"],
                        returns_received=r["returns_received"],
                        staff_available=r["staff_available"],
                        normal_staff_capacity=r["normal_staff_capacity"],
                        processing_capacity=r["processing_capacity"],
                        average_processing_minutes=r["average_processing_minutes"],
                        backlog_size=r["backlog_size"],
                        carrier_delay_hours=r["carrier_delay_hours"],
                        urgent_demand_index=r["urgent_demand_index"],
                        inspection_capacity=r["inspection_capacity"],
                        system_status=r["system_status"]
                    ))

                # 4. Seed Returns & run prediction engine for top 1000 sample records
                sample_returns = master_df.head(1000)
                for _, r in sample_returns.iterrows():
                    ret_rec = ReturnRecord(
                        return_id=r["return_id"],
                        order_id=r["order_id"],
                        customer_id=r["customer_id"],
                        sku=r["sku"],
                        return_date=r["return_date"],
                        purchase_date=r["purchase_date"],
                        return_text=r["return_text"],
                        customer_selected_reason=r["customer_selected_reason"],
                        return_type=r["return_type"],
                        refund_amount=r["refund_amount"],
                        quantity=r["quantity"],
                        store_channel=r["store_channel"],
                        return_channel=r["return_channel"],
                        warranty_claim=r["warranty_claim"],
                        days_since_purchase=r["days_since_purchase"],
                        return_status=r["return_status"],
                        ground_truth_reason=r["ground_truth_reason"]
                    )
                    db.add(ret_rec)

                    # Run prediction & store
                    analyze_and_store_return(db, r.to_dict())

                db.commit()

                # Generate SKU anomaly alerts
                generate_sku_anomaly_alerts(db, master_df)
                logger.info("Database seeding complete!")
    finally:
        db.close()

@app.get("/api/health")
def health_check():
    """API health status endpoint."""
    return {"status": "HEALTHY", "application": "Return Insight", "version": "1.0.0"}

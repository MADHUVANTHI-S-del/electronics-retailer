from sqlalchemy.orm import Session
from app.models import AlertRecord, PredictionRecord, ReturnRecord
from src.models.anomaly_detector import SKUAnomalyDetector
import pandas as pd

def get_active_alerts(db: Session):
    """Returns active alerts from database."""
    return db.query(AlertRecord).filter(AlertRecord.status == "ACTIVE").all()

def generate_sku_anomaly_alerts(db: Session, master_df: pd.DataFrame):
    """Runs anomaly detector and populates AlertRecord table."""
    detector = SKUAnomalyDetector()
    anomalies = detector.detect_sku_anomalies(master_df)

    for idx, row in anomalies.iterrows():
        sku = row["sku"]
        existing = db.query(AlertRecord).filter(AlertRecord.sku == sku).first()
        if not existing:
            title = f"High Return Volume Spike: {row['product_name']}"
            desc = (
                f"SKU {sku} experienced {int(row['total_returns'])} returns "
                f"(baseline: {row['historical_baseline']}). Dominant reason: {row['dominant_reason']}."
            )
            alert = AlertRecord(
                alert_id=f"ALT-SKU-{sku}",
                sku=sku,
                alert_type="SKU_RETURN_SPIKE",
                priority="P1" if row["z_score"] > 3.0 else "P2",
                title=title,
                description=desc,
                evidence_json=str({"z_score": round(float(row["z_score"]), 2), "total_returns": int(row["total_returns"])}),
                status="ACTIVE"
            )
            db.add(alert)
    db.commit()

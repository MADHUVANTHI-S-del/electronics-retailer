import pandas as pd
from typing import Dict, List, Tuple
from src.utils.logger import logger

REQUIRED_SCHEMAS = {
    "returns_raw": [
        "return_id", "order_id", "customer_id", "sku", "return_date", "purchase_date",
        "return_text", "customer_selected_reason"
    ],
    "products_raw": ["sku", "product_name", "brand", "product_category", "price"],
    "listings_raw": ["sku", "listing_title", "content_quality_score"],
    "customer_actions_raw": ["return_id", "viewed_product_page"],
    "inspections_raw": ["return_id", "inspection_outcome"],
    "operations_raw": ["date", "scenario", "returns_received"]
}

def validate_dataset_schema(df: pd.DataFrame, dataset_name: str) -> Tuple[bool, List[str]]:
    """Validates that a DataFrame contains all required columns."""
    if dataset_name not in REQUIRED_SCHEMAS:
        return True, []
    
    missing = [col for col in REQUIRED_SCHEMAS[dataset_name] if col not in df.columns]
    if missing:
        logger.error(f"Dataset {dataset_name} missing required columns: {missing}")
        return False, missing
    return True, []

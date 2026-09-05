from typing import Tuple

PREVENTABILITY_MAP = {
    "PRODUCT_DEFECT": ("YES", "Product Team"),
    "SHIPPING_DAMAGE": ("YES", "Logistics"),
    "PACKAGING_ISSUE": ("YES", "Warehouse"),
    "MISSING_ACCESSORY": ("YES", "Supplier"),
    "LISTING_MISMATCH": ("YES", "Content Team"),
    "COMPATIBILITY_ISSUE": ("YES", "Content Team"),
    "SETUP_DIFFICULTY": ("YES", "Customer Support"),
    "CUSTOMER_ORDER_ERROR": ("NO", "Customer"),
    "CUSTOMER_DAMAGE": ("NO", "Customer"),
    "PERFORMANCE_EXPECTATION": ("YES", "Content Team"),
    "WARRANTY_FAILURE": ("YES", "Product Team"),
    "NO_FAULT_FOUND": ("UNCERTAIN", "Customer Support"),
    "OTHER": ("UNCERTAIN", "Unknown")
}

def determine_preventability(reason: str) -> Tuple[str, str]:
    """Returns (preventable_status, recommended_owner) based on return reason."""
    return PREVENTABILITY_MAP.get(reason, ("UNCERTAIN", "Unknown"))

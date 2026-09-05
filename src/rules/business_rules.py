from typing import Tuple

ROOT_CAUSE_MAP = {
    "PRODUCT_DEFECT": ("PRODUCT", "Product Team"),
    "SHIPPING_DAMAGE": ("LOGISTICS", "Logistics"),
    "PACKAGING_ISSUE": ("LOGISTICS", "Warehouse"),
    "MISSING_ACCESSORY": ("PRODUCT", "Supplier"),
    "LISTING_MISMATCH": ("CONTENT", "Content Team"),
    "COMPATIBILITY_ISSUE": ("CONTENT", "Content Team"),
    "SETUP_DIFFICULTY": ("CONTENT", "Customer Support"),
    "CUSTOMER_ORDER_ERROR": ("CUSTOMER", "Customer"),
    "CUSTOMER_DAMAGE": ("CUSTOMER", "Customer"),
    "PERFORMANCE_EXPECTATION": ("CONTENT", "Content Team"),
    "WARRANTY_FAILURE": ("PRODUCT", "Product Team"),
    "NO_FAULT_FOUND": ("OPERATIONS", "Customer Support"),
    "OTHER": ("UNKNOWN", "Unknown")
}

def get_root_cause_and_owner(reason: str) -> Tuple[str, str]:
    """Maps return reason to (root_cause_group, recommended_owner)."""
    return ROOT_CAUSE_MAP.get(reason, ("UNKNOWN", "Unknown"))

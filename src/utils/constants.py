"""
Constants used across Return Insight platform.
"""

RETURN_REASONS = [
    "PRODUCT_DEFECT",
    "SHIPPING_DAMAGE",
    "PACKAGING_ISSUE",
    "MISSING_ACCESSORY",
    "LISTING_MISMATCH",
    "COMPATIBILITY_ISSUE",
    "SETUP_DIFFICULTY",
    "CUSTOMER_ORDER_ERROR",
    "CUSTOMER_DAMAGE",
    "PERFORMANCE_EXPECTATION",
    "WARRANTY_FAILURE",
    "NO_FAULT_FOUND",
    "OTHER",
]

ROOT_CAUSE_GROUPS = [
    "PRODUCT",
    "CONTENT",
    "LOGISTICS",
    "CUSTOMER",
    "OPERATIONS",
    "UNKNOWN",
]

PREVENTABLE_VALUES = ["YES", "NO", "UNCERTAIN"]

PREVENTABLE_OWNERS = [
    "Product Team",
    "Content Team",
    "Supplier",
    "Warehouse",
    "Logistics",
    "Customer Support",
    "Customer",
    "Unknown",
]

SEVERITIES = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]

PRIORITIES = ["P1", "P2", "P3", "P4"]

OPERATIONAL_SCENARIOS = [
    "NORMAL",
    "DELIVERY_DELAY",
    "CAPACITY_LOSS",
    "URGENT_DEMAND",
]

PRODUCT_CATEGORIES = [
    "Smartphones",
    "Laptops",
    "Headphones",
    "Smartwatches",
    "Chargers",
    "Power Banks",
    "TVs",
    "Tablets",
    "Cameras",
    "Keyboards",
    "Mice",
    "Speakers",
    "Cables",
    "Routers",
    "Gaming Accessories",
]

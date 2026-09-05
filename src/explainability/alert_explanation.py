from typing import Dict, Any

def generate_alert_explanation(alert_data: Dict[str, Any]) -> str:
    """Formats an executive natural language explanation for high-priority operational alerts."""
    sku = alert_data.get("sku", "N/A")
    product = alert_data.get("product_name", "Product")
    reason = alert_data.get("dominant_reason", "PRODUCT_DEFECT")
    owner = alert_data.get("recommended_owner", "Product Team")
    vol = alert_data.get("current_volume", 0)
    baseline = alert_data.get("historical_baseline", 0)

    explanation = (
        f"HIGH PRIORITY ALERT for SKU {sku} ({product}): "
        f"Current return volume is {vol} units vs baseline of {baseline} units. "
        f"Dominant predicted root cause: {reason}. "
        f"Assigned owner: {owner}. Recommended immediate action: Inspect product batch & update listing."
    )
    return explanation

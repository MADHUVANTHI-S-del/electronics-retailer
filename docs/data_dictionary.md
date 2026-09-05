# Data Dictionary — RETURN INSIGHT

## 1. Returns Raw Dataset (`returns_raw.csv`)
- `return_id` (string): Unique return identifier (e.g. `RET-100001`).
- `order_id` (string): Original purchase order ID.
- `customer_id` (string): Customer account ID.
- `sku` (string): Stock Keeping Unit identifier.
- `return_date` (string): Date return was initiated (ISO / MM/DD/YYYY formats).
- `purchase_date` (string): Date item was purchased.
- `return_text` (string): Customer free-text return reason.
- `customer_selected_reason` (string): Category chosen by customer in portal.
- `return_type` (string): `STANDARD_RETURN` or `WARRANTY`.
- `refund_amount` (float): Total monetary value refunded.
- `quantity` (int): Quantity of items returned.
- `store_channel` (string): `ONLINE`, `RETAIL_STORE`, `MARKETPLACE`.
- `return_channel` (string): `MAIL`, `IN_STORE_DROP`, `LOCKER`.
- `warranty_claim` (boolean): Flag indicating whether return is under warranty.
- `days_since_purchase` (int): Number of days between purchase and return initiation.
- `return_status` (string): `PROCESSED`, `PENDING_INSPECTION`, `APPROVED`, `REJECTED`.
- `ground_truth_reason` (string): Primary ground-truth label for evaluation.

## 2. Products Raw Dataset (`products_raw.csv`)
- `sku` (string): SKU key.
- `product_name` (string): Commercial product name.
- `brand` (string): Brand name.
- `product_category` (string): Category (Smartphones, Laptops, Headphones, etc.).
- `price` (float): Retail selling price.
- `warranty_months` (int): Manufacturer warranty duration in months.

## 3. Listings Raw Dataset (`listings_raw.csv`)
- `sku` (string): SKU key.
- `content_quality_score` (float): Content quality index (0.0 - 1.0).
- `compatibility_information_present` (boolean): Whether compatibility details are present.
- `installation_guide_present` (boolean): Whether setup guide is present.
- `image_accuracy_score` (float): Image accuracy index (0.0 - 1.0).

## 4. Customer Actions Dataset (`customer_actions_raw.csv`)
- `return_id` (string): Return key.
- `viewed_compatibility_guide` (boolean): Whether customer viewed compatibility guide before purchasing.
- `support_contact_count` (int): Number of support contacts before return.

## 5. Inspections Dataset (`inspections_raw.csv`)
- `return_id` (string): Return key.
- `physical_damage` (boolean): Physical damage detected during inspection.
- `fault_confirmed` (boolean): Hardware fault confirmed during testing.
- `inspection_outcome` (string): `Confirmed Defect`, `No Fault Found`, `Customer Damage`, etc.

## 6. Operations Dataset (`operations_raw.csv`)
- `date` (string): Log date.
- `scenario` (string): `NORMAL`, `CAPACITY_LOSS`, `DELIVERY_DELAY`, `URGENT_DEMAND`.
- `processing_capacity` (int): Daily case processing limit.
- `backlog_size` (int): Return queue backlog count.

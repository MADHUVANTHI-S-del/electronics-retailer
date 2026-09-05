import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
from src.utils.logger import logger
from src.utils.helpers import get_project_root
from src.utils.constants import PRODUCT_CATEGORIES, RETURN_REASONS, OPERATIONAL_SCENARIOS

RANDOM_SEED = 42

def set_seeds(seed=RANDOM_SEED):
    random.seed(seed)
    np.random.seed(seed)

def generate_products(num_products=150) -> pd.DataFrame:
    """Generates synthetic product metadata across 15 categories."""
    set_seeds()
    brands = ["AeroTech", "SonicWave", "VoltMax", "PixelCraft", "NexusCore", "OmniGear", "UltraLink", "Zenith"]
    suppliers = [f"SUP-{100 + i}" for i in range(15)]
    packaging_types = ["Box", "Blister Pack", "Pouch", "Eco Carton", "Reinforced Case"]

    products = []
    for i in range(1, num_products + 1):
        cat = PRODUCT_CATEGORIES[(i - 1) % len(PRODUCT_CATEGORIES)]
        sku = f"SKU-{cat[:3].upper()}-{1000 + i}"
        brand = random.choice(brands)
        price = round(random.uniform(15.0, 1200.0), 2)
        warranty = random.choice([6, 12, 24, 36])
        launch_date = (datetime(2023, 1, 1) + timedelta(days=random.randint(0, 500))).strftime("%Y-%m-%d")

        # Category specific properties
        os_type = "Android" if cat in ["Smartphones", "Tablets"] and random.random() > 0.4 else ("iOS" if cat in ["Smartphones", "Tablets"] else "N/A")
        batt = random.choice([2000, 4000, 5000, 10000]) if cat in ["Smartphones", "Laptops", "Headphones", "Power Banks", "Smartwatches", "Tablets", "Speakers"] else 0
        conn = random.choice(["USB-C", "Lightning", "Micro-USB", "Bluetooth", "HDMI", "3.5mm Jack"])

        products.append({
            "sku": sku,
            "product_name": f"{brand} {cat[:-1] if cat.endswith('s') else cat} {100 + i}",
            "brand": brand,
            "product_category": cat,
            "subcategory": f"{cat} Standard",
            "model": f"MOD-{2000 + i}",
            "price": price,
            "warranty_months": warranty,
            "launch_date": launch_date,
            "weight": round(random.uniform(0.1, 5.0), 2),
            "colour": random.choice(["Midnight Black", "Silver", "Space Gray", "Ocean Blue", "White"]),
            "battery_capacity": batt,
            "connector_type": conn,
            "operating_system": os_type,
            "compatibility": "Universal" if conn == "USB-C" else ("iOS/Android" if conn == "Bluetooth" else "Specific"),
            "supplier_id": random.choice(suppliers),
            "packaging_type": random.choice(packaging_types)
        })
    df = pd.DataFrame(products)
    logger.info(f"Generated {len(df)} products.")
    return df

def generate_listings(products_df: pd.DataFrame) -> pd.DataFrame:
    """Generates listing metadata with intentional errors for testing listing mismatch & compatibility issues."""
    set_seeds()
    listings = []
    for idx, row in products_df.iterrows():
        sku = row["sku"]
        # Introduce intentional errors for ~20% of listings
        has_flaw = random.random() < 0.20
        flaw_type = random.choice(["wrong_conn", "missing_compat", "exaggerated_batt", "missing_guide"]) if has_flaw else "none"

        quality_score = round(random.uniform(0.3, 0.6), 2) if has_flaw else round(random.uniform(0.8, 1.0), 2)
        compat_info = False if flaw_type == "missing_compat" else (random.random() > 0.15)
        guide_present = False if flaw_type == "missing_guide" else (random.random() > 0.20)
        img_score = round(random.uniform(0.4, 0.7), 2) if has_flaw else round(random.uniform(0.85, 1.0), 2)

        listed_conn = "Micro USB" if flaw_type == "wrong_conn" and row["connector_type"] == "USB-C" else row["connector_type"]

        listings.append({
            "sku": sku,
            "listing_title": f"{row['product_name']} - High Performance",
            "listing_description": f"Official {row['brand']} {row['product_category']} with {listed_conn} support.",
            "listed_compatibility": "iOS and Android" if compat_info else "See Description",
            "listed_accessories": "Charger, User Manual, Cable" if flaw_type != "missing_guide" else "Device Only",
            "listed_dimensions": f"{random.randint(10, 30)}x{random.randint(5, 15)}x{random.randint(1, 5)} cm",
            "listed_colour": row["colour"],
            "listing_last_updated": (datetime(2024, 1, 1) + timedelta(days=random.randint(0, 180))).strftime("%Y-%m-%d"),
            "content_quality_score": quality_score,
            "compatibility_information_present": compat_info,
            "installation_guide_present": guide_present,
            "image_accuracy_score": img_score
        })
    df = pd.DataFrame(listings)
    logger.info(f"Generated {len(df)} listings.")
    return df

def generate_operations(num_days=365) -> pd.DataFrame:
    """Generates daily operational logs across 4 operational scenarios."""
    set_seeds()
    ops = []
    start_date = datetime(2025, 1, 1)
    scenarios = ["NORMAL", "DELIVERY_DELAY", "CAPACITY_LOSS", "URGENT_DEMAND"]
    weights = [0.70, 0.10, 0.10, 0.10]

    for d in range(num_days):
        current_date = (start_date + timedelta(days=d)).strftime("%Y-%m-%d")
        scen = random.choices(scenarios, weights=weights)[0]

        if scen == "NORMAL":
            returns_cnt = random.randint(30, 60)
            staff = random.randint(25, 30)
            cap = 60
            proc_min = random.randint(12, 18)
            backlog = random.randint(5, 20)
            delay = round(random.uniform(0.5, 2.0), 1)
        elif scen == "CAPACITY_LOSS":
            returns_cnt = random.randint(40, 70)
            staff = random.randint(12, 18)
            cap = 35
            proc_min = random.randint(25, 40)
            backlog = random.randint(40, 100)
            delay = round(random.uniform(1.0, 4.0), 1)
        elif scen == "DELIVERY_DELAY":
            returns_cnt = random.randint(50, 80)
            staff = random.randint(25, 30)
            cap = 60
            proc_min = random.randint(15, 22)
            backlog = random.randint(20, 50)
            delay = round(random.uniform(12.0, 48.0), 1)
        else: # URGENT_DEMAND
            returns_cnt = random.randint(90, 150)
            staff = random.randint(28, 32)
            cap = 70
            proc_min = random.randint(20, 30)
            backlog = random.randint(60, 130)
            delay = round(random.uniform(2.0, 8.0), 1)

        ops.append({
            "date": current_date,
            "scenario": scen,
            "returns_received": returns_cnt,
            "staff_available": staff,
            "normal_staff_capacity": 30,
            "processing_capacity": cap,
            "average_processing_minutes": proc_min,
            "backlog_size": backlog,
            "carrier_delay_hours": delay,
            "urgent_demand_index": round(random.uniform(1.0, 2.5), 2) if scen == "URGENT_DEMAND" else 1.0,
            "inspection_capacity": cap,
            "system_status": "DEGRADED" if scen in ["CAPACITY_LOSS", "DELIVERY_DELAY"] else "HEALTHY"
        })
    df = pd.DataFrame(ops)
    logger.info(f"Generated {len(df)} operational days.")
    return df

TEXT_PATTERNS = {
    "PRODUCT_DEFECT": [
        "battery draining very fast", "device stopped turning on after two weeks", "product overheating during charging",
        "screen keeps flickering", "speaker produces loud static noise", "left earbud stopped working",
        "power button got stuck", "motherboard short circuited", "wifi drops connection constantly"
    ],
    "SHIPPING_DAMAGE": [
        "screen arrived cracked", "box damaged but product works", "outer carton crushed during transit",
        "dented casing upon opening package", "glass back panel shattered in delivery"
    ],
    "PACKAGING_ISSUE": [
        "packaging torn open", "seal was broken on delivery box", "box arrived soaked in rain",
        "internal plastic tray smashed"
    ],
    "MISSING_ACCESSORY": [
        "charger missing from box", "expected USB C cable but not included", "manual missing from package",
        "power adapter absent from sealed box", "mounting screws missing"
    ],
    "LISTING_MISMATCH": [
        "product does not match description", "camera quality is not as advertised", "expected USB C but received micro USB",
        "colour received is red not blue as listed", "received wrong model version"
    ],
    "COMPATIBILITY_ISSUE": [
        "headphones won't connect to my laptop", "not compatible with iPhone", "wrong size cable",
        "router does not support mesh network", "keyboard won't pair with Mac OS"
    ],
    "SETUP_DIFFICULTY": [
        "manual didn't explain installation", "bluetooth disconnecting every few minutes", "cannot get software setup to complete",
        "confusing setup steps device won't pair"
    ],
    "CUSTOMER_ORDER_ERROR": [
        "customer accidentally ordered wrong model", "ordered wrong size by mistake", "bought wrong connector version",
        "realized I don't need this item"
    ],
    "CUSTOMER_DAMAGE": [
        "dropped phone on tile floor screen cracked", "spilled coffee on keyboard", "submerged non-waterproof speaker",
        "bent charging pin by forcing cable"
    ],
    "PERFORMANCE_EXPECTATION": [
        "sound quality not as good as expected", "battery life shorter than I hoped", "screen brightness too low for outdoor use",
        "camera photos look grainy in low light"
    ],
    "WARRANTY_FAILURE": [
        "stopped working after 8 months under warranty", "battery expanded after 10 months", "charging port loose after half year",
        "display lines appeared after 5 months"
    ],
    "NO_FAULT_FOUND": [
        "returned because changed mind works fine", "no issue found works as expected", "tested fine customer didn't like color",
        "works perfectly on test bench"
    ],
    "OTHER": [
        "not satisfied", "bad product", "not working", "doesn't fit", "just return it"
    ]
}

def generate_returns(products_df: pd.DataFrame, num_returns=12000) -> tuple:
    """Generates returns_raw, customer_actions_raw, inspections_raw, and ground truth metadata."""
    set_seeds()
    skus = products_df["sku"].tolist()
    sku_to_cat = dict(zip(products_df["sku"], products_df["product_category"]))
    sku_to_price = dict(zip(products_df["sku"], products_df["price"]))

    reasons_list = RETURN_REASONS
    reason_weights = [0.22, 0.08, 0.04, 0.06, 0.12, 0.12, 0.08, 0.06, 0.05, 0.06, 0.05, 0.04, 0.02]

    returns = []
    actions = []
    inspections = []

    start_date = datetime(2025, 1, 1)

    for i in range(1, num_returns + 1):
        ret_id = f"RET-{100000 + i}"
        ord_id = f"ORD-{500000 + random.randint(1, 80000)}"
        cust_id = f"CUST-{90000 + random.randint(1, 50000)}"

        sku = random.choice(skus)
        price = sku_to_price[sku]
        days_since = random.randint(1, 365)
        ret_date_dt = start_date + timedelta(days=days_since)
        purch_date_dt = ret_date_dt - timedelta(days=random.randint(2, 30))

        # Date string formatting with intentional data quality noise
        ret_date_str = ret_date_dt.strftime("%Y-%m-%d") if random.random() > 0.05 else ret_date_dt.strftime("%m/%d/%Y")
        purch_date_str = purch_date_dt.strftime("%Y-%m-%d")

        gt_reason = random.choices(reasons_list, weights=reason_weights)[0]

        # Return text generation with noisy variants
        base_text = random.choice(TEXT_PATTERNS[gt_reason])
        
        # Introduce noise (typos, casing, punctuation)
        if random.random() < 0.15:
            base_text = base_text.upper()
        elif random.random() < 0.15:
            base_text = base_text.title()
        
        if random.random() < 0.08:
            base_text = base_text.replace("e", "3").replace("a", "4") # typo / slang
        if random.random() < 0.05:
            base_text = "   " + base_text + "   " # whitespace noise

        # Customer selected reason (sometimes inaccurate vs ground truth)
        cust_selected = gt_reason if random.random() > 0.25 else random.choice(reasons_list)

        qty = 1 if random.random() > 0.05 else 2
        refund_amt = round(price * qty, 2)
        warranty_claim = (gt_reason == "WARRANTY_FAILURE") or (days_since > 30 and random.random() < 0.3)

        returns.append({
            "return_id": ret_id,
            "order_id": ord_id,
            "customer_id": cust_id,
            "sku": sku,
            "return_date": ret_date_str,
            "purchase_date": purch_date_str,
            "return_text": base_text,
            "customer_selected_reason": cust_selected,
            "return_type": "WARRANTY" if warranty_claim else "STANDARD_RETURN",
            "refund_amount": refund_amt,
            "quantity": qty,
            "store_channel": random.choice(["ONLINE", "RETAIL_STORE", "MARKETPLACE"]),
            "return_channel": random.choice(["MAIL", "IN_STORE_DROP", "LOCKER"]),
            "warranty_claim": warranty_claim,
            "days_since_purchase": (ret_date_dt - purch_date_dt).days,
            "return_status": random.choice(["PROCESSED", "PENDING_INSPECTION", "APPROVED", "REJECTED"]),

            # Ground truth fields embedded for evaluation pipeline
            "ground_truth_reason": gt_reason,
            "root_cause_group": "PRODUCT" if gt_reason in ["PRODUCT_DEFECT", "WARRANTY_FAILURE", "MISSING_ACCESSORY"] else (
                "CONTENT" if gt_reason in ["LISTING_MISMATCH", "COMPATIBILITY_ISSUE", "SETUP_DIFFICULTY", "PERFORMANCE_EXPECTATION"] else (
                    "LOGISTICS" if gt_reason in ["SHIPPING_DAMAGE", "PACKAGING_ISSUE"] else (
                        "CUSTOMER" if gt_reason in ["CUSTOMER_ORDER_ERROR", "CUSTOMER_DAMAGE"] else (
                            "OPERATIONS" if gt_reason == "NO_FAULT_FOUND" else "UNKNOWN"
                        )
                    )
                )
            ),
            "preventable": "NO" if gt_reason in ["CUSTOMER_DAMAGE", "CUSTOMER_ORDER_ERROR"] else ("UNCERTAIN" if gt_reason == "NO_FAULT_FOUND" else "YES"),
            "preventable_owner": "Product Team" if gt_reason in ["PRODUCT_DEFECT", "WARRANTY_FAILURE"] else (
                "Content Team" if gt_reason in ["LISTING_MISMATCH", "COMPATIBILITY_ISSUE", "PERFORMANCE_EXPECTATION"] else (
                    "Logistics" if gt_reason == "SHIPPING_DAMAGE" else (
                        "Warehouse" if gt_reason == "PACKAGING_ISSUE" else (
                            "Supplier" if gt_reason == "MISSING_ACCESSORY" else (
                                "Customer Support" if gt_reason == "SETUP_DIFFICULTY" else "Customer"
                            )
                        )
                    )
                )
            ),
            "severity": "CRITICAL" if gt_reason == "PRODUCT_DEFECT" and price > 500 else (
                "HIGH" if gt_reason in ["PRODUCT_DEFECT", "WARRANTY_FAILURE", "LISTING_MISMATCH"] else (
                    "MEDIUM" if gt_reason in ["SHIPPING_DAMAGE", "COMPATIBILITY_ISSUE", "MISSING_ACCESSORY"] else "LOW"
                )
            ),
            "ground_truth_priority": "P1" if gt_reason in ["PRODUCT_DEFECT", "WARRANTY_FAILURE"] and price > 400 else (
                "P2" if gt_reason in ["LISTING_MISMATCH", "COMPATIBILITY_ISSUE", "SHIPPING_DAMAGE"] else (
                    "P3" if gt_reason in ["MISSING_ACCESSORY", "SETUP_DIFFICULTY"] else "P4"
                )
            )
        })

        # Customer Actions
        actions.append({
            "return_id": ret_id,
            "viewed_product_page": True,
            "viewed_compatibility_guide": False if gt_reason == "COMPATIBILITY_ISSUE" else random.choice([True, False]),
            "viewed_size_guide": random.choice([True, False]),
            "viewed_manual": False if gt_reason == "SETUP_DIFFICULTY" else random.choice([True, False]),
            "contacted_support": True if gt_reason in ["SETUP_DIFFICULTY", "WARRANTY_FAILURE"] else (random.random() > 0.5),
            "support_contact_count": random.randint(2, 5) if gt_reason == "SETUP_DIFFICULTY" else random.randint(0, 2),
            "attempted_troubleshooting": False if gt_reason in ["SETUP_DIFFICULTY", "CUSTOMER_ORDER_ERROR"] else (random.random() > 0.4),
            "replacement_requested": gt_reason in ["PRODUCT_DEFECT", "SHIPPING_DAMAGE", "MISSING_ACCESSORY"],
            "refund_requested": gt_reason not in ["PRODUCT_DEFECT", "SHIPPING_DAMAGE"],
            "days_before_contact": random.randint(0, 10),
            "customer_action_notes": f"Customer initiated return for {gt_reason}"
        })

        # Inspection Dataset
        phys_dmg = gt_reason in ["SHIPPING_DAMAGE", "CUSTOMER_DAMAGE"]
        func_fail = gt_reason in ["PRODUCT_DEFECT", "WARRANTY_FAILURE"]
        missing_acc = gt_reason == "MISSING_ACCESSORY"
        pkg_dmg = gt_reason in ["SHIPPING_DAMAGE", "PACKAGING_ISSUE"]
        batt_health = random.randint(20, 50) if gt_reason == "PRODUCT_DEFECT" and "battery" in base_text.lower() else random.randint(85, 100)

        if func_fail:
            outcome = "Confirmed Defect"
        elif gt_reason == "NO_FAULT_FOUND":
            outcome = "No Fault Found"
        elif gt_reason == "CUSTOMER_DAMAGE":
            outcome = "Customer Damage"
        elif missing_acc:
            outcome = "Missing Accessory"
        elif gt_reason == "SHIPPING_DAMAGE":
            outcome = "Shipping Damage"
        elif gt_reason == "COMPATIBILITY_ISSUE":
            outcome = "Compatibility Issue"
        else:
            outcome = "Unable to Reproduce" if random.random() < 0.3 else "No Fault Found"

        inspections.append({
            "return_id": ret_id,
            "inspection_date": (ret_date_dt + timedelta(days=random.randint(1, 3))).strftime("%Y-%m-%d"),
            "inspector_id": f"INSP-{10 + random.randint(1, 10)}",
            "physical_damage": phys_dmg,
            "functional_test": "FAILED" if func_fail else "PASSED",
            "missing_accessories": missing_acc,
            "packaging_damage": pkg_dmg,
            "water_damage": gt_reason == "CUSTOMER_DAMAGE" and "coffee" in base_text.lower(),
            "battery_health": batt_health,
            "compatibility_verified": not (gt_reason == "COMPATIBILITY_ISSUE"),
            "fault_confirmed": func_fail or phys_dmg or missing_acc,
            "inspection_notes": f"Inspection completed. Outcome: {outcome}",
            "inspection_outcome": outcome
        })

    returns_df = pd.DataFrame(returns)
    actions_df = pd.DataFrame(actions)
    inspections_df = pd.DataFrame(inspections)

    # Introduce duplicate rows (~0.5%) for raw data cleaning test
    dup_rows = returns_df.iloc[:60].copy()
    returns_df = pd.concat([returns_df, dup_rows], ignore_index=True)

    logger.info(f"Generated {len(returns_df)} return records.")
    return returns_df, actions_df, inspections_df

def generate_all():
    """Master generator script to write all 6 raw CSV files."""
    root = get_project_root()
    raw_dir = root / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    products_df = generate_products()
    products_df.to_csv(raw_dir / "products_raw.csv", index=False)

    listings_df = generate_listings(products_df)
    listings_df.to_csv(raw_dir / "listings_raw.csv", index=False)

    ops_df = generate_operations()
    ops_df.to_csv(raw_dir / "operations_raw.csv", index=False)

    returns_df, actions_df, inspections_df = generate_returns(products_df)
    returns_df.to_csv(raw_dir / "returns_raw.csv", index=False)
    actions_df.to_csv(raw_dir / "customer_actions_raw.csv", index=False)
    inspections_df.to_csv(raw_dir / "inspections_raw.csv", index=False)

    logger.info("All raw synthetic datasets successfully generated in data/raw/")

if __name__ == "__main__":
    generate_all()

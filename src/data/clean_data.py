import os
import pandas as pd
import numpy as np
from pathlib import Path
from src.utils.logger import logger
from src.utils.helpers import get_project_root

def clean_returns_df(df: pd.DataFrame) -> tuple:
    """Cleans returns raw dataframe."""
    initial_rows = len(df)
    
    # 1. Remove duplicate return_ids
    df = df.drop_duplicates(subset=["return_id"], keep="first").copy()
    dups_removed = initial_rows - len(df)

    # 2. Clean return text: whitespace, lowercase, handle missing
    df["return_text"] = df["return_text"].astype(str).str.strip().str.lower()
    df["return_text"] = df["return_text"].replace(["nan", "none", ""], "no reason provided")

    # 3. Standardize dates to YYYY-MM-DD
    df["return_date"] = pd.to_datetime(df["return_date"], errors="coerce").dt.strftime("%Y-%m-%d")
    df["purchase_date"] = pd.to_datetime(df["purchase_date"], errors="coerce").dt.strftime("%Y-%m-%d")

    # Fill invalid date values with default
    df["return_date"] = df["return_date"].fillna("2025-01-01")
    df["purchase_date"] = df["purchase_date"].fillna("2024-12-15")

    # 4. Fill numeric & categoricals
    df["refund_amount"] = pd.to_numeric(df["refund_amount"], errors="coerce").fillna(0.0)
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(1).astype(int)
    df["days_since_purchase"] = pd.to_numeric(df["days_since_purchase"], errors="coerce").fillna(7).astype(int)

    summary = {
        "dataset": "returns",
        "initial_rows": initial_rows,
        "final_rows": len(df),
        "duplicates_removed": dups_removed
    }
    return df, summary

def clean_products_df(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans products raw dataframe."""
    df = df.drop_duplicates(subset=["sku"]).copy()
    df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0.0)
    df["warranty_months"] = pd.to_numeric(df["warranty_months"], errors="coerce").fillna(12).astype(int)
    return df

def clean_listings_df(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans listings raw dataframe."""
    df = df.drop_duplicates(subset=["sku"]).copy()
    df["content_quality_score"] = pd.to_numeric(df["content_quality_score"], errors="coerce").fillna(0.8)
    df["image_accuracy_score"] = pd.to_numeric(df["image_accuracy_score"], errors="coerce").fillna(0.85)
    return df

def clean_customer_actions_df(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans customer actions dataframe."""
    df = df.drop_duplicates(subset=["return_id"]).copy()
    df["support_contact_count"] = pd.to_numeric(df["support_contact_count"], errors="coerce").fillna(0).astype(int)
    return df

def clean_inspections_df(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans inspections dataframe."""
    df = df.drop_duplicates(subset=["return_id"]).copy()
    df["battery_health"] = pd.to_numeric(df["battery_health"], errors="coerce").fillna(100).astype(int)
    return df

def clean_operations_df(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans operations dataframe."""
    df = df.drop_duplicates(subset=["date"]).copy()
    return df

def clean_all():
    """Main execution function for data cleaning pipeline."""
    root = get_project_root()
    raw_dir = root / "data" / "raw"
    cleaned_dir = root / "data" / "cleaned"
    cleaned_dir.mkdir(parents=True, exist_ok=True)

    returns_raw = pd.read_csv(raw_dir / "returns_raw.csv")
    products_raw = pd.read_csv(raw_dir / "products_raw.csv")
    listings_raw = pd.read_csv(raw_dir / "listings_raw.csv")
    actions_raw = pd.read_csv(raw_dir / "customer_actions_raw.csv")
    inspections_raw = pd.read_csv(raw_dir / "inspections_raw.csv")
    ops_raw = pd.read_csv(raw_dir / "operations_raw.csv")

    returns_cleaned, summary = clean_returns_df(returns_raw)
    products_cleaned = clean_products_df(products_raw)
    listings_cleaned = clean_listings_df(listings_raw)
    actions_cleaned = clean_customer_actions_df(actions_raw)
    inspections_cleaned = clean_inspections_df(inspections_raw)
    ops_cleaned = clean_operations_df(ops_raw)

    returns_cleaned.to_csv(cleaned_dir / "returns_cleaned.csv", index=False)
    products_cleaned.to_csv(cleaned_dir / "products_cleaned.csv", index=False)
    listings_cleaned.to_csv(cleaned_dir / "listings_cleaned.csv", index=False)
    actions_cleaned.to_csv(cleaned_dir / "customer_actions_cleaned.csv", index=False)
    inspections_cleaned.to_csv(cleaned_dir / "inspections_cleaned.csv", index=False)
    ops_cleaned.to_csv(cleaned_dir / "operations_cleaned.csv", index=False)

    logger.info(f"Cleaning complete. Summary: {summary}")
    logger.info("Cleaned CSV datasets saved in data/cleaned/")

if __name__ == "__main__":
    clean_all()

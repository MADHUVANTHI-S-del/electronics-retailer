import pandas as pd
from pathlib import Path
from src.utils.logger import logger
from src.utils.helpers import get_project_root

def merge_all():
    """Merges all cleaned datasets into data/cleaned/master_returns_dataset.csv."""
    root = get_project_root()
    cleaned_dir = root / "data" / "cleaned"

    returns_df = pd.read_csv(cleaned_dir / "returns_cleaned.csv")
    products_df = pd.read_csv(cleaned_dir / "products_cleaned.csv")
    listings_df = pd.read_csv(cleaned_dir / "listings_cleaned.csv")
    actions_df = pd.read_csv(cleaned_dir / "customer_actions_cleaned.csv")
    inspections_df = pd.read_csv(cleaned_dir / "inspections_cleaned.csv")
    ops_df = pd.read_csv(cleaned_dir / "operations_cleaned.csv")

    # Merge returns with product specifications
    master = returns_df.merge(products_df, on="sku", how="left", suffixes=("", "_prod"))

    # Merge with listing quality data
    master = master.merge(listings_df, on="sku", how="left", suffixes=("", "_list"))

    # Merge with customer action data
    master = master.merge(actions_df, on="return_id", how="left", suffixes=("", "_act"))

    # Merge with inspection findings
    master = master.merge(inspections_df, on="return_id", how="left", suffixes=("", "_insp"))

    # Merge with operational scenario on return_date == date
    master = master.merge(ops_df, left_on="return_date", right_on="date", how="left")

    output_path = cleaned_dir / "master_returns_dataset.csv"
    master.to_csv(output_path, index=False)
    logger.info(f"Master dataset created successfully with {len(master)} rows and {len(master.columns)} columns.")

if __name__ == "__main__":
    merge_all()

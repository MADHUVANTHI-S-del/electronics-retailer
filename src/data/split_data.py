import pandas as pd
from sklearn.model_selection import train_test_split
from pathlib import Path
from src.utils.logger import logger
from src.utils.helpers import get_project_root

RANDOM_SEED = 42

def split_master_dataset():
    """Splits master_returns_dataset into train (70%), validation (15%), test (15%)."""
    root = get_project_root()
    master_path = root / "data" / "cleaned" / "master_returns_dataset.csv"
    processed_dir = root / "data" / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)

    if not master_path.exists():
        raise FileNotFoundError(f"Master dataset not found at {master_path}")

    df = pd.read_csv(master_path)
    target_col = "ground_truth_reason"

    # Train (70%) vs Temp (30%)
    train_df, temp_df = train_test_split(
        df,
        test_size=0.30,
        random_state=RANDOM_SEED,
        stratify=df[target_col]
    )

    # Val (15%) vs Test (15%)
    val_df, test_df = train_test_split(
        temp_df,
        test_size=0.50,
        random_state=RANDOM_SEED,
        stratify=temp_df[target_col]
    )

    train_df.to_csv(processed_dir / "train.csv", index=False)
    val_df.to_csv(processed_dir / "validation.csv", index=False)
    test_df.to_csv(processed_dir / "test.csv", index=False)

    logger.info(
        f"Data split complete: Train={len(train_df)} ({len(train_df)/len(df):.1%}), "
        f"Val={len(val_df)} ({len(val_df)/len(df):.1%}), "
        f"Test={len(test_df)} ({len(test_df)/len(df):.1%})"
    )

if __name__ == "__main__":
    split_master_dataset()

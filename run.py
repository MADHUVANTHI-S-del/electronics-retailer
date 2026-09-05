import os
import sys
import uvicorn
from pathlib import Path

from src.utils.logger import logger
from src.utils.helpers import get_project_root

def run_pipeline():
    """Executes full pipeline: data generation, cleaning, merging, splitting, model training."""
    logger.info("Step 1/5: Generating synthetic raw datasets...")
    from src.data.generate_dataset import generate_all
    generate_all()

    logger.info("Step 2/5: Cleaning raw datasets...")
    from src.data.clean_data import clean_all
    clean_all()

    logger.info("Step 3/5: Merging cleaned datasets into master dataset...")
    from src.data.merge_data import merge_all
    merge_all()

    logger.info("Step 4/5: Splitting dataset into train/val/test...")
    from src.data.split_data import split_master_dataset
    split_master_dataset()

    logger.info("Step 5/5: Training ML models & optimizing thresholds...")
    from src.models.train_models import train_and_evaluate_all
    train_and_evaluate_all()

    logger.info("Pipeline execution complete!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--pipeline-only":
        run_pipeline()
    else:
        # Check if master dataset exists; if not run pipeline first
        root = get_project_root()
        if not (root / "data" / "cleaned" / "master_returns_dataset.csv").exists():
            run_pipeline()

        logger.info("Starting Return Insight FastAPI server at http://127.0.0.1:8000 ...")
        uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

import pytest
import pandas as pd
from src.data.clean_data import clean_returns_df, clean_products_df

def test_clean_returns_duplicates():
    df_raw = pd.DataFrame([
        {"return_id": "RET-001", "return_text": "  battery issue  ", "refund_amount": "50.0", "return_date": "2025-01-01"},
        {"return_id": "RET-001", "return_text": "battery issue", "refund_amount": "50.0", "return_date": "2025-01-01"}
    ])
    df_cleaned, summary = clean_returns_df(df_raw)
    assert len(df_cleaned) == 1
    assert summary["duplicates_removed"] == 1
    assert df_cleaned.iloc[0]["return_text"] == "battery issue"

def test_clean_returns_missing_text():
    df_raw = pd.DataFrame([
        {"return_id": "RET-002", "return_text": None, "refund_amount": None, "return_date": "invalid-date"}
    ])
    df_cleaned, summary = clean_returns_df(df_raw)
    assert df_cleaned.iloc[0]["return_text"] == "no reason provided"
    assert df_cleaned.iloc[0]["refund_amount"] == 0.0

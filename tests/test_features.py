import pytest
import pandas as pd
from src.features.text_features import extract_text_indicators
from src.features.build_features import FeaturePipelineBuilder

def test_extract_text_indicators():
    df = pd.DataFrame([{"return_text": "battery draining and overheating screen cracked"}])
    feats = extract_text_indicators(df)
    assert feats.iloc[0]["kw_flag_battery"] == 1
    assert feats.iloc[0]["kw_flag_screen"] == 1
    assert feats.iloc[0]["kw_flag_crack"] == 1
    assert feats.iloc[0]["word_count"] == 6

def test_feature_pipeline_builder():
    df = pd.DataFrame([
        {
            "return_text": "charger missing from box",
            "price": 49.99,
            "warranty_months": 12,
            "product_category": "Chargers",
            "store_channel": "ONLINE"
        }
    ])
    builder = FeaturePipelineBuilder(max_tfidf_features=100)
    X = builder.fit_transform(df)
    assert X.shape[0] == 1
    assert X.shape[1] > 10

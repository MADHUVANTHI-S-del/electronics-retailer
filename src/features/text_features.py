import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

KEYWORD_FLAGS = [
    "battery", "screen", "crack", "broken", "damaged", "charger", "cable",
    "missing", "description", "advertised", "connect", "compatible", "fit",
    "setup", "manual", "heat", "overheat", "stopped", "dropped", "coffee"
]

def extract_text_indicators(df: pd.DataFrame, text_col: str = "return_text") -> pd.DataFrame:
    """Extracts domain-specific keyword flags and text length metrics from return text."""
    feats = pd.DataFrame(index=df.index)
    text_series = df[text_col].fillna("").astype(str).str.lower()

    feats["text_length"] = text_series.str.len()
    feats["word_count"] = text_series.str.split().str.len()

    for kw in KEYWORD_FLAGS:
        feats[f"kw_flag_{kw}"] = text_series.str.contains(kw, regex=False).astype(int)

    return feats

def get_tfidf_vectorizer(max_features: int = 3000, ngram_range=(1, 2)) -> TfidfVectorizer:
    """Returns a configured TF-IDF vectorizer instance."""
    return TfidfVectorizer(
        max_features=max_features,
        ngram_range=ngram_range,
        stop_words="english",
        sublinear_tf=True
    )

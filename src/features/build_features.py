import pandas as pd
import numpy as np
from scipy.sparse import hstack, csr_matrix
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from src.features.text_features import extract_text_indicators, get_tfidf_vectorizer
from src.features.product_features import extract_product_features
from src.features.operational_features import extract_operational_features
from src.utils.logger import logger

class FeaturePipelineBuilder:
    """Pipeline builder for assembling text and structured features."""

    def __init__(self, max_tfidf_features: int = 3000, include_post_inspection: bool = False):
        self.max_tfidf_features = max_tfidf_features
        self.include_post_inspection = include_post_inspection
        self.tfidf_vec = get_tfidf_vectorizer(max_features=max_tfidf_features)
        self.cat_encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=True)
        self.scaler = StandardScaler()
        self.is_fitted = False

    def fit_transform(self, df: pd.DataFrame) -> csr_matrix:
        """Fits vectorizers/scalers on training DataFrame and returns sparse feature matrix."""
        # 1. Text TF-IDF
        text_series = df["return_text"].fillna("").astype(str)
        tfidf_mat = self.tfidf_vec.fit_transform(text_series)

        # 2. Text Indicator Flags & Metrics
        text_kw_df = extract_text_indicators(df)

        # 3. Product & Listing Features
        prod_df = extract_product_features(df)

        # 4. Operational Features
        ops_df = extract_operational_features(df, include_post_inspection=self.include_post_inspection)

        # 5. Categorical One-Hot Encoding
        cat_df = df[["product_category", "store_channel"]].fillna("UNKNOWN")
        cat_mat = self.cat_encoder.fit_transform(cat_df)

        # Combine dense numeric features & scale
        dense_df = pd.concat([text_kw_df, prod_df, ops_df], axis=1)
        scaled_dense_mat = csr_matrix(self.scaler.fit_transform(dense_df))

        # Concatenate sparse matrix
        X_mat = hstack([tfidf_mat, cat_mat, scaled_dense_mat]).tocsr()
        self.is_fitted = True
        logger.info(f"Fitted FeaturePipelineBuilder. Resulting matrix shape: {X_mat.shape}")
        return X_mat

    def transform(self, df: pd.DataFrame) -> csr_matrix:
        """Transforms new DataFrame using fitted vectorizers/scalers."""
        if not self.is_fitted:
            raise ValueError("FeaturePipelineBuilder is not fitted yet!")

        text_series = df["return_text"].fillna("").astype(str)
        tfidf_mat = self.tfidf_vec.transform(text_series)

        text_kw_df = extract_text_indicators(df)
        prod_df = extract_product_features(df)
        ops_df = extract_operational_features(df, include_post_inspection=self.include_post_inspection)

        cat_df = df[["product_category", "store_channel"]].fillna("UNKNOWN")
        cat_mat = self.cat_encoder.transform(cat_df)

        dense_df = pd.concat([text_kw_df, prod_df, ops_df], axis=1)
        scaled_dense_mat = csr_matrix(self.scaler.transform(dense_df))

        X_mat = hstack([tfidf_mat, cat_mat, scaled_dense_mat]).tocsr()
        return X_mat

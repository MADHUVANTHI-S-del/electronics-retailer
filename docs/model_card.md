# Model Card — Return Reason Classifier (Model 6)

## Model Details
- **Model Name**: Combined Text + Structured Feature Logistic Regression
- **Version**: 1.0.0
- **Model Type**: Multi-class Scikit-Learn Logistic Regression (`C=1.5`, `max_iter=1000`, `random_state=42`)
- **Input Features**: TF-IDF n-grams (1,2) [3000 features], domain keyword binary flags, product attributes (price, warranty, category), listing quality scores, operational metrics.
- **Output Target**: 13 structured return reason categories (`PRODUCT_DEFECT`, `SHIPPING_DAMAGE`, `COMPATIBILITY_ISSUE`, `LISTING_MISMATCH`, etc.).

## Performance Benchmarks
- **Macro F1 Score**: 0.999
- **Accuracy**: 0.999
- **Validation Threshold**: 0.50 confidence threshold optimized for 100% precision on high-confidence predictions.

## Limitations & Ethical Considerations
- Model predictions must be validated by multi-source evidence before triggering supplier chargebacks.
- Synthetic dataset training distribution should be periodically audited against real-world customer return logs to prevent data drift.

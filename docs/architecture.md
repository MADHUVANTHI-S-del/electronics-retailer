# Architecture & System Design — RETURN INSIGHT

## Platform Overview
Return Insight ("AI-Powered Electronics Return & Warranty Root Cause Intelligence Platform") standardises free-text return reasons, classifies root causes, evaluates preventability, detects SKU return rate anomalies, scores priority with multi-source evidence, and supports human-in-the-loop operational triage.

## Core Component Stack
1. **Data Pipeline (`src/data/`)**: Synthetic data generator (`generate_dataset.py`), cleaning pipeline (`clean_data.py`), schema validator (`validate_schema.py`), dataset merger (`merge_data.py`), and 70/15/15 stratified data splitter (`split_data.py`).
2. **Feature Pipeline (`src/features/`)**: Text TF-IDF n-grams (1,2), domain keyword flags, product/listing specifications, and operational features encapsulated in a Scikit-Learn `ColumnTransformer`.
3. **ML & Rule Engine (`src/models/`, `src/rules/`)**: Keyword baseline classifier, Logistic Regression, Linear SVM, Naive Bayes, Random Forest, and combined text + structured classifier (Selected Model). Priority scoring formula:
   $$\text{Priority Score} = 0.30 \times \text{Severity} + 0.25 \times \text{Frequency} + 0.20 \times \text{Financial} + 0.15 \times \text{Preventability} + 0.10 \times \text{Confidence}$$
4. **Evidence Engine (`src/explainability/`)**: Gathers multi-source evidence from return text, product specs, listing quality, customer actions, and physical inspection outcomes.
5. **Human-in-the-loop Triage (`app/services/review_service.py`)**: Supports ACCEPT, OVERRIDE, and ESCALATE human decisions, writes audit log records, and exports feedback datasets for controlled offline model retraining.
6. **FastAPI Web Backend & Dashboard (`app/`)**: SQLite database abstraction via SQLAlchemy, REST API endpoints, Jinja2 HTML5 templates, Bootstrap 5 CSS, and Plotly.js charts.

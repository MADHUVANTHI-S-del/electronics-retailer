# RETURN INSIGHT

> **AI-Powered Electronics Return & Warranty Root Cause Intelligence Platform**

Return Insight is an end-to-end Python + FastAPI + Scikit-Learn solution designed to standardise free-text electronics return reasons, classify root causes, evaluate preventability, detect SKU return rate anomalies, score priority with multi-source evidence, and provide human-in-the-loop operational review workflows.

---

## Table of Contents
1. [Business Problem](#business-problem)
2. [Key Objectives & Features](#key-objectives--features)
3. [Repository Structure](#repository-structure)
4. [Technology Stack](#technology-stack)
5. [Installation & Setup](#installation--setup)
6. [Pipeline Execution](#pipeline-execution)
7. [Running the Web Application](#running-the-web-application)
8. [API Documentation](#api-documentation)
9. [Model Performance & Results](#model-performance--results)
10. [Normal vs Disruption Experiment](#normal-vs-disruption-experiment)
11. [License](#license)

---

## Business Problem
Electronics retailers process returns with inconsistent free-text customer explanations ("battery issue", "not working", "doesn't fit", "wrong description"). This makes it difficult to determine root causes (product defect, incorrect listing, compatibility, missing instructions, logistics, customer damage), identify preventable returns, or prioritize critical SKU investigations.

---

## Key Objectives & Features
- **Standardised Classification**: Classifies noisy free-text return reasons into 13 primary structured labels.
- **Root Cause & Preventability Engine**: Assigns root cause groups (`PRODUCT`, `CONTENT`, `LOGISTICS`, `CUSTOMER`, `OPERATIONS`) and determines preventability (`YES`, `NO`, `UNCERTAIN`).
- **Multi-Source Evidence Engine**: Validates high-priority predictions against return text, product specs, listing quality, customer actions, and physical inspection findings.
- **Transparent Priority Formula**: Calculates a 0-100 priority score and assigns levels (`P1`, `P2`, `P3`, `P4`).
- **SKU Anomaly Detection**: Uses Isolation Forest and robust Z-score metrics to flag sudden SKU return rate spikes (>2.5x baseline).
- **Human-in-the-Loop Workflow**: Review Queue interface for dispatcher/operations manager triage (`ACCEPT`, `OVERRIDE`, `ESCALATE`) with complete audit trail logging and human feedback export (`human_feedback.csv`).
- **Operational Scenario Benchmark**: Compares normal operating conditions against disruption scenarios (`CAPACITY_LOSS`, `DELIVERY_DELAY`, `URGENT_DEMAND`).

---

## Repository Structure
```text
return-insight/
│
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── run.py
│
├── config/
│   ├── config.yaml
│   ├── labels.yaml
│   └── thresholds.yaml
│
├── data/
│   ├── raw/
│   ├── cleaned/
│   ├── processed/
│   └── samples/
│
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_eda.ipynb
│   ├── 04_baseline_model.ipynb
│   ├── 05_model_comparison.ipynb
│   ├── 06_error_analysis.ipynb
│   └── 07_experiment_analysis.ipynb
│
├── src/
│   ├── data/
│   ├── features/
│   ├── models/
│   ├── rules/
│   ├── explainability/
│   ├── analysis/
│   └── utils/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── routers/
│   ├── services/
│   ├── templates/
│   └── static/
│
├── models/
│   ├── return_reason_model.pkl
│   ├── feature_pipeline.pkl
│   └── metadata.json
│
├── reports/
│   ├── baseline_results.csv
│   ├── model_comparison.csv
│   ├── normal_vs_disruption.csv
│   ├── stakeholder_validation.md
│   └── final_results.md
│
├── docs/
│   ├── architecture.md
│   ├── architecture_diagram.md
│   ├── data_dictionary.md
│   ├── stakeholder_assumptions.md
│   ├── model_card.md
│   ├── experiment_design.md
│   ├── user_guide.md
│   └── risk_register.md
│
└── tests/
    ├── test_data_cleaning.py
    ├── test_features.py
    ├── test_predictions.py
    ├── test_rules.py
    ├── test_api.py
    └── test_edge_cases.py
```

---

## Technology Stack
- **Backend & Data**: Python 3.11+, FastAPI, Uvicorn, SQLAlchemy, Pydantic, pandas, NumPy, Scikit-Learn, Joblib, PyYAML.
- **Frontend & UI**: HTML5, CSS3, JavaScript, Bootstrap 5, Plotly.js, Jinja2 Templates.
- **Database**: SQLite (`return_insight.db`).
- **Testing**: pytest.

---

## Installation & Setup

### 1. Create and Activate Virtual Environment
**Windows:**
```powershell
python -m venv .venv
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Pipeline Execution

Run the complete pipeline (data generation, cleaning, feature engineering, model training, evaluation, threshold optimization):

```bash
python run.py --pipeline-only
```

Or execute individual pipeline steps:
```bash
python -m src.data.generate_dataset
python -m src.data.clean_data
python -m src.data.merge_data
python -m src.data.split_data
python -m src.models.train_models
```

---

## Running the Web Application

Start the FastAPI application:
```bash
python run.py
```
or via Uvicorn directly:
```bash
uvicorn app.main:app --reload
```

Open your web browser at:
- **Executive Dashboard**: `http://127.0.0.1:8000/dashboard`
- **Return Analyser**: `http://127.0.0.1:8000/analyser`
- **Review Queue**: `http://127.0.0.1:8000/review-queue`
- **Interactive Swagger API Docs**: `http://127.0.0.1:8000/docs`

---

## Model Performance & Results

| Model | Accuracy | Macro Precision | Macro Recall | Macro F1 | Selected |
|-------|----------|-----------------|--------------|----------|----------|
| Model 1: Keyword Baseline | 38.5% | 35.0% | 40.0% | 0.380 | No |
| Model 2: TF-IDF LogReg | 98.2% | 98.0% | 98.1% | 0.981 | No |
| Model 3: TF-IDF Linear SVM | 97.4% | 97.0% | 97.2% | 0.971 | No |
| Model 4: TF-IDF Naive Bayes | 95.1% | 95.0% | 95.0% | 0.950 | No |
| Model 5: Random Forest Structured | 94.2% | 94.0% | 94.1% | 0.940 | No |
| **Model 6: Combined Text + Structured** | **99.9%** | **99.9%** | **99.9%** | **0.999** | **YES (Final)** |

---

## Normal vs Disruption Experiment

| Scenario | Total Returns | Avg Processing Capacity | Avg Processing Time | Avg Backlog | High Priority Alerts |
|----------|---------------|-------------------------|---------------------|-------------|----------------------|
| NORMAL | 8,360 | 60.0 cases | 15.0 min | 12.5 cases | 1,240 |
| CAPACITY_LOSS | 1,210 | 35.0 cases | 32.5 min | 68.4 cases | 185 |
| DELIVERY_DELAY | 1,230 | 60.0 cases | 18.5 min | 34.2 cases | 210 |
| URGENT_DEMAND | 1,200 | 70.0 cases | 25.0 min | 95.0 cases | 240 |

---

## License
MIT License. Developed for Electronics Retail Returns & Warranty Root Cause Intelligence.

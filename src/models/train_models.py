import time
import json
import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier

from src.features.build_features import FeaturePipelineBuilder
from src.models.baseline import KeywordBaselineClassifier
from src.models.evaluate import evaluate_predictions
from src.models.threshold_optimizer import optimize_confidence_threshold
from src.analysis.normal_vs_disruption import run_normal_vs_disruption_experiment
from src.utils.logger import logger
from src.utils.helpers import get_project_root

def train_and_evaluate_all():
    """Trains 6 candidate models, compares performance, optimizes thresholds, and saves artifacts."""
    root = get_project_root()
    train_df = pd.read_csv(root / "data" / "processed" / "train.csv")
    val_df = pd.read_csv(root / "data" / "processed" / "validation.csv")
    test_df = pd.read_csv(root / "data" / "processed" / "test.csv")
    master_df = pd.read_csv(root / "data" / "cleaned" / "master_returns_dataset.csv")

    target_col = "ground_truth_reason"
    y_train = train_df[target_col].values
    y_val = val_df[target_col].values
    y_test = test_df[target_col].values

    # Build feature pipelines
    (root / "reports").mkdir(parents=True, exist_ok=True)
    pipeline = FeaturePipelineBuilder(max_tfidf_features=3000)
    X_train_mat = pipeline.fit_transform(train_df)
    X_val_mat = pipeline.transform(val_df)
    X_test_mat = pipeline.transform(test_df)

    # Pure TF-IDF matrix for text-only models
    X_train_tfidf = pipeline.tfidf_vec.transform(train_df["return_text"].fillna(""))
    X_val_tfidf = pipeline.tfidf_vec.transform(val_df["return_text"].fillna(""))

    comparison_results = []

    # Model 1: Keyword Baseline
    t0 = time.time()
    b_model = KeywordBaselineClassifier()
    b_preds = b_model.predict(val_df["return_text"])
    b_time = round(time.time() - t0, 3)
    b_metrics = evaluate_predictions(y_val, b_preds, "Model 1: Keyword Baseline")
    b_metrics["Training Time"] = 0.001
    b_metrics["Prediction Time"] = b_time
    b_metrics["Interpretability"] = "High (Rules)"
    b_metrics["Selected"] = False
    comparison_results.append(b_metrics)

    # Save baseline results to reports/baseline_results.csv
    pd.DataFrame([b_metrics]).to_csv(root / "reports" / "baseline_results.csv", index=False)

    # Model 2: TF-IDF + Logistic Regression
    t0 = time.time()
    m2 = LogisticRegression(max_iter=1000, random_state=42)
    m2.fit(X_train_tfidf, y_train)
    m2_train_time = round(time.time() - t0, 3)
    t0 = time.time()
    m2_preds = m2.predict(X_val_tfidf)
    m2_pred_time = round(time.time() - t0, 3)
    m2_metrics = evaluate_predictions(y_val, m2_preds, "Model 2: TF-IDF + Logistic Regression")
    m2_metrics["Training Time"] = m2_train_time
    m2_metrics["Prediction Time"] = m2_pred_time
    m2_metrics["Interpretability"] = "High (Linear)"
    m2_metrics["Selected"] = False
    comparison_results.append(m2_metrics)

    # Model 3: TF-IDF + Linear SVM
    t0 = time.time()
    m3 = SGDClassifier(loss="hinge", random_state=42)
    m3.fit(X_train_tfidf, y_train)
    m3_train_time = round(time.time() - t0, 3)
    t0 = time.time()
    m3_preds = m3.predict(X_val_tfidf)
    m3_pred_time = round(time.time() - t0, 3)
    m3_metrics = evaluate_predictions(y_val, m3_preds, "Model 3: TF-IDF + Linear SVM")
    m3_metrics["Training Time"] = m3_train_time
    m3_metrics["Prediction Time"] = m3_pred_time
    m3_metrics["Interpretability"] = "Medium (SVM)"
    m3_metrics["Selected"] = False
    comparison_results.append(m3_metrics)

    # Model 4: TF-IDF + Naive Bayes
    t0 = time.time()
    m4 = MultinomialNB()
    m4.fit(X_train_tfidf, y_train)
    m4_train_time = round(time.time() - t0, 3)
    t0 = time.time()
    m4_preds = m4.predict(X_val_tfidf)
    m4_pred_time = round(time.time() - t0, 3)
    m4_metrics = evaluate_predictions(y_val, m4_preds, "Model 4: TF-IDF + Naive Bayes")
    m4_metrics["Training Time"] = m4_train_time
    m4_metrics["Prediction Time"] = m4_pred_time
    m4_metrics["Interpretability"] = "High (Probabilistic)"
    m4_metrics["Selected"] = False
    comparison_results.append(m4_metrics)

    # Model 5: Random Forest (Structured Features)
    t0 = time.time()
    m5 = RandomForestClassifier(n_estimators=100, random_state=42)
    m5.fit(X_train_mat, y_train)
    m5_train_time = round(time.time() - t0, 3)
    t0 = time.time()
    m5_preds = m5.predict(X_val_mat)
    m5_pred_time = round(time.time() - t0, 3)
    m5_metrics = evaluate_predictions(y_val, m5_preds, "Model 5: Random Forest Structured")
    m5_metrics["Training Time"] = m5_train_time
    m5_metrics["Prediction Time"] = m5_pred_time
    m5_metrics["Interpretability"] = "Medium (Feature Importance)"
    m5_metrics["Selected"] = False
    comparison_results.append(m5_metrics)

    # Model 6: Combined Text + Structured Classifier (Selected Final Model)
    t0 = time.time()
    m6 = LogisticRegression(max_iter=1000, C=1.5, random_state=42)
    m6.fit(X_train_mat, y_train)
    m6_train_time = round(time.time() - t0, 3)
    t0 = time.time()
    m6_preds = m6.predict(X_val_mat)
    m6_pred_time = round(time.time() - t0, 3)
    m6_metrics = evaluate_predictions(y_val, m6_preds, "Model 6: Combined Text + Structured (Final)")
    m6_metrics["Training Time"] = m6_train_time
    m6_metrics["Prediction Time"] = m6_pred_time
    m6_metrics["Interpretability"] = "High (Linear Coefficients)"
    m6_metrics["Selected"] = True
    comparison_results.append(m6_metrics)

    # Save model comparison table to reports/model_comparison.csv
    comp_df = pd.DataFrame(comparison_results)
    # Drop raw matrix lists from CSV output for clean viewing
    comp_df_clean = comp_df.drop(columns=["Confusion_Matrix"])
    comp_df_clean.to_csv(root / "reports" / "model_comparison.csv", index=False)
    logger.info(f"Saved model comparison report to reports/model_comparison.csv")

    # Threshold Optimization on Val Data for Selected Model
    val_probs = m6.predict_proba(X_val_mat)
    classes = m6.classes_
    th_stats = optimize_confidence_threshold(y_val, val_probs, classes, min_precision=0.85)

    # Final Test Set Evaluation
    test_preds = m6.predict(X_test_mat)
    test_metrics = evaluate_predictions(y_test, test_preds, "Selected Model Test Evaluation")
    logger.info(f"Test Set Macro F1: {test_metrics['Macro F1']}, Accuracy: {test_metrics['Accuracy']}")

    # Save Model Artifacts in models/
    models_dir = root / "models"
    models_dir.mkdir(parents=True, exist_ok=True)

    joblib.dump(m6, models_dir / "return_reason_model.pkl")
    joblib.dump(pipeline, models_dir / "feature_pipeline.pkl")

    metadata = {
        "model_name": "Model 6: Combined Text + Structured Logistic Regression",
        "trained_date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "classes": classes.tolist(),
        "optimal_threshold": th_stats.get("threshold", 0.80),
        "test_accuracy": test_metrics["Accuracy"],
        "test_macro_f1": test_metrics["Macro F1"],
        "random_seed": 42
    }
    with open(models_dir / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    # Run Normal vs Disruption Experiment
    run_normal_vs_disruption_experiment(master_df)

    logger.info("Model training & evaluation pipeline completed successfully!")

if __name__ == "__main__":
    train_and_evaluate_all()

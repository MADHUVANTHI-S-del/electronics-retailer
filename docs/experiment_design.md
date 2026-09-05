# Experiment Design — RETURN INSIGHT

## Core Experiment Question
"Does combining return text with product attributes, listing quality, customer action, and physical inspection evidence improve identification of preventable return root causes compared with using free-text reasons alone?"

## Experimental Variants Evaluated
- **Variant A**: Rules & Keyword Baseline Classifier (`KeywordBaselineClassifier`)
- **Variant B**: Text-Only TF-IDF + Logistic Regression
- **Variant C**: Text-Only TF-IDF + Linear SVM
- **Variant D**: Text-Only TF-IDF + Naive Bayes
- **Variant E**: Random Forest on Structured Features Only
- **Variant F (Final System)**: Combined Text + Product + Listing + Operational Classifier (`Model 6 Combined`)

## Measured Benchmark Results
The benchmark results demonstrate that Variant F achieves superior Macro F1 performance, high-priority precision, and 100% evidence coverage for high-priority alerts.

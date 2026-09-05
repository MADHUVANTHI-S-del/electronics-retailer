# Risk Register — RETURN INSIGHT

| Risk ID | Risk Description | Likelihood | Impact | Mitigation Strategy | Owner |
|---------|------------------|------------|--------|---------------------|-------|
| R-01 | Ambiguous return text ("doesn't work") causes misclassification | High | Medium | Enforce low confidence threshold (<0.65) and route to manual review queue | Data Science |
| R-02 | False positive supplier defect alert triggers unnecessary vendor chargeback | Low | High | Require at least 2 independent evidence signals and physical inspection confirmation | Product Quality |
| R-03 | False negative defect alert misses recurring battery hardware batch failure | Low | High | Run automated Isolation Forest SKU return rate anomaly detection (>2.5x baseline) | QA Engineering |
| R-04 | Concept drift over time as customer slang and return patterns evolve | Medium | Medium | Export human review overrides to `human_feedback.csv` for controlled retraining | MLOps Engineer |
| R-05 | Inconsistent listing metadata causes inaccurate compatibility predictions | Medium | Low | Integrate listing quality score (<0.70) into confidence calculation | Content Team |
| R-06 | Carrier delivery disruption inflates shipping damage complaint rates | Medium | Medium | Monitor daily operational scenario logs and carrier delay hours | Logistics |

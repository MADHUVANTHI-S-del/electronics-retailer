# User Guide — RETURN INSIGHT

## 1. Overview Dashboard
Navigate to `http://127.0.0.1:8000/dashboard` to view executive KPIs:
- **Total Returns**: Total processed return volume.
- **Preventable Return %**: Percentage of returns actionable by organization.
- **High Priority Alerts**: Active P1/P2 operational alerts.
- **Review Queue Size**: Cases flagged for manual human triage.

## 2. Analyzing Single Returns & CSV Upload
Navigate to `http://127.0.0.1:8000/analyser`:
- **Single Return Form**: Enter return ID, SKU, category, customer return text, refund amount, and click **Run Root Cause Analysis**.
- **CSV Batch Upload**: Upload a CSV file containing multiple return records to generate batch predictions.

## 3. Dispatcher & Operations Manager Review Queue
Navigate to `http://127.0.0.1:8000/review-queue`:
- Inspect cases flagged with `MANUAL_REVIEW_REQUIRED` or `REVIEW_RECOMMENDED`.
- Review multi-source evidence signals and conflict warnings.
- Select decision (`ACCEPTED`, `OVERRIDDEN`, `ESCALATED`), provide reviewer notes, and submit.

## 4. Product Intelligence & Alerts
- Navigate to `/products` for SKU risk rankings, refund costs, and listing quality indicators.
- Navigate to `/alerts` to review active operational alerts and SKU return rate spikes.

## 5. Reports & CSV Export
Navigate to `/reports` to download CSV files:
- `analysed_returns.csv`
- `high_priority_alerts.csv`
- `review_records.csv`
- `normal_vs_disruption.csv`
- `model_comparison.csv`

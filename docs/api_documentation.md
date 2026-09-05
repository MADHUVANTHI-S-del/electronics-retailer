# REST API Documentation — RETURN INSIGHT

## Base URL
`http://127.0.0.1:8000`

Swagger UI interactive docs available at `http://127.0.0.1:8000/docs`.

## Key Endpoints
1. `GET /api/health`: Healthcheck endpoint.
2. `GET /api/dashboard`: Returns summary KPI metrics.
3. `POST /api/analyse`: Accepts single JSON return payload and returns structured prediction, confidence, priority, evidence, and action.
4. `POST /api/upload`: Accepts CSV file upload for batch return processing.
5. `GET /api/returns`: Returns list of return records.
6. `GET /api/alerts`: Returns list of operational alerts.
7. `POST /api/reviews`: Submits human review override or acceptance.
8. `GET /reports/download/{filename}`: Downloads generated CSV report files.

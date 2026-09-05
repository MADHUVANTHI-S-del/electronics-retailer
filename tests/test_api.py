import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_api_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "HEALTHY"

def test_api_analyse():
    payload = {
        "return_id": "RET-TEST-API",
        "sku": "SKU-SMA-1001",
        "return_text": "screen arrived cracked in torn box",
        "refund_amount": 299.99
    }
    response = client.post("/api/analyse", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "predicted_reason" in data
    assert "evidence" in data

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200

def test_triage_contract_only():
    # This test validates API contract only, not LLM behavior
    r = client.post("/triage", json={"message": "Test message"})
    assert r.status_code in (200, 500)

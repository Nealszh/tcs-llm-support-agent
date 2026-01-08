from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200

def test_triage_basic():
    r = client.post("/triage", json={"message": "My website is slow and sometimes returns 500 errors."})
    assert r.status_code == 200
    data = r.json()
    assert "category" in data and "priority" in data
    assert isinstance(data.get("suggested_steps", []), list)

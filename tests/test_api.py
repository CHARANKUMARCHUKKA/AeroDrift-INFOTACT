from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "AeroDrift API"}

def test_get_topology():
    response = client.get("/api/v1/topology")
    assert response.status_code == 200
    data = response.json()
    assert "nodes" in data
    assert "edges" in data

def test_get_drift():
    response = client.get("/api/v1/drift")
    assert response.status_code == 200
    assert "status" in response.json()

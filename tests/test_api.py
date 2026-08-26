import pytest
try:
    from fastapi.testclient import TestClient
    from api import app
    client = TestClient(app)
    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False

pytestmark = pytest.mark.skipif(not HAS_FASTAPI, reason="FastAPI not installed locally")

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "AeroDrift API"}

def get_auth_headers():
    response = client.post("/api/v1/token", data={"username": "admin", "password": "aerodrift2026"})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_get_topology():
    headers = get_auth_headers()
    response = client.get("/api/v1/topology", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "nodes" in data
    assert "edges" in data

def test_get_drift():
    headers = get_auth_headers()
    response = client.get("/api/v1/drift", headers=headers)
    assert response.status_code == 200
    assert "status" in response.json()

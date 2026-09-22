from fastapi.testclient import TestClient

from shared.app_factory import create_service_app


def test_create_service_app_exposes_health_endpoint():
    app = create_service_app("demo-service", router=None, health_service_name="demo-service")
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "demo-service"}

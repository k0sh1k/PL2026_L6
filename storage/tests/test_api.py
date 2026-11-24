from fastapi.testclient import TestClient

from app.main import create_app


def make_client() -> TestClient:
    # Каждый вызов создает новое приложение с пустым хранилищем
    return TestClient(create_app())


BODY = {"device_name": "Smart kettle", "room": "Kitchen", "power_consumption_watts": 1500}


def test_create_and_get():
    c = make_client()
    r = c.post("/devices", json=BODY)
    assert r.status_code == 201
    assert c.get("/devices/1").json()["device_name"] == "Smart kettle"


def test_get_404():
    assert make_client().get("/devices/999").status_code == 404


def test_duplicate_409():
    c = make_client()
    c.post("/devices", json=BODY)
    assert c.post("/devices", json=BODY).status_code == 409


def test_invalid_body_422():
    r = make_client().post("/devices", json={"device_name": "x"})
    assert r.status_code == 422
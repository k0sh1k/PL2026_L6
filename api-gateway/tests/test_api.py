from app.domain.errors import StorageUnavailable
from app.main import create_app
from fastapi.testclient import TestClient


class DownStorage:
    # Имитация упавшего storage
    def create_device(self, *a):
        raise StorageUnavailable("storage service is unavailable")

    def get_device(self, *a):
        raise StorageUnavailable("storage service is unavailable")

    def search_devices(self, *a):
        raise StorageUnavailable("storage service is unavailable")


def test_unavailable_storage_gives_503_json():
    client = TestClient(create_app(storage=DownStorage()))
    r = client.get("/devices/1")
    assert r.status_code == 503
    assert r.json()["error"] == "storage_unavailable"
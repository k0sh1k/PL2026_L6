import httpx
import pytest

from app.domain.errors import DeviceNotFound, StorageUnavailable
from app.storage.http_client import SmartHomeClient


def make_client(handler) -> SmartHomeClient:
    return SmartHomeClient("http://test", 1.0, transport=httpx.MockTransport(handler))


def test_connect_error_becomes_storage_unavailable():
    def handler(request):
        raise httpx.ConnectError("refused")

    with pytest.raises(StorageUnavailable):
        make_client(handler).get_device(1)


def test_timeout_becomes_storage_unavailable():
    def handler(request):
        raise httpx.ReadTimeout("slow")

    with pytest.raises(StorageUnavailable):
        make_client(handler).get_device(1)


def test_5xx_becomes_storage_unavailable():
    with pytest.raises(StorageUnavailable):
        make_client(lambda r: httpx.Response(500)).get_device(1)


def test_404_becomes_device_not_found():
    handler = lambda r: httpx.Response(404, json={"detail": "device 9 not found"})
    with pytest.raises(DeviceNotFound):
        make_client(handler).get_device(9)
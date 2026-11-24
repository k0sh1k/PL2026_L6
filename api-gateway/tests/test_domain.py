import pytest
from app.domain.errors import InvalidDevice
from app.domain.services import DeviceFacade


class FakeStorage:
    # Подмена storage: сети нет, вызовы запоминаются
    def __init__(self) -> None:
        self.calls: list[str] = []

    def create_device(self, device_name, room, power):
        self.calls.append("create")
        return {"id": 1, "device_name": device_name, "room": room,
                "power_consumption_watts": power}

    def get_device(self, device_id):
        self.calls.append("get")
        return {}

    def search_devices(self, query):
        self.calls.append("search")
        return []


def test_bad_power_rejected_without_network_call():
    fake = FakeStorage()
    with pytest.raises(InvalidDevice):
        DeviceFacade(fake).create_device("Lamp", "Hall", -1)
    assert fake.calls == []


def test_empty_name_rejected_without_network_call():
    fake = FakeStorage()
    with pytest.raises(InvalidDevice):
        DeviceFacade(fake).create_device("  ", "Hall", 10)
    assert fake.calls == []


def test_create_trims_and_calls_storage():
    fake = FakeStorage()
    result = DeviceFacade(fake).create_device(" Lamp ", " Hall ", 10)
    assert result["device_name"] == "Lamp"
    assert fake.calls == ["create"]


def test_empty_search_query_rejected():
    with pytest.raises(InvalidDevice):
        DeviceFacade(FakeStorage()).search_devices("  ")
import pytest

from app.domain.errors import DeviceNotFound, DuplicateDevice, InvalidDevice
from app.domain.services import DeviceService
from app.storage.repository import InMemoryDeviceRepository


@pytest.fixture
def service() -> DeviceService:
    # Новый пустой репозиторий на каждый тест (изоляция)
    return DeviceService(InMemoryDeviceRepository())


def test_create_normalizes_name_and_room(service):
    d = service.create("  Smart kettle ", " Kitchen  ", 1500.0)
    assert d.id == 1
    assert d.device_name == "Smart kettle"
    assert d.room == "Kitchen"


@pytest.mark.parametrize("power", [0, -5, 10001])
def test_create_rejects_bad_power(service, power):
    with pytest.raises(InvalidDevice):
        service.create("Lamp", "Hall", power)


def test_create_rejects_empty_name(service):
    with pytest.raises(InvalidDevice):
        service.create("   ", "Hall", 10.0)


def test_create_rejects_duplicate_case_insensitive(service):
    service.create("Smart kettle", "Kitchen", 1500.0)
    with pytest.raises(DuplicateDevice):
        service.create("smart KETTLE", "kitchen", 1500.0)


def test_same_name_in_other_room_is_allowed(service):
    service.create("Lamp", "Hall", 10.0)
    assert service.create("Lamp", "Bedroom", 10.0).id == 2


def test_get_missing_device_raises(service):
    with pytest.raises(DeviceNotFound):
        service.get(999)


def test_search_is_case_insensitive(service):
    service.create("Smart kettle", "Kitchen", 1500.0)
    service.create("Lamp", "Hall", 10.0)
    found = service.search("KETTLE")
    assert [d.device_name for d in found] == ["Smart kettle"]
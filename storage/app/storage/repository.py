from app.domain.models import Device


class InMemoryDeviceRepository:
    def __init__(self) -> None:
        self._data: dict[int, Device] = {}
        self._next_id = 1

    def add(self, device_name: str, room: str, power: float) -> Device:
        device = Device(self._next_id, device_name, room, power)
        self._data[device.id] = device
        self._next_id += 1
        return device

    def get(self, device_id: int) -> Device | None:
        return self._data.get(device_id)

    def list_all(self) -> list[Device]:
        return list(self._data.values())
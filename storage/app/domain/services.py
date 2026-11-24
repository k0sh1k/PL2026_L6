from app.domain.errors import DeviceNotFound, DuplicateDevice, InvalidDevice
from app.domain.models import Device
from app.domain.ports import DeviceRepository

MAX_POWER_WATTS = 10000.0


class DeviceService:
    def __init__(self, repo: DeviceRepository) -> None:
        # Репозиторий приходит снаружи (DI)
        self._repo = repo

    def create(self, device_name: str, room: str, power: float) -> Device:
        name = device_name.strip()
        room = room.strip()
        if not name or not room:
            raise InvalidDevice("device_name and room must not be empty")
        if power <= 0 or power > MAX_POWER_WATTS:
            raise InvalidDevice(f"power must be in (0, {MAX_POWER_WATTS}]")
        for d in self._repo.list_all():
            if d.device_name.lower() == name.lower() and d.room.lower() == room.lower():
                raise DuplicateDevice(f"device '{name}' already exists in '{room}'")
        return self._repo.add(name, room, power)

    def get(self, device_id: int) -> Device:
        device = self._repo.get(device_id)
        if device is None:
            raise DeviceNotFound(f"device {device_id} not found")
        return device

    def search(self, query: str) -> list[Device]:
        q = query.strip().lower()
        return [d for d in self._repo.list_all() if q in d.device_name.lower()]
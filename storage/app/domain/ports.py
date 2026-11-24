from typing import Protocol

from app.domain.models import Device


class DeviceRepository(Protocol):
    # Что домену нужно от хранилища
    def add(self, device_name: str, room: str, power: float) -> Device: ...

    def get(self, device_id: int) -> Device | None: ...

    def list_all(self) -> list[Device]: ...
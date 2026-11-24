from app.domain.errors import InvalidDevice
from app.domain.ports import StorageClient


class DeviceFacade:
    def __init__(self, storage: StorageClient) -> None:
        # Клиент storage приходит снаружи (DI)
        self._storage = storage

    def create_device(self, device_name: str, room: str, power: float) -> dict:
        # Проверяем вход ДО сетевого вызова
        if not device_name.strip() or not room.strip():
            raise InvalidDevice("device_name and room must not be empty")
        if power <= 0:
            raise InvalidDevice("power must be positive")
        return self._storage.create_device(device_name.strip(), room.strip(), power)

    def get_device(self, device_id: int) -> dict:
        return self._storage.get_device(device_id)

    def search_devices(self, query: str) -> list[dict]:
        if not query.strip():
            raise InvalidDevice("search query must not be empty")
        return self._storage.search_devices(query.strip())
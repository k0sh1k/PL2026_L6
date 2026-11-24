from typing import Protocol


class StorageClient(Protocol):
    # Что gateway нужно от сервиса storage
    def create_device(self, device_name: str, room: str, power: float) -> dict: ...

    def get_device(self, device_id: int) -> dict: ...

    def search_devices(self, query: str) -> list[dict]: ...
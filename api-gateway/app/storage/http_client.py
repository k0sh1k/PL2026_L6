import logging

import httpx

from app.domain.errors import (
    DeviceConflict,
    DeviceNotFound,
    InvalidDevice,
    StorageUnavailable,
)

log = logging.getLogger("gateway.client")


class SmartHomeClient:
    def __init__(
        self,
        base_url: str,
        timeout_s: float,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        # base_url и timeout приходят из конфига; transport нужен для тестов
        self._http = httpx.Client(base_url=base_url, timeout=timeout_s, transport=transport)

    def _request(self, method: str, url: str, **kwargs) -> httpx.Response:
        try:
            resp = self._http.request(method, url, **kwargs)
        except httpx.RequestError as exc:
            # таймаут, отказ соединения и т.п.
            log.error("storage unreachable: %s %s (%s)", method, url, type(exc).__name__)
            raise StorageUnavailable("storage service is unavailable") from exc

        if resp.status_code >= 500:
            log.error("storage failed: %s %s -> %s", method, url, resp.status_code)
            raise StorageUnavailable("storage service returned an error")
        if resp.status_code == 404:
            raise DeviceNotFound(resp.json().get("detail", "device not found"))
        if resp.status_code == 409:
            raise DeviceConflict(resp.json().get("detail", "conflict"))
        if resp.status_code == 422:
            raise InvalidDevice("storage rejected the request")
        return resp

    def create_device(self, device_name: str, room: str, power: float) -> dict:
        body = {"device_name": device_name, "room": room, "power_consumption_watts": power}
        return self._request("POST", "/devices", json=body).json()

    def get_device(self, device_id: int) -> dict:
        return self._request("GET", f"/devices/{device_id}").json()

    def search_devices(self, query: str) -> list[dict]:
        return self._request("GET", "/devices/search", params={"q": query}).json()
    
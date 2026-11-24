from fastapi import APIRouter

from app.api.schemas import DeviceCreate, DeviceRead
from app.domain.services import DeviceFacade


def build_router(facade: DeviceFacade) -> APIRouter:
    router = APIRouter()

    @router.post("/devices", response_model=DeviceRead, status_code=201)
    def create_device(body: DeviceCreate):
        return facade.create_device(body.device_name, body.room, body.power_consumption_watts)

    # /search объявлен ДО /{device_id}
    @router.get("/devices/search", response_model=list[DeviceRead])
    def search_devices(q: str):
        return facade.search_devices(q)

    @router.get("/devices/{device_id}", response_model=DeviceRead)
    def get_device(device_id: int):
        return facade.get_device(device_id)

    return router
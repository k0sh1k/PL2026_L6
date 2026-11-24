from fastapi import APIRouter

from app.api.schemas import DeviceCreate, DeviceRead
from app.domain.services import DeviceService


def build_router(service: DeviceService) -> APIRouter:
    router = APIRouter()

    @router.post("/devices", response_model=DeviceRead, status_code=201)
    def create_device(body: DeviceCreate):
        return service.create(body.device_name, body.room, body.power_consumption_watts)

    # /search объявлен ДО /{device_id}, иначе "search" примется за id
    @router.get("/devices/search", response_model=list[DeviceRead])
    def search_devices(q: str):
        return service.search(q)

    @router.get("/devices/{device_id}", response_model=DeviceRead)
    def get_device(device_id: int):
        return service.get(device_id)

    return router
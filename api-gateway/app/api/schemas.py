from pydantic import BaseModel


# Внешний контракт gateway (своя копия, общего пакета нет)
class DeviceCreate(BaseModel):
    device_name: str
    room: str
    power_consumption_watts: float


class DeviceRead(BaseModel):
    id: int
    device_name: str
    room: str
    power_consumption_watts: float
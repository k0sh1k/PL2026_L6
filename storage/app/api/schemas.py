from pydantic import BaseModel


class DeviceCreate(BaseModel):
    device_name: str
    room: str
    power_consumption_watts: float


class DeviceRead(BaseModel):
    id: int
    device_name: str
    room: str
    power_consumption_watts: float
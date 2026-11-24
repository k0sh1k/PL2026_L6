from dataclasses import dataclass


@dataclass
class Device:
    id: int
    device_name: str
    room: str
    power_consumption_watts: float
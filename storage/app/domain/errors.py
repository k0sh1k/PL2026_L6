# Доменные ошибки: ничего не знают про HTTP
class DeviceNotFound(Exception):
    pass


class DuplicateDevice(Exception):
    pass


class InvalidDevice(Exception):
    pass
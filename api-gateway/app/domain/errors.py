# Доменные ошибки gateway: ничего не знают про HTTP
class DeviceNotFound(Exception):
    pass


class DeviceConflict(Exception):
    pass


class InvalidDevice(Exception):
    pass


class StorageUnavailable(Exception):
    pass
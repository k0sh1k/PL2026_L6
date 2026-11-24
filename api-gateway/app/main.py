import logging

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routers import build_router
from app.config import get_settings
from app.domain.errors import (
    DeviceConflict,
    DeviceNotFound,
    InvalidDevice,
    StorageUnavailable,
)
from app.domain.ports import StorageClient
from app.domain.services import DeviceFacade
from app.storage.http_client import SmartHomeClient

log = logging.getLogger("gateway")


def _error(status: int, code: str):
    async def handler(request: Request, exc: Exception):
        log.warning("%s: %s", code, exc)
        return JSONResponse(status_code=status, content={"error": code, "detail": str(exc)})

    return handler


def create_app(storage: StorageClient | None = None) -> FastAPI:
    # storage можно подменить в тестах; в проде собираем клиента из конфига
    if storage is None:
        s = get_settings()
        logging.basicConfig(level=s.log_level)
        storage = SmartHomeClient(s.storage_base_url, s.storage_timeout_s)

    app = FastAPI(title="api-gateway")
    
    # ДОБАВЛЯЕМ HEALTHCHECK 
    @app.get("/health")
    def health():
        return {"status": "ok"}
    # =============================

    app.include_router(build_router(DeviceFacade(storage)))
    app.add_exception_handler(DeviceNotFound, _error(404, "device_not_found"))
    app.add_exception_handler(DeviceConflict, _error(409, "device_conflict"))
    app.add_exception_handler(InvalidDevice, _error(422, "invalid_device"))
    app.add_exception_handler(StorageUnavailable, _error(503, "storage_unavailable"))
    return app


def get_app() -> FastAPI:
    return create_app()

# ДОБАВЛЯЕМ ГЛОБАЛЬНУЮ ПЕРЕМЕННУЮ ДЛЯ UVICORN ===
app = create_app()


if __name__ == "__main__":
    s = get_settings()
    uvicorn.run("app.main:get_app", factory=True, host=s.host, port=s.port)
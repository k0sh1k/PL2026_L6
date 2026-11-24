import logging

import psycopg
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routers import build_router
from app.config import get_settings
from app.domain.errors import DeviceNotFound, DuplicateDevice, InvalidDevice
from app.domain.services import DeviceService
from app.storage.repository import InMemoryDeviceRepository

log = logging.getLogger("storage")


def _error(status: int, code: str):
    # Перевод доменных ошибок в HTTP-ответы
    async def handler(request: Request, exc: Exception):
        log.warning("%s: %s", code, exc)
        return JSONResponse(status_code=status, content={"error": code, "detail": str(exc)})

    return handler


def create_app() -> FastAPI:
    settings = get_settings()
    logging.basicConfig(level=settings.log_level)

    try:
        with psycopg.connect(settings.database_url):
            log.info("Successfully connected to PostgreSQL")
    except Exception as e:
        log.error(f"Failed to connect to DB: {e}")
        # Если базы нет, приложение упадет (так и должно быть)
        raise
    
    service = DeviceService(InMemoryDeviceRepository())

    app = FastAPI(title="storage")

    # === ДОБАВЛЯЕМ HEALTHCHECK СЮДА ===
    @app.get("/health")
    def health():
        return {"status": "ok"}
    # ===================================

    app.include_router(build_router(service))
    app.add_exception_handler(DeviceNotFound, _error(404, "device_not_found"))
    app.add_exception_handler(DuplicateDevice, _error(409, "duplicate_device"))
    app.add_exception_handler(InvalidDevice, _error(422, "invalid_device"))
    return app


app = create_app()

if __name__ == "__main__":
    s = get_settings()
    uvicorn.run("app.main:app", host=s.host, port=s.port)
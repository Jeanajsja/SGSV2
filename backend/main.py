import os
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controllers.vista_controller import router as vista_router
from controllers.usuario_controller import router as usuario_router
from controllers.docente_controller import router as docente_router
from controllers.reserva_controller import router as reserva_router
from controllers.salon_controller import router as salon_router
from controllers.rol_controller import router as rol_router

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.abspath(os.path.join(BASE_DIR, "../frontend/static"))


def _cors_origins():
    raw = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:8080,http://127.0.0.1:8080")
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


def create_app() -> FastAPI:
    application = FastAPI(title="SGSDev", description="Sistema de Gestión de Salones")
    application.add_middleware(
        CORSMiddleware,
        allow_origins=_cors_origins(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.include_router(vista_router)
    application.include_router(usuario_router)
    application.include_router(docente_router)
    application.include_router(reserva_router)
    application.include_router(salon_router)
    application.include_router(rol_router)
    application.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    return application


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)


import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db_config import get_connection
from repositories.postgres_reserva_repository import PostgresReservaRepository
from reserva_controller import crear_router
from reserva_service import ReservaService


def _cors_origins():
    raw = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:8080,http://127.0.0.1:8080")
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


def create_app(service=None):
    if service is None:
        service = ReservaService(PostgresReservaRepository(get_connection))
    app = FastAPI(title="ms-reservas")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=_cors_origins(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    def health():
        return {"status": "ok", "service": "ms-reservas"}

    app.include_router(crear_router(service))
    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=int(os.getenv("PORT", 5006)), reload=True)

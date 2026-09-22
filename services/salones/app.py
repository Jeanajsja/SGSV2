import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db_config import get_connection
from repositories.postgres_salon_repository import PostgresSalonRepository
from salon_controller import crear_router
from salon_service import SalonService


def create_app(service=None):
    if service is None:
        service = SalonService(PostgresSalonRepository(get_connection))
    app = FastAPI(title="ms-salones")
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

    @app.get("/health")
    def health():
        return {"status": "ok", "service": "ms-salones"}

    app.include_router(crear_router(service))
    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=int(os.getenv("PORT", 5002)), reload=True)

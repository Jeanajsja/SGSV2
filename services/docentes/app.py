import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db_config import get_connection
from docente_controller import crear_router
from docente_service import DocenteService
from dominio_email_validator import DominioEmailValidator
from repositories.postgres_docente_repository import PostgresDocenteRepository
from security.werkzeug_password_hasher import WerkzeugPasswordHasher


def create_app(service=None):
    if service is None:
        service = DocenteService(
            PostgresDocenteRepository(get_connection),
            WerkzeugPasswordHasher(),
            DominioEmailValidator(),
        )
    app = FastAPI(title="ms-docentes")
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

    @app.get("/health")
    def health():
        return {"status": "ok", "service": "ms-docentes"}

    app.include_router(crear_router(service))
    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=int(os.getenv("PORT", 5003)), reload=True)

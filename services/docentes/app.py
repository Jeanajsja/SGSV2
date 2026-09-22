import os

from db_config import get_connection
from docente_controller import crear_router
from docente_service import DocenteService
from dominio_email_validator import DominioEmailValidator
from repositories.postgres_docente_repository import PostgresDocenteRepository
from security.werkzeug_password_hasher import WerkzeugPasswordHasher
from shared.app_factory import create_service_app


def create_app(service=None):
    if service is None:
        service = DocenteService(
            PostgresDocenteRepository(get_connection),
            WerkzeugPasswordHasher(),
            DominioEmailValidator(),
        )
    return create_service_app("docentes", crear_router(service), health_service_name="ms-docentes")


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=int(os.getenv("PORT", 5003)), reload=True)

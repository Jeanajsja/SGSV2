import os

from db_config import get_connection
from repositories.postgres_rol_repository import PostgresRolRepository
from rol_controller import crear_router
from rol_service import RolService
from shared.app_factory import create_service_app


def create_app(service=None):
    if service is None:
        service = RolService(PostgresRolRepository(get_connection))
    return create_service_app("roles", crear_router(service), health_service_name="ms-roles")


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=int(os.getenv("PORT", 5004)), reload=True)

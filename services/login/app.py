import os

from db_config import get_connection
from login_controller import crear_router
from login_service import LoginService
from repositories.postgres_login_repository import PostgresLoginRepository
from security.werkzeug_password_hasher import WerkzeugPasswordHasher
from seed_superadmin import asegurar_superadmin
from shared.app_factory import create_service_app


def create_app(service=None):
    asegurar_superadmin(get_connection)
    if service is None:
        service = LoginService(PostgresLoginRepository(get_connection), WerkzeugPasswordHasher())

    return create_service_app("login", crear_router(service), health_service_name="ms-login")


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=int(os.getenv("PORT", 5001)), reload=True)

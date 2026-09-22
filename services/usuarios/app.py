import os

from db_config import get_connection
from dominio_email_validator import DominioEmailValidator
from repositories.postgres_usuario_repository import PostgresUsuarioRepository
from security.werkzeug_password_hasher import WerkzeugPasswordHasher
from seed_superadmin import asegurar_superadmin
from shared.app_factory import create_service_app
from usuario_controller import crear_router
from usuario_service import UsuarioService


def create_app(service=None):
    asegurar_superadmin(get_connection)
    if service is None:
        service = UsuarioService(
            PostgresUsuarioRepository(get_connection),
            WerkzeugPasswordHasher(),
            DominioEmailValidator(),
        )
    return create_service_app("usuarios", crear_router(service), health_service_name="ms-usuarios")


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=int(os.getenv("PORT", 5005)), reload=True)

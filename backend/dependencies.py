from database.db_config import get_connection
from repositories.postgres_docente_repository import PostgresDocenteRepository
from repositories.postgres_reserva_repository import PostgresReservaRepository
from repositories.postgres_rol_repository import PostgresRolRepository
from repositories.postgres_salon_repository import PostgresSalonRepository
from repositories.postgres_usuario_repository import PostgresUsuarioRepository
from security.werkzeug_password_hasher import WerkzeugPasswordHasher
from services.docente_service import DocenteService
from services.dominio_email_validator import DominioEmailValidator
from services.login_service import LoginService
from services.reserva_service import ReservaService
from services.rol_service import RolService
from services.salon_service import SalonService
from services.usuario_service import UsuarioService


def get_login_service() -> LoginService:
    return LoginService(PostgresUsuarioRepository(get_connection), WerkzeugPasswordHasher())


def get_usuario_service() -> UsuarioService:
    return UsuarioService(
        PostgresUsuarioRepository(get_connection),
        WerkzeugPasswordHasher(),
        DominioEmailValidator(),
    )


def get_salon_service() -> SalonService:
    return SalonService(PostgresSalonRepository(get_connection))


def get_reserva_service() -> ReservaService:
    return ReservaService(PostgresReservaRepository(get_connection))


def get_docente_service() -> DocenteService:
    return DocenteService(
        PostgresDocenteRepository(get_connection),
        WerkzeugPasswordHasher(),
        DominioEmailValidator(),
    )


def get_rol_service() -> RolService:
    return RolService(PostgresRolRepository(get_connection))

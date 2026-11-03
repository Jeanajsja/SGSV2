import os

from db_config import get_connection
from repositories.postgres_reserva_repository import PostgresReservaRepository
from reserva_controller import crear_router
from reserva_service import ReservaService
from shared.app_factory import create_service_app


def create_app(service=None):
    if service is None:
        service = ReservaService(PostgresReservaRepository(get_connection))
    return create_service_app("reservas", crear_router(service), health_service_name="ms-reservas")


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=int(os.getenv("PORT", 5006)), reload=True)

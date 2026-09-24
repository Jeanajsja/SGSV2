import os

from db_config import get_connection
from repositories.postgres_salon_repository import PostgresSalonRepository
from salon_controller import crear_router
from salon_service import SalonService
from shared.app_factory import create_service_app


def create_app(service=None):
    if service is None:
        service = SalonService(PostgresSalonRepository(get_connection))
    return create_service_app("salones", crear_router(service), health_service_name="ms-salones")


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=int(os.getenv("PORT", 5002)), reload=True)

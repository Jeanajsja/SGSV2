from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from rol_service import RolService


def crear_router(service: RolService) -> APIRouter:
    router = APIRouter(prefix="/api", tags=["roles"])

    @router.get("/roles")
    def get_roles():
        return jsonable_encoder(service.listar())

    return router

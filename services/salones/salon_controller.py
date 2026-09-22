from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from salon_service import SalonService


class SalonPayload(BaseModel):
    nombre: str
    capacidad: int
    ubicacion: str


def crear_router(service: SalonService) -> APIRouter:
    router = APIRouter(prefix="/api", tags=["salones"])

    @router.get("/salones")
    def get_salones():
        return {"status": "ok", "data": jsonable_encoder(service.listar())}

    @router.post("/salones")
    def crear(payload: SalonPayload):
        return service.crear(payload.model_dump())

    @router.put("/salones/{id_salon}")
    def editar(id_salon: int, payload: SalonPayload):
        return service.actualizar(id_salon, payload.model_dump())

    return router

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from schemas import SalonPayload
from dependencies import get_salon_service
from services.salon_service import SalonService

router = APIRouter(prefix="/api", tags=["salones"])


@router.get("/salones")
def get_salones(service: SalonService = Depends(get_salon_service)):
    return {"status": "ok", "data": jsonable_encoder(service.listar())}


@router.post("/salones")
def crear(payload: SalonPayload, service: SalonService = Depends(get_salon_service)):
    return service.crear(payload.model_dump())


@router.put("/salones/{id_salon}")
def editar(id_salon: int, payload: SalonPayload, service: SalonService = Depends(get_salon_service)):
    return service.actualizar(id_salon, payload.model_dump())

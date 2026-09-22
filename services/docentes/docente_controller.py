from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from typing import Optional
from docente_service import DocenteService


class DocenteCreate(BaseModel):
    nombre: str
    correo: str
    telefono: Optional[str] = Field(default=None)


def crear_router(service: DocenteService) -> APIRouter:
    router = APIRouter(prefix="/api", tags=["docentes"])

    @router.get("/docentes")
    def listar():
        return {"status": "ok", "data": jsonable_encoder(service.listar())}

    @router.post("/docentes")
    def crear(payload: DocenteCreate):
        return service.crear(payload.model_dump())

    return router

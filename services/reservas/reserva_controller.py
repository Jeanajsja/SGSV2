from typing import Optional
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from reserva_service import ReservaService


class ReservaPayload(BaseModel):
    fecha: str
    hora_inicio: str
    hora_fin: Optional[str] = None
    id_salon: int
    id_docente: int


def crear_router(service: ReservaService) -> APIRouter:
    router = APIRouter(prefix="/api", tags=["reservas"])

    @router.get("/reservas")
    def listar():
        res = service.listar()
        if res.get("status") != "ok":
            return JSONResponse(content={"status": "error", "message": res.get("message")}, status_code=500)
        return {"status": "ok", "data": jsonable_encoder(res.get("data"))}

    @router.post("/reservas")
    def crear(payload: ReservaPayload):
        return service.crear_reserva(payload.model_dump())

    @router.put("/reservas/{id_reserva}")
    def actualizar(id_reserva: int, payload: ReservaPayload):
        return service.actualizar_reserva(id_reserva, payload.model_dump())

    @router.delete("/reservas/{id_reserva}")
    def cancelar(id_reserva: int):
        return service.cancelar_reserva(id_reserva)

    return router

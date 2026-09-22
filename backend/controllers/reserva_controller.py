from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from dependencies import get_reserva_service
from schemas import ReservaPayload
from services.reserva_service import ReservaService

router = APIRouter(prefix="/api", tags=["reservas"])


@router.get("/reservas")
def listar(service: ReservaService = Depends(get_reserva_service)):
    res = service.listar()
    if res.get("status") != "ok":
        return JSONResponse(content={"status": "error", "message": res.get("message")}, status_code=500)
    return {"status": "ok", "data": jsonable_encoder(res.get("data"))}


@router.post("/reservas")
def crear(payload: ReservaPayload, service: ReservaService = Depends(get_reserva_service)):
    return service.crear_reserva(payload.model_dump())


@router.put("/reservas/{id_reserva}")
def actualizar(id_reserva: int, payload: ReservaPayload, service: ReservaService = Depends(get_reserva_service)):
    return service.actualizar_reserva(id_reserva, payload.model_dump())


@router.delete("/reservas/{id_reserva}")
def cancelar(id_reserva: int, service: ReservaService = Depends(get_reserva_service)):
    return service.cancelar_reserva(id_reserva)

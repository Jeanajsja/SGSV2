from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from dependencies import get_docente_service
from schemas import DocenteCreate
from services.docente_service import DocenteService

router = APIRouter(prefix="/api", tags=["docentes"])


@router.get("/docentes")
def listar(service: DocenteService = Depends(get_docente_service)):
    return {"status": "ok", "data": jsonable_encoder(service.listar())}


@router.post("/docentes")
def crear(payload: DocenteCreate, service: DocenteService = Depends(get_docente_service)):
    return service.crear(payload.model_dump())

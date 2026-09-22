from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from dependencies import get_rol_service
from services.rol_service import RolService

router = APIRouter(prefix="/api", tags=["roles"])


@router.get("/roles")
def get_roles(service: RolService = Depends(get_rol_service)):
    return jsonable_encoder(service.listar())

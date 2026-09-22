from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from dependencies import get_login_service, get_usuario_service
from schemas import LoginRequest, UsuarioCreate
from services.login_service import LoginService
from services.usuario_service import UsuarioService

router = APIRouter(prefix="/api", tags=["usuarios"])


@router.post("/login")
def login(payload: LoginRequest, service: LoginService = Depends(get_login_service)):
    res = service.login(payload.email, payload.password)
    if res and res.get("status") == "ok":
        return jsonable_encoder(res)
    return JSONResponse(content=jsonable_encoder(res), status_code=401)


@router.post("/usuarios")
def registrar(payload: UsuarioCreate, service: UsuarioService = Depends(get_usuario_service)):
    res = service.crear_usuario(payload.model_dump())
    if res and res.get("status") == "ok":
        return res
    return JSONResponse(content=res, status_code=400)

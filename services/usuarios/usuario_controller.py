from typing import Optional
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from usuario_service import UsuarioService


class UsuarioCreate(BaseModel):
    nombre: str
    email: str
    password: str
    id_rol: int
    solicitante_email: Optional[str] = None


class UsuarioRolUpdate(BaseModel):
    id_rol: int
    solicitante_email: str


def crear_router(service: UsuarioService) -> APIRouter:
    router = APIRouter(prefix="/api", tags=["usuarios"])

    @router.post("/usuarios")
    def registrar(payload: UsuarioCreate):
        res = service.crear_usuario(payload.model_dump())
        if res and res.get("status") == "ok":
            return res
        return JSONResponse(content=res, status_code=400)

    @router.get("/usuarios")
    def listar():
        res = service.listar_usuarios()
        if res and res.get("status") == "ok":
            return res
        return JSONResponse(content=res, status_code=400)

    @router.put("/usuarios/{id_usuario}")
    def cambiar_rol(id_usuario: int, payload: UsuarioRolUpdate):
        res = service.cambiar_rol(id_usuario, payload.id_rol, payload.solicitante_email)
        if res and res.get("status") == "ok":
            return res
        return JSONResponse(content=res, status_code=400)

    @router.delete("/usuarios/{id_usuario}")
    def eliminar(id_usuario: int, solicitante_email: str = ""):
        res = service.eliminar_cuenta(id_usuario, solicitante_email)
        if res and res.get("status") == "ok":
            return res
        return JSONResponse(content=res, status_code=400)

    return router

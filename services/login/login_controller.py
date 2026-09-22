from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from login_service import LoginService


class LoginRequest(BaseModel):
    email: str
    password: str


def crear_router(service: LoginService) -> APIRouter:
    router = APIRouter(prefix="/api", tags=["login"])

    @router.post("/login")
    def login(payload: LoginRequest):
        res = service.login(payload.email, payload.password)
        if res and res.get("status") == "ok":
            return jsonable_encoder(res)
        return JSONResponse(content=jsonable_encoder(res), status_code=401)

    return router

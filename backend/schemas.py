from typing import Optional
from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    email: str
    password: str


class UsuarioCreate(BaseModel):
    nombre: str
    email: str
    password: str
    id_rol: int
    solicitante_email: Optional[str] = None


class SalonPayload(BaseModel):
    nombre: str
    capacidad: int
    ubicacion: str


class ReservaPayload(BaseModel):
    fecha: str
    hora_inicio: str
    hora_fin: Optional[str] = None
    id_salon: int
    id_docente: int


class DocenteCreate(BaseModel):
    nombre: str
    correo: str
    telefono: Optional[str] = Field(default=None)

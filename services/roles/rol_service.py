from interfaces.rol_repository import IRolRepository
from models.rol import Rol

NOMBRES_ROL = {
    1: "Superadministrador",
    2: "Administrador",
    3: "Docente",
}


class RolService:
    def __init__(self, repository: IRolRepository):
        self._repository = repository

    def listar(self):
        roles = []
        for row in self._repository.listar():
            data = Rol.from_row(row).to_dict()
            if data["id_rol"] in NOMBRES_ROL:
                data["nombre"] = NOMBRES_ROL[data["id_rol"]]
            roles.append(data)
        return roles

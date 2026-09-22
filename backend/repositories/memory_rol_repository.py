from interfaces.rol_repository import IRolRepository


class MemoryRolRepository(IRolRepository):
    def __init__(self, roles=None):
        self._roles = roles or [
            {"id_rol": 1, "nombre": "Superadministrador"},
            {"id_rol": 2, "nombre": "Administrador"},
            {"id_rol": 3, "nombre": "Docente"},
        ]

    def listar(self):
        return list(self._roles)

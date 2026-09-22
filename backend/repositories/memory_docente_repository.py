from interfaces.docente_repository import IDocenteRepository


class MemoryDocenteRepository(IDocenteRepository):
    def __init__(self):
        self._docentes = []
        self._next_id = 1

    def listar(self):
        return list(self._docentes)

    def crear(self, nombre, correo, password_hash):
        self._docentes.append(
            {
                "id_docente": self._next_id,
                "nombre": nombre,
                "correo": correo,
                "telefono": "Sin Teléfono",
                "password": password_hash,
            }
        )
        self._next_id += 1

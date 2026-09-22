from interfaces.login_repository import ILoginRepository
from interfaces.usuario_repository import IUsuarioRepository


class MemoryUsuarioRepository(IUsuarioRepository, ILoginRepository):
    def __init__(self):
        self._usuarios = []
        self._next_id = 1

    def crear(self, nombre, email, password_hash, id_rol):
        if any(u["email"] == email for u in self._usuarios):
            raise Exception("duplicate key")
        self._usuarios.append(
            {
                "id_usuario": self._next_id,
                "nombre": nombre,
                "email": email,
                "password": password_hash,
                "id_rol": id_rol,
            }
        )
        self._next_id += 1

    def listar(self):
        return [self._sin_clave(u) for u in self._usuarios]

    def buscar_por_id(self, id_usuario):
        return next((u.copy() for u in self._usuarios if u["id_usuario"] == id_usuario), None)

    def buscar_por_email(self, email):
        buscado = (email or "").lower()
        return next((u.copy() for u in self._usuarios if u["email"].lower() == buscado), None)

    def actualizar_rol(self, id_usuario, id_rol):
        for usuario in self._usuarios:
            if usuario["id_usuario"] == id_usuario:
                usuario["id_rol"] = id_rol
                return True
        return False

    def eliminar(self, id_usuario):
        antes = len(self._usuarios)
        self._usuarios = [u for u in self._usuarios if u["id_usuario"] != id_usuario]
        return len(self._usuarios) < antes

    def _sin_clave(self, usuario):
        copia = usuario.copy()
        copia.pop("password", None)
        return copia

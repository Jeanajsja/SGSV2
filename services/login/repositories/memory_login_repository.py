from interfaces.login_repository import ILoginRepository


class MemoryLoginRepository(ILoginRepository):
    def __init__(self):
        self._usuarios = []

    def agregar(self, usuario):
        self._usuarios.append(usuario)

    def buscar_por_email(self, email):
        return next((u.copy() for u in self._usuarios if u["email"] == email), None)

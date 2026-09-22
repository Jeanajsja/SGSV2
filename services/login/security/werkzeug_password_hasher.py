from werkzeug.security import check_password_hash
from interfaces.password_hasher import IPasswordHasher


class WerkzeugPasswordHasher(IPasswordHasher):
    def verificar(self, password: str, almacenado: str) -> bool:
        if almacenado == password:
            return True
        try:
            return check_password_hash(almacenado, password)
        except Exception:
            return False

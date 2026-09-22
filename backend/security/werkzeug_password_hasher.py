from werkzeug.security import check_password_hash, generate_password_hash
from interfaces.password_hasher import IPasswordHasher
from interfaces.password_verifier import IPasswordVerifier


class WerkzeugPasswordHasher(IPasswordHasher, IPasswordVerifier):
    def hash(self, password: str) -> str:
        return generate_password_hash(password)

    def verificar(self, password: str, almacenado: str) -> bool:
        if almacenado == password:
            return True
        try:
            return check_password_hash(almacenado, password)
        except Exception:
            return False

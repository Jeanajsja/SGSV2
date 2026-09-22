from werkzeug.security import generate_password_hash
from interfaces.password_hasher import IPasswordHasher


class WerkzeugPasswordHasher(IPasswordHasher):
    def hash(self, password: str) -> str:
        return generate_password_hash(password)

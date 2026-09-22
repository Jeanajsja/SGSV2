from interfaces.login_repository import ILoginRepository
from interfaces.password_hasher import IPasswordHasher
from models.usuario import Usuario


class LoginService:
    def __init__(self, repository: ILoginRepository, password_hasher: IPasswordHasher):
        self._repository = repository
        self._password_hasher = password_hasher

    def login(self, email, password):
        try:
            user = self._repository.buscar_por_email(email)
        except ConnectionError:
            return {"status": "error", "message": "No se pudo conectar a la base de datos de Supabase"}
        except Exception as e:
            return {"status": "error", "message": f"Error en el servidor: {str(e)}"}

        if user and self._password_hasher.verificar(password, user["password"]):
            return {"status": "ok", "user": Usuario.from_row(user).to_public_dict()}
        return {"status": "error", "message": "Credenciales inválidas"}

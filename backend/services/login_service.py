from interfaces.login_repository import ILoginRepository
from interfaces.password_verifier import IPasswordVerifier
from models.usuario_factory import usuario_desde_fila


class LoginService:
    def __init__(self, repository: ILoginRepository, password_verifier: IPasswordVerifier):
        self._repository = repository
        self._password_verifier = password_verifier

    def login(self, email, password):
        try:
            user = self._repository.buscar_por_email(email)
        except ConnectionError:
            return {"status": "error", "message": "No se pudo conectar a la base de datos de Supabase"}
        except Exception as e:
            return {"status": "error", "message": f"Error en el servidor: {str(e)}"}

        if user and self._password_verifier.verificar(password, user["password"]):
            return {"status": "ok", "user": usuario_desde_fila(user).to_public_dict()}
        return {"status": "error", "message": "Credenciales inválidas"}

from interfaces.docente_repository import IDocenteRepository
from interfaces.email_validator import IEmailValidator
from interfaces.password_hasher import IPasswordHasher
from models.docente import Docente


class DocenteService:
    def __init__(self, repository: IDocenteRepository, password_hasher: IPasswordHasher, email_validator: IEmailValidator):
        self._repository = repository
        self._password_hasher = password_hasher
        self._email_validator = email_validator

    def listar(self):
        try:
            return [Docente.from_row(row).to_dict() for row in self._repository.listar()]
        except ConnectionError:
            return []

    def crear(self, data):
        if not data:
            return {"status": "error", "message": "Datos del docente requeridos"}

        nombre = str(data.get("nombre", "")).strip()
        correo = str(data.get("correo", "")).strip()
        if not nombre or not correo:
            return {"status": "error", "message": "Los campos 'nombre' y 'correo' son obligatorios."}

        error = self._email_validator.validar(correo)
        if error:
            return error

        try:
            password_defecto = self._password_hasher.hash("docente123")
            self._repository.crear(nombre, correo, password_defecto)
        except ConnectionError:
            return {"status": "error", "message": "Error de conexión"}
        except Exception as exc:
            return {"status": "error", "message": f"Error al registrar docente: {str(exc)}"}
        return {"status": "ok", "message": "Docente registrado con éxito. Contraseña por defecto: docente123"}

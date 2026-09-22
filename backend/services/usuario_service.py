from interfaces.email_validator import IEmailValidator
from interfaces.password_hasher import IPasswordHasher
from interfaces.usuario_repository import IUsuarioRepository

SUPERADMIN_ANCLA = "lfpaez30@ucatolica.edu.co"
ROL_SUPERADMIN = 1
ROLES_VALIDOS = {1, 2, 3}


class UsuarioService:
    def __init__(self, repository: IUsuarioRepository, password_hasher: IPasswordHasher, email_validator: IEmailValidator):
        self._repository = repository
        self._password_hasher = password_hasher
        self._email_validator = email_validator

    def crear_usuario(self, data):
        error = self._email_validator.validar(data.get("email", ""))
        if error:
            return error
        try:
            id_rol = int(data["id_rol"])
        except (TypeError, ValueError):
            return {"status": "error", "message": "El rol no es válido"}
        if id_rol == ROL_SUPERADMIN:
            solicitante = (data.get("solicitante_email") or "").lower()
            if solicitante != SUPERADMIN_ANCLA:
                return {
                    "status": "error",
                    "message": "Solo el superadministrador ancla puede crear otro superadministrador",
                }
        try:
            password_segura = self._password_hasher.hash(data["password"])
            self._repository.crear(data["nombre"], data["email"], password_segura, id_rol)
        except ConnectionError:
            return {"status": "error", "message": "Error de conexión"}
        except Exception as e:
            return {"status": "error", "message": f"El correo ya existe o hay un error: {str(e)}"}
        return {"status": "ok", "message": "Cuenta creada exitosamente"}

    def listar_usuarios(self):
        try:
            return {"status": "ok", "data": [self._publico(u) for u in self._repository.listar()]}
        except ConnectionError:
            return {"status": "error", "message": "Error de conexión", "data": []}

    def cambiar_rol(self, id_usuario, id_rol, solicitante_email):
        solicitante = self._exigir_superadmin(solicitante_email)
        if isinstance(solicitante, dict) and solicitante.get("status") == "error":
            return solicitante
        try:
            nuevo_rol = int(id_rol)
        except (TypeError, ValueError):
            return {"status": "error", "message": "El rol no es válido"}
        if nuevo_rol not in ROLES_VALIDOS:
            return {"status": "error", "message": "El rol no es válido"}
        objetivo = self._repository.buscar_por_id(id_usuario)
        if not objetivo:
            return {"status": "error", "message": "La cuenta no existe"}
        if self._es_ancla(objetivo):
            return {"status": "error", "message": "El superadministrador ancla no se puede modificar"}
        if nuevo_rol == ROL_SUPERADMIN and not self._es_ancla(solicitante):
            return {
                "status": "error",
                "message": "Solo el superadministrador ancla puede asignar el rol de superadministrador",
            }
        try:
            self._repository.actualizar_rol(id_usuario, nuevo_rol)
        except ConnectionError:
            return {"status": "error", "message": "Error de conexión"}
        except Exception as e:
            return {"status": "error", "message": f"No se pudo cambiar el rol: {str(e)}"}
        return {"status": "ok", "message": "Rol actualizado"}

    def eliminar_cuenta(self, id_usuario, solicitante_email):
        solicitante = self._exigir_superadmin(solicitante_email)
        if isinstance(solicitante, dict) and solicitante.get("status") == "error":
            return solicitante
        objetivo = self._repository.buscar_por_id(id_usuario)
        if not objetivo:
            return {"status": "error", "message": "La cuenta no existe"}
        if self._es_ancla(objetivo):
            return {"status": "error", "message": "El superadministrador ancla no se puede eliminar"}
        if (objetivo.get("email") or "").lower() == (solicitante.get("email") or "").lower():
            return {"status": "error", "message": "No puedes eliminar tu propia cuenta"}
        try:
            self._repository.eliminar(id_usuario)
        except ConnectionError:
            return {"status": "error", "message": "Error de conexión"}
        except Exception as e:
            return {"status": "error", "message": f"No se pudo eliminar la cuenta: {str(e)}"}
        return {"status": "ok", "message": "Cuenta eliminada"}

    def _exigir_superadmin(self, email):
        if not email:
            return {"status": "error", "message": "Solo un superadministrador puede gestionar cuentas"}
        solicitante = self._repository.buscar_por_email(email)
        if not solicitante or int(solicitante.get("id_rol") or 0) != ROL_SUPERADMIN:
            return {"status": "error", "message": "Solo un superadministrador puede gestionar cuentas"}
        return solicitante

    def _es_ancla(self, usuario):
        return (usuario.get("email") or "").lower() == SUPERADMIN_ANCLA

    def _publico(self, usuario):
        return {
            "id_usuario": usuario["id_usuario"],
            "nombre": usuario["nombre"],
            "email": usuario["email"],
            "id_rol": usuario["id_rol"],
        }

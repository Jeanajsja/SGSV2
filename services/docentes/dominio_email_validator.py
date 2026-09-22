from interfaces.email_validator import IEmailValidator
from validador_correo import validar_dominio_email


class DominioEmailValidator(IEmailValidator):
    def validar(self, email):
        return validar_dominio_email(email)

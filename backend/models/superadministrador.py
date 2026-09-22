from models.usuario import Usuario


class Superadministrador(Usuario):
    def etiqueta(self):
        return f"Superadministrador {self.nombre}"

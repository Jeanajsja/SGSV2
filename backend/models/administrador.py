from models.usuario import Usuario


class Administrador(Usuario):
    def etiqueta(self):
        return f"Administrador {self.nombre}"

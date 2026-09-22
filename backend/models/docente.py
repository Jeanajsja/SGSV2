class Docente:

    def __init__(self, id_docente=None, nombre=None, correo=None, telefono=None):
        self.id_docente = id_docente
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @classmethod
    def from_row(cls, row):
        data = dict(row)
        return cls(
            id_docente=data.get("id_docente"),
            nombre=data.get("nombre"),
            correo=data.get("correo"),
            telefono=data.get("telefono"),
        )

    def to_dict(self):
        return {
            "id_docente": self.id_docente,
            "nombre": self.nombre,
            "correo": self.correo,
            "telefono": self.telefono,
        }

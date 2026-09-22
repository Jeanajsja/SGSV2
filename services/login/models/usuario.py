class Usuario:
    def __init__(self, id_usuario=None, nombre=None, email=None, password=None, id_rol=None):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.email = email
        self.password = password
        self.id_rol = id_rol

    @classmethod
    def from_row(cls, row):
        data = dict(row)
        return cls(
            id_usuario=data.get("id_usuario"),
            nombre=data.get("nombre"),
            email=data.get("email"),
            password=data.get("password"),
            id_rol=data.get("id_rol"),
        )

    def to_public_dict(self):
        return {
            "id_usuario": self.id_usuario,
            "nombre": self.nombre,
            "email": self.email,
            "id_rol": self.id_rol,
        }

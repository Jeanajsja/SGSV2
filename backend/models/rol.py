class Rol:

    def __init__(self, id_rol=None, nombre=None):
        self.id_rol = id_rol
        self.nombre = nombre

    @classmethod
    def from_row(cls, row):
        data = dict(row)
        return cls(id_rol=data.get("id_rol"), nombre=data.get("nombre"))

    def to_dict(self):
        return {"id_rol": self.id_rol, "nombre": self.nombre}

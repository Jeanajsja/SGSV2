class Salon:

    def __init__(self, id_salon=None, nombre=None, capacidad=None, estado=None, ubicacion=None):
        self.id_salon = id_salon
        self.nombre = nombre
        self.capacidad = capacidad
        self.estado = estado
        self.ubicacion = ubicacion

    @classmethod
    def from_row(cls, row):
        data = dict(row)
        return cls(
            id_salon=data.get("id_salon"),
            nombre=data.get("nombre"),
            capacidad=data.get("capacidad"),
            estado=data.get("estado"),
            ubicacion=data.get("ubicacion"),
        )

    def to_dict(self):
        return {
            "id_salon": self.id_salon,
            "nombre": self.nombre,
            "capacidad": self.capacidad,
            "estado": self.estado,
            "ubicacion": self.ubicacion,
        }

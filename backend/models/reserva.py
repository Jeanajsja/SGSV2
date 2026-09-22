class Reserva:

    def __init__(self, id_reserva=None, fecha=None, hora_inicio=None, hora_fin=None, estado=None, id_docente=None, id_salon=None):
        self.id_reserva = id_reserva
        self.fecha = fecha
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.estado = estado
        self.id_docente = id_docente
        self.id_salon = id_salon

    @classmethod
    def from_row(cls, row):
        data = dict(row)
        return cls(
            id_reserva=data.get("id_reserva"),
            fecha=data.get("fecha"),
            hora_inicio=data.get("hora_inicio"),
            hora_fin=data.get("hora_fin"),
            estado=data.get("estado"),
            id_docente=data.get("id_docente"),
            id_salon=data.get("id_salon"),
        )

    def to_dict(self):
        return {
            "id_reserva": self.id_reserva,
            "fecha": self.fecha,
            "hora_inicio": self.hora_inicio,
            "hora_fin": self.hora_fin,
            "estado": self.estado,
            "id_docente": self.id_docente,
            "id_salon": self.id_salon,
        }

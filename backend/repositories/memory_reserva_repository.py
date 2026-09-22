from interfaces.reserva_repository import IReservaRepository


class MemoryReservaRepository(IReservaRepository):
    def __init__(self):
        self._reservas = []
        self._cola = []
        self._next_id = 1
        self._next_cola = 1

    def listar_detalle(self):
        return list(self._reservas)

    def existe_cruce(self, id_salon, fecha, hora_inicio, hora_fin):
        for r in self._reservas:
            if r["id_salon"] != id_salon or r["fecha"] != fecha or r["estado"] == "cancelada":
                continue
            if r["hora_inicio"] < hora_fin and r["hora_fin"] > hora_inicio:
                return True
        return False

    def crear(self, fecha, hora_inicio, hora_fin, id_docente, id_salon):
        self._reservas.append(
            {
                "id_reserva": self._next_id,
                "fecha": fecha,
                "hora_inicio": hora_inicio,
                "hora_fin": hora_fin,
                "estado": "confirmada",
                "id_docente": id_docente,
                "id_salon": id_salon,
                "docente": "Docente",
                "salon": f"Salon {id_salon}",
            }
        )
        self._next_id += 1

    def actualizar(self, id_reserva, fecha, hora_inicio, hora_fin, id_salon, id_docente):
        for r in self._reservas:
            if r["id_reserva"] == id_reserva:
                r["fecha"] = fecha
                r["hora_inicio"] = hora_inicio
                r["hora_fin"] = hora_fin
                r["id_salon"] = id_salon
                r["id_docente"] = id_docente
                return

    def cancelar(self, id_reserva):
        for r in self._reservas:
            if r["id_reserva"] == id_reserva:
                r["estado"] = "cancelada"
                return r["id_salon"]
        return None

    def encolar(self, id_salon, id_docente):
        self._cola.append({"id_cola": self._next_cola, "id_salon": id_salon, "id_docente": id_docente})
        self._next_cola += 1

    def promover_siguiente_cola(self, id_salon):
        for i, item in enumerate(self._cola):
            if item["id_salon"] == id_salon:
                self._cola.pop(i)
                return

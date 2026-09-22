from datetime import datetime, timedelta
from interfaces.reserva_repository import IReservaRepository


class ReservaService:

    def __init__(self, repository: IReservaRepository):
        self._repository = repository

    def listar(self):
        try:
            return {"status": "ok", "data": self._repository.listar_detalle()}
        except ConnectionError as e:
            return {"status": "error", "message": str(e)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def crear_reserva(self, data):
        h_ini = data["hora_inicio"]
        h_fin = data.get("hora_fin")
        if not h_fin:
            try:
                t_ini = datetime.strptime(h_ini, "%H:%M")
                h_fin = (t_ini + timedelta(hours=2)).strftime("%H:%M")
            except Exception:
                h_fin = "22:00"

        if self._repository.existe_cruce(data["id_salon"], data["fecha"], h_ini, h_fin):
            return self._suscribir_a_cola(data["id_salon"], data["id_docente"])

        try:
            self._repository.crear(data["fecha"], h_ini, h_fin, data["id_docente"], data["id_salon"])
        except ConnectionError:
            return {"status": "error", "message": "Error de conexión"}
        except Exception as e:
            return {"status": "error", "message": f"Error al crear reserva: {str(e)}"}
        return {"status": "ok", "message": "Reserva confirmada en Supabase"}

    def actualizar_reserva(self, id_reserva, data):
        try:
            self._repository.actualizar(
                id_reserva,
                data["fecha"],
                data["hora_inicio"],
                data["hora_fin"],
                data["id_salon"],
                data["id_docente"],
            )
        except ConnectionError:
            return {"status": "error", "message": "Error de conexión"}
        except Exception as e:
            return {"status": "error", "message": f"Error al actualizar reserva: {str(e)}"}
        return {"status": "ok", "message": "Reserva actualizada con éxito"}

    def cancelar_reserva(self, id_reserva):
        try:
            id_salon = self._repository.cancelar(id_reserva)
            if id_salon is not None:
                self._repository.promover_siguiente_cola(id_salon)
        except ConnectionError:
            return {"status": "error", "message": "Error de conexión"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
        return {"status": "ok"}

    def _suscribir_a_cola(self, id_salon, id_docente):
        try:
            self._repository.encolar(id_salon, id_docente)
        except ConnectionError:
            return {"status": "error", "message": "Error de conexión"}
        except Exception as e:
            return {"status": "error", "message": f"Error al ingresar a cola: {str(e)}"}
        return {"status": "cola", "message": "Añadido a lista de espera FIFO"}

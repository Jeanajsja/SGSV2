from abc import ABC, abstractmethod


class IReservaRepository(ABC):
    @abstractmethod
    def listar_detalle(self):
        pass

    @abstractmethod
    def existe_cruce(self, id_salon, fecha, hora_inicio, hora_fin):
        pass

    @abstractmethod
    def crear(self, fecha, hora_inicio, hora_fin, id_docente, id_salon):
        pass

    @abstractmethod
    def actualizar(self, id_reserva, fecha, hora_inicio, hora_fin, id_salon, id_docente):
        pass

    @abstractmethod
    def cancelar(self, id_reserva):
        pass

    @abstractmethod
    def encolar(self, id_salon, id_docente):
        pass

    @abstractmethod
    def promover_siguiente_cola(self, id_salon):
        pass

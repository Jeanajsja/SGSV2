from abc import ABC, abstractmethod


class ISalonRepository(ABC):

    @abstractmethod
    def listar(self):
        pass

    @abstractmethod
    def crear(self, nombre, capacidad, ubicacion):
        pass

    @abstractmethod
    def actualizar(self, id_salon, nombre, capacidad, ubicacion):
        pass

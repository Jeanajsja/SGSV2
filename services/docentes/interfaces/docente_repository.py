from abc import ABC, abstractmethod


class IDocenteRepository(ABC):
    @abstractmethod
    def listar(self):
        pass

    @abstractmethod
    def crear(self, nombre, correo, password_hash):
        pass

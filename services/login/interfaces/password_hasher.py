from abc import ABC, abstractmethod


class IPasswordHasher(ABC):
    @abstractmethod
    def verificar(self, password: str, almacenado: str) -> bool:
        pass

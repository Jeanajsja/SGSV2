from abc import ABC, abstractmethod


class IPasswordVerifier(ABC):
    @abstractmethod
    def verificar(self, password: str, almacenado: str) -> bool:
        pass

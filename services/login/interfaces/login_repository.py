from abc import ABC, abstractmethod


class ILoginRepository(ABC):
    @abstractmethod
    def buscar_por_email(self, email):
        pass

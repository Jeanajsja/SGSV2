from abc import ABC, abstractmethod


class IEmailValidator(ABC):
    @abstractmethod
    def validar(self, email):
        pass

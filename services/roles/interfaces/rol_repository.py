from abc import ABC, abstractmethod


class IRolRepository(ABC):
    @abstractmethod
    def listar(self):
        pass

from abc import ABC, abstractmethod


class IUsuarioRepository(ABC):
    @abstractmethod
    def crear(self, nombre, email, password_hash, id_rol):
        pass

    @abstractmethod
    def listar(self):
        pass

    @abstractmethod
    def buscar_por_id(self, id_usuario):
        pass

    @abstractmethod
    def buscar_por_email(self, email):
        pass

    @abstractmethod
    def actualizar_rol(self, id_usuario, id_rol):
        pass

    @abstractmethod
    def eliminar(self, id_usuario):
        pass

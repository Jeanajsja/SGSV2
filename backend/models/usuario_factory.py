from models.administrador import Administrador
from models.superadministrador import Superadministrador
from models.usuario import Usuario


def usuario_desde_fila(row):
    data = dict(row)
    rol = data.get("id_rol")
    if rol == 1:
        return Superadministrador.from_row(data)
    if rol == 2:
        return Administrador.from_row(data)
    return Usuario.from_row(data)

from psycopg2.extras import RealDictCursor
from interfaces.docente_repository import IDocenteRepository


class PostgresDocenteRepository(IDocenteRepository):
    def __init__(self, connection_factory):
        self._connection_factory = connection_factory

    def listar(self):
        conn = self._connection_factory()
        if conn is None:
            return []
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(
                """
                SELECT id_usuario as id_docente, nombre, email as correo, 'Sin Teléfono' as telefono
                FROM usuario
                WHERE id_rol = 3
                ORDER BY nombre ASC
                """
            )
            return cursor.fetchall()
        except Exception:
            return []
        finally:
            conn.close()

    def crear(self, nombre, correo, password_hash):
        conn = self._connection_factory()
        if conn is None:
            raise ConnectionError("No se pudo conectar a la base de datos")
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO usuario (nombre, email, password, id_rol)
                VALUES (%s, %s, %s, 3)
                """,
                (nombre, correo, password_hash),
            )
            conn.commit()
        finally:
            conn.close()

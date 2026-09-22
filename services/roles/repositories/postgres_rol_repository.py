from psycopg2.extras import RealDictCursor
from interfaces.rol_repository import IRolRepository


class PostgresRolRepository(IRolRepository):
    def __init__(self, connection_factory):
        self._connection_factory = connection_factory

    def listar(self):
        conn = self._connection_factory()
        if conn is None:
            return []
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT * FROM Rol")
            return cursor.fetchall()
        finally:
            conn.close()

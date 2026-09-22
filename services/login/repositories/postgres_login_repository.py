from psycopg2.extras import RealDictCursor
from interfaces.login_repository import ILoginRepository


class PostgresLoginRepository(ILoginRepository):
    def __init__(self, connection_factory):
        self._connection_factory = connection_factory

    def buscar_por_email(self, email):
        conn = self._connection_factory()
        if conn is None:
            raise ConnectionError("No se pudo conectar a la base de datos de Supabase")
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT * FROM usuario WHERE email = %s", (email,))
            return cursor.fetchone()
        finally:
            conn.close()

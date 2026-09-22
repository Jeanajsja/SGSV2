from psycopg2.extras import RealDictCursor
from interfaces.login_repository import ILoginRepository
from interfaces.usuario_repository import IUsuarioRepository


class PostgresUsuarioRepository(IUsuarioRepository, ILoginRepository):
    def __init__(self, connection_factory):
        self._connection_factory = connection_factory

    def crear(self, nombre, email, password_hash, id_rol):
        conn = self._connection_factory()
        if conn is None:
            raise ConnectionError("No se pudo conectar a la base de datos")
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO usuario (nombre, email, password, id_rol)
                VALUES (%s, %s, %s, %s)
                """,
                (nombre, email, password_hash, id_rol),
            )
            conn.commit()
        finally:
            conn.close()

    def listar(self):
        conn = self._connection_factory()
        if conn is None:
            raise ConnectionError("No se pudo conectar a la base de datos")
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(
                "SELECT id_usuario, nombre, email, id_rol FROM usuario ORDER BY id_usuario"
            )
            return cursor.fetchall()
        finally:
            conn.close()

    def buscar_por_id(self, id_usuario):
        conn = self._connection_factory()
        if conn is None:
            raise ConnectionError("No se pudo conectar a la base de datos")
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(
                "SELECT id_usuario, nombre, email, id_rol FROM usuario WHERE id_usuario = %s",
                (id_usuario,),
            )
            return cursor.fetchone()
        finally:
            conn.close()

    def buscar_por_email(self, email):
        conn = self._connection_factory()
        if conn is None:
            raise ConnectionError("No se pudo conectar a la base de datos de Supabase")
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(
                "SELECT * FROM usuario WHERE lower(email) = lower(%s)",
                (email,),
            )
            return cursor.fetchone()
        finally:
            conn.close()

    def actualizar_rol(self, id_usuario, id_rol):
        conn = self._connection_factory()
        if conn is None:
            raise ConnectionError("No se pudo conectar a la base de datos")
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE usuario SET id_rol = %s WHERE id_usuario = %s",
                (id_rol, id_usuario),
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    def eliminar(self, id_usuario):
        conn = self._connection_factory()
        if conn is None:
            raise ConnectionError("No se pudo conectar a la base de datos")
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM cola_espera WHERE id_docente = %s", (id_usuario,))
            cursor.execute("DELETE FROM reserva WHERE id_docente = %s", (id_usuario,))
            cursor.execute("DELETE FROM usuario WHERE id_usuario = %s", (id_usuario,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

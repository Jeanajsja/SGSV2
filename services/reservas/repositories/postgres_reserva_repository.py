from psycopg2.extras import RealDictCursor
from interfaces.reserva_repository import IReservaRepository


class PostgresReservaRepository(IReservaRepository):
    def __init__(self, connection_factory):
        self._connection_factory = connection_factory

    def listar_detalle(self):
        conn = self._connection_factory()
        if conn is None:
            raise ConnectionError("No se pudo conectar a la base de datos")
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(
                """
                SELECT r.id_reserva, r.fecha::TEXT, r.hora_inicio::TEXT, r.hora_fin::TEXT, r.estado,
                       COALESCE(u.nombre, 'Admin') as docente, s.nombre as salon, r.id_docente, r.id_salon
                FROM reserva r
                LEFT JOIN usuario u ON r.id_docente = u.id_usuario
                LEFT JOIN salon s ON r.id_salon = s.id_salon
                ORDER BY r.fecha DESC, r.hora_inicio DESC
                """
            )
            return cursor.fetchall()
        finally:
            conn.close()

    def existe_cruce(self, id_salon, fecha, hora_inicio, hora_fin):
        conn = self._connection_factory()
        if conn is None:
            return False
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(
                """
                SELECT * FROM reserva WHERE id_salon = %s AND fecha = %s
                AND estado != 'cancelada' AND (hora_inicio < %s AND hora_fin > %s)
                """,
                (id_salon, fecha, hora_fin, hora_inicio),
            )
            return cursor.fetchone() is not None
        except Exception:
            return False
        finally:
            conn.close()

    def crear(self, fecha, hora_inicio, hora_fin, id_docente, id_salon):
        conn = self._connection_factory()
        if conn is None:
            raise ConnectionError("No se pudo conectar a la base de datos")
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO reserva (fecha, hora_inicio, hora_fin, estado, id_docente, id_salon)
                VALUES (%s, %s, %s, 'confirmada', %s, %s)
                """,
                (fecha, hora_inicio, hora_fin, id_docente, id_salon),
            )
            conn.commit()
        finally:
            conn.close()

    def actualizar(self, id_reserva, fecha, hora_inicio, hora_fin, id_salon, id_docente):
        conn = self._connection_factory()
        if conn is None:
            raise ConnectionError("No se pudo conectar a la base de datos")
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE reserva
                SET fecha = %s, hora_inicio = %s, hora_fin = %s, id_salon = %s, id_docente = %s
                WHERE id_reserva = %s
                """,
                (fecha, hora_inicio, hora_fin, id_salon, id_docente, id_reserva),
            )
            conn.commit()
        finally:
            conn.close()

    def cancelar(self, id_reserva):
        conn = self._connection_factory()
        if conn is None:
            raise ConnectionError("No se pudo conectar a la base de datos")
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT id_salon FROM reserva WHERE id_reserva = %s", (id_reserva,))
            res = cursor.fetchone()
            if res:
                cursor.execute("UPDATE reserva SET estado = 'cancelada' WHERE id_reserva = %s", (id_reserva,))
                conn.commit()
                return res["id_salon"]
            return None
        finally:
            conn.close()

    def encolar(self, id_salon, id_docente):
        conn = self._connection_factory()
        if conn is None:
            raise ConnectionError("No se pudo conectar a la base de datos")
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO cola_espera (id_salon, id_docente) VALUES (%s, %s)",
                (id_salon, id_docente),
            )
            conn.commit()
        finally:
            conn.close()

    def promover_siguiente_cola(self, id_salon):
        conn = self._connection_factory()
        if conn is None:
            return
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(
                "SELECT * FROM cola_espera WHERE id_salon = %s ORDER BY fecha_registro ASC LIMIT 1",
                (id_salon,),
            )
            siguiente = cursor.fetchone()
            if siguiente:
                cursor.execute(
                    """
                    INSERT INTO reserva (fecha, estado, id_docente, id_salon, fecha_notificacion)
                    VALUES (CURRENT_DATE, 'pendiente_confirmacion', %s, %s, CURRENT_TIMESTAMP)
                    """,
                    (siguiente["id_docente"], id_salon),
                )
                cursor.execute("DELETE FROM cola_espera WHERE id_cola = %s", (siguiente["id_cola"],))
                conn.commit()
        finally:
            conn.close()

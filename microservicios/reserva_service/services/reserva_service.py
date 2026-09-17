from database.db_config import get_connection
from psycopg2.extras import RealDictCursor
from datetime import datetime

class ReservaService:
    def listar(self, id_usuario, id_rol):
        conn = get_connection()
        if conn is None:
            return {"status": "error", "message": "No se pudo conectar a la base de datos"}
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Consulta base. En DDD puro, los joins a docentes y salones
            # se manejarían por IDs y se ensamblarían en el Gateway o Frontend.
            # Asumiremos que la BD de reservas guarda el id y un snapshot del nombre (o se replica).
            # Para fines del taller, mantendremos la estructura pero filtramos en DB.
            
            query = """
                SELECT r.id_reserva, r.fecha::TEXT, r.hora_inicio::TEXT, r.hora_fin::TEXT, r.estado, 
                       COALESCE(u.nombre, 'Admin') as docente, s.nombre as salon, r.id_docente, r.id_salon
                FROM reserva r 
                LEFT JOIN usuario u ON r.id_docente = u.id_usuario 
                LEFT JOIN salon s ON r.id_salon = s.id_salon
            """
            
            params = []
            
            # FASE 5 MVC: Lógica de filtrado en el backend
            # Si es docente (rol 3), solo ve sus propias reservas
            if id_rol == 3:
                query += " WHERE r.id_docente = %s"
                params.append(id_usuario)
                
            query += " ORDER BY r.fecha DESC, r.hora_inicio DESC"
            
            cursor.execute(query, tuple(params))
            data = cursor.fetchall()
            conn.close()
            return {"status": "ok", "data": data}
        except Exception as e:
            if conn: conn.close()
            return {"status": "error", "message": str(e)}

    def obtener_estadisticas(self):
        conn = get_connection()
        if conn is None: return {"status": "error"}
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            # FASE 5 MVC: Agrupación en el backend
            query = """
                SELECT s.nombre as salon, COUNT(*) as total_reservas
                FROM reserva r
                JOIN salon s ON r.id_salon = s.id_salon
                WHERE r.estado != 'cancelada'
                GROUP BY s.nombre
            """
            cursor.execute(query)
            data = cursor.fetchall()
            conn.close()
            return {"status": "ok", "data": data}
        except Exception as e:
            if conn: conn.close()
            return {"status": "error", "message": str(e)}

    def existe_cruce(self, id_salon, fecha, h_ini, h_fin):
        conn = get_connection()
        if conn is None: return False
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query = """SELECT * FROM reserva WHERE id_salon = %s AND fecha = %s 
                       AND estado != 'cancelada' AND (hora_inicio < %s AND hora_fin > %s)"""
            cursor.execute(query, (id_salon, fecha, h_fin, h_ini))
            res = cursor.fetchone()
            conn.close()
            return res is not None
        except Exception as e:
            if conn: conn.close()
            return False

    def crear_reserva(self, data):
        h_ini = data['hora_inicio']
        h_fin = data.get('hora_fin')
        if not h_fin:
            try:
                from datetime import datetime, timedelta
                t_ini = datetime.strptime(h_ini, "%H:%M")
                t_fin = t_ini + timedelta(hours=2)
                h_fin = t_fin.strftime("%H:%M")
            except Exception:
                h_fin = "22:00"
        
        if self.existe_cruce(data['id_salon'], data['fecha'], h_ini, h_fin):
            return self._suscribir_a_cola(data['id_salon'], data['id_docente'])
        
        conn = get_connection()
        if conn is None: return {"status": "error", "message": "Error de conexión"}
        try:
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO reserva (fecha, hora_inicio, hora_fin, estado, id_docente, id_salon) 
                              VALUES (%s, %s, %s, 'confirmada', %s, %s)""", 
                           (data['fecha'], h_ini, h_fin, data['id_docente'], data['id_salon']))
            conn.commit()
            conn.close()
            return {"status": "ok", "message": "Reserva confirmada en BD"}
        except Exception as e:
            if conn: conn.close()
            return {"status": "error", "message": f"Error al crear reserva: {str(e)}"}

    def actualizar_reserva(self, id_reserva, data):
        conn = get_connection()
        if conn is None: return {"status": "error", "message": "Error de conexión"}
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE reserva 
                SET fecha = %s, hora_inicio = %s, hora_fin = %s, id_salon = %s, id_docente = %s
                WHERE id_reserva = %s
            """, (data['fecha'], data['hora_inicio'], data['hora_fin'], data['id_salon'], data['id_docente'], id_reserva))
            conn.commit()
            conn.close()
            return {"status": "ok", "message": "Reserva actualizada con éxito"}
        except Exception as e:
            if conn: conn.close()
            return {"status": "error", "message": f"Error al actualizar reserva: {str(e)}"}

    def _suscribir_a_cola(self, id_salon, id_docente):
        conn = get_connection()
        if conn is None: return {"status": "error", "message": "Error de conexión"}
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO cola_espera (id_salon, id_docente) VALUES (%s, %s)", (id_salon, id_docente))
            conn.commit()
            conn.close()
            return {"status": "cola", "message": "Añadido a lista de espera FIFO"}
        except Exception as e:
            if conn: conn.close()
            return {"status": "error", "message": f"Error al ingresar a cola: {str(e)}"}

    def cancelar_reserva(self, id_reserva):
        conn = get_connection()
        if conn is None: return {"status": "error", "message": "Error de conexión"}
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT id_salon FROM reserva WHERE id_reserva = %s", (id_reserva,))
            res = cursor.fetchone()
            
            if res:
                id_salon = res['id_salon']
                cursor.execute("UPDATE reserva SET estado = 'cancelada' WHERE id_reserva = %s", (id_reserva,))
                conn.commit()
                self._notificar_siguiente(id_salon)
            conn.close()
            return {"status": "ok"}
        except Exception as e:
            if conn: conn.close()
            return {"status": "error", "message": str(e)}

    def _notificar_siguiente(self, id_salon):
        conn = get_connection()
        if conn is None: return
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT * FROM cola_espera WHERE id_salon = %s ORDER BY fecha_registro ASC LIMIT 1", (id_salon,))
            siguiente = cursor.fetchone()
            if siguiente:
                cursor.execute("""INSERT INTO reserva (fecha, estado, id_docente, id_salon, fecha_notificacion) 
                                  VALUES (CURRENT_DATE, 'pendiente_confirmacion', %s, %s, CURRENT_TIMESTAMP)""", 
                               (siguiente['id_docente'], id_salon))
                cursor.execute("DELETE FROM cola_espera WHERE id_cola = %s", (siguiente['id_cola'],))
                conn.commit()
            conn.close()
        except Exception as e:
            if conn: conn.close()

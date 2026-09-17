from database.db_config import get_connection
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

class ReservaService:
    
    def existe_cruce(self, id_salon: Any, fecha: Any, h_ini: str, h_fin: str) -> bool:
        """Verifica si existe un cruce de horarios para un salón en una fecha específica."""
        conn = get_connection()
        if not conn: 
            return False
        
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                    SELECT 1 FROM reserva 
                    WHERE id_salon = %s AND fecha = %s 
                    AND estado != 'cancelada' AND (hora_inicio < %s AND hora_fin > %s)
                    LIMIT 1
                """
                cursor.execute(query, (id_salon, fecha, h_fin, h_ini))
                return cursor.fetchone() is not None
        except Exception as e:
            print(f"[ERROR DB] Error al verificar cruce: {e}")
            return False
        finally:
            if conn: 
                conn.close()

    def crear_reserva(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Crea una reserva o la envía a la cola de espera si hay cruce de horarios."""
        # 1. Validación de campos obligatorios mínimos
        if not all(k in data for k in ('id_salon', 'fecha', 'id_docente', 'hora_inicio')):
            return {"status": "error", "message": "Faltan datos obligatorios para la reserva."}
        
        h_ini = data['hora_inicio']
        h_fin = data.get('hora_fin')
        
        # 2. Fallback de hora de fin si no viene especificada
        if not h_fin:
            try:
                t_ini = datetime.strptime(h_ini, "%H:%M")
                t_fin = t_ini + timedelta(hours=2)
                h_fin = t_fin.strftime("%H:%M")
            except Exception:
                h_fin = "22:00" # Fallback absoluto
        
        # 3. Comprobar si existe cruce de horarios
        if self.existe_cruce(data['id_salon'], data['fecha'], h_ini, h_fin):
            return self._suscribir_a_cola(data['id_salon'], data['id_docente'])
        
        # 4. Registrar la reserva en firme
        conn = get_connection()
        if not conn: 
            return {"status": "error", "message": "Error de conexión"}
        
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO reserva (fecha, hora_inicio, hora_fin, estado, id_docente, id_salon) 
                    VALUES (%s, %s, %s, 'confirmada', %s, %s)
                """, (data['fecha'], h_ini, h_fin, data['id_docente'], data['id_salon']))
                
                conn.commit()
                return {"status": "ok", "message": "Reserva confirmada en Supabase"}
        except Exception as e:
            conn.rollback()
            return {"status": "error", "message": f"Error al crear reserva: {str(e)}"}
        finally:
            if conn: 
                conn.close()

    def actualizar_reserva(self, id_reserva: Any, data: Dict[str, Any]) -> Dict[str, str]:
        """Actualiza los datos de una reserva existente."""
        if not all(k in data for k in ('fecha', 'hora_inicio', 'hora_fin', 'id_salon', 'id_docente')):
            return {"status": "error", "message": "Faltan datos obligatorios para la actualización."}

        conn = get_connection()
        if not conn: 
            return {"status": "error", "message": "Error de conexión"}
        
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE reserva 
                    SET fecha = %s, hora_inicio = %s, hora_fin = %s, id_salon = %s, id_docente = %s
                    WHERE id_reserva = %s
                """, (data['fecha'], data['hora_inicio'], data['hora_fin'], data['id_salon'], data['id_docente'], id_reserva))
                
                conn.commit()
                return {"status": "ok", "message": "Reserva actualizada con éxito"}
        except Exception as e:
            conn.rollback()
            return {"status": "error", "message": f"Error al actualizar reserva: {str(e)}"}
        finally:
            if conn: 
                conn.close()

    def _suscribir_a_cola(self, id_salon: Any, id_docente: Any) -> Dict[str, str]:
        """Añade al docente a la cola de espera de un salón."""
        conn = get_connection()
        if not conn: 
            return {"status": "error", "message": "Error de conexión"}
        
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO cola_espera (id_salon, id_docente) 
                    VALUES (%s, %s)
                """, (id_salon, id_docente))
                
                conn.commit()
                return {"status": "cola", "message": "Añadido a lista de espera FIFO"}
        except Exception as e:
            conn.rollback()
            return {"status": "error", "message": f"Error al ingresar a cola: {str(e)}"}
        finally:
            if conn: 
                conn.close()

    def cancelar_reserva(self, id_reserva: Any) -> Dict[str, Any]:
        """Cancela una reserva y notifica automáticamente al siguiente en la cola de espera."""
        conn = get_connection()
        if not conn: 
            return {"status": "error", "message": "Error de conexión"}
        
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT id_salon FROM reserva WHERE id_reserva = %s", (id_reserva,))
                res = cursor.fetchone()
                
                if res:
                    id_salon = res['id_salon']
                    cursor.execute("UPDATE reserva SET estado = 'cancelada' WHERE id_reserva = %s", (id_reserva,))
                    conn.commit()
                    # Notificar al siguiente en la cola tras cancelar exitosamente
                    self._notificar_siguiente(id_salon)
                    
            return {"status": "ok", "message": "Reserva cancelada correctamente"}
        except Exception as e:
            if conn:
                conn.rollback()
            return {"status": "error", "message": str(e)}
        finally:
            if conn: 
                conn.close()

    def _notificar_siguiente(self, id_salon: Any) -> None:
        """Toma al primer docente de la cola de espera y le crea una reserva pendiente."""
        conn = get_connection()
        if not conn: 
            return
        
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT * FROM cola_espera 
                    WHERE id_salon = %s 
                    ORDER BY fecha_registro ASC 
                    LIMIT 1
                """, (id_salon,))
                siguiente = cursor.fetchone()
                
                if siguiente:
                    cursor.execute("""
                        INSERT INTO reserva (fecha, estado, id_docente, id_salon, fecha_notificacion) 
                        VALUES (CURRENT_DATE, 'pendiente_confirmacion', %s, %s, CURRENT_TIMESTAMP)
                    """, (siguiente['id_docente'], id_salon))
                    
                    cursor.execute("DELETE FROM cola_espera WHERE id_cola = %s", (siguiente['id_cola'],))
                    conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"[ERROR DB] Error al notificar siguiente en cola: {e}")
        finally:
            if conn: 
                conn.close()
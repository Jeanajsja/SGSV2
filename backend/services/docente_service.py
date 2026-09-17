from database.db_config import get_connection
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash
from typing import List, Dict, Any

class DocenteService:
    
    def listar(self) -> List[Dict[str, Any]]:
        """Obtiene la lista de todos los docentes registrados."""
        conn = get_connection()
        if not conn:
            return []
        
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT id_usuario AS id_docente, nombre, email AS correo, 'Sin Teléfono' AS telefono
                    FROM usuario 
                    WHERE id_rol = 3 
                    ORDER BY nombre ASC
                """)
                return cursor.fetchall()
        except Exception as e:
            print(f"[ERROR DB] Error al listar docentes: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def crear(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Registra un nuevo docente validando datos básicos y errores tipográficos en el correo."""
        # 1. Validación de campos obligatorios para evitar KeyErrors
        nombre = data.get('nombre')
        correo = data.get('correo')
        
        if not nombre or not correo:
            return {"status": "error", "message": "Los campos 'nombre' y 'correo' son obligatorios."}

        email = correo.strip().lower()
        
        # 2. Validación y detección de typos en el correo (Se mantiene tu lógica útil)
        if '@' in email:
            dominio_completo = email.split('@')[-1]
            dominio_base = dominio_completo.split('.')[0]
            
            typos_base = {
                'gmal': 'gmail', 'gmai': 'gmail', 'gamil': 'gmail', 'gmaill': 'gmail',
                'hotml': 'hotmail', 'hotmal': 'hotmail', 'hormail': 'hotmail', 'homail': 'hotmail',
                'outlok': 'outlook', 'outloo': 'outlook', 'oulook': 'outlook',
                'yaho': 'yahoo', 'yahhoo': 'yahoo'
            }
            
            if dominio_base in typos_base:
                correccion = dominio_completo.replace(dominio_base, typos_base[dominio_base], 1)
                return {"status": "error", "message": f"Dominio de correo inválido. ¿Quisiste escribir @{correccion}?"}
            
            if dominio_completo.endswith(('.con', '.c', '.om', '.o')):
                correccion = dominio_completo.rsplit('.', 1)[0] + '.com'
                return {"status": "error", "message": f"Dominio de correo inválido. ¿Quisiste escribir @{correccion}?"}

        # 3. Operación en Base de Datos de forma segura
        conn = get_connection()
        if not conn:
            return {"status": "error", "message": "Error de conexión a la base de datos"}
        
        try:
            with conn.cursor() as cursor:
                password_defecto = generate_password_hash("docente123")
                cursor.execute("""
                    INSERT INTO usuario (nombre, email, password, id_rol) 
                    VALUES (%s, %s, %s, 3)
                """, (nombre, email, password_defecto))
                
                conn.commit()
                return {
                    "status": "ok", 
                    "message": "Docente registrado con éxito. Contraseña por defecto: docente123"
                }
        except Exception as e:
            conn.rollback() # Revierte cambios si ocurre un fallo en el INSERT
            return {"status": "error", "message": f"Error al registrar docente en la BD: {str(e)}"}
        finally:
            if conn:
                conn.close()
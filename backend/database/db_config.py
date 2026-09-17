import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Carga las variables del archivo .env si existe localmente
load_dotenv()

def get_db_connection():
    """
    Fabrica de conexiones modular para el microservicio.
    """
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            hostaddr=os.getenv("DB_HOSTADDR"),
            port=os.getenv("DB_PORT", 6543),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            sslmode="require",
            connect_timeout=5,
            cursor_factory=RealDictCursor # Retorna los resultados como diccionarios listos para APIs
        )
        return conn
    except Exception as e:
        print(f"[ERROR DB] No se pudo establecer la conexión: {e}")
        raise e
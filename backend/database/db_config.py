import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

<<<<<<< HEAD
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
=======
def get_connection():
    # 1. Si existe DATABASE_URL en las variables de entorno (ej. en Render)
    database_url = os.environ.get("DATABASE_URL")
    if database_url:
        try:
            return psycopg2.connect(database_url, sslmode="require", connect_timeout=10)
        except Exception as e:
            print(f"[WARN] Connection using DATABASE_URL failed: {e}")

    host = os.environ.get("DB_HOST", "aws-1-us-east-2.pooler.supabase.com")
    port = int(os.environ.get("DB_PORT", "6543"))
    database = os.environ.get("DB_NAME", "postgres")
    user = os.environ.get("DB_USER", "postgres.qgwpttpknrevnbdsjnrx")
    password = os.environ.get("DB_PASSWORD", "Sgs_Proyecto_2026")
    hostaddr = os.environ.get("DB_HOSTADDR", "13.58.13.125")

    # 2. Intento estándar por nombre de host (recomendado en Render y entornos de nube)
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
            sslmode="require",
            connect_timeout=10
        )
        return conn
    except Exception as e1:
        print(f"[WARN] Connection via hostname ({host}) failed: {e1}")

    # 3. Intento secundario con IP fija (para resolver bloqueos de DNS locales)
    try:
        conn = psycopg2.connect(
            host=host,
            hostaddr=hostaddr,
            port=port,
            database=database,
            user=user,
            password=password,
            sslmode="require",
            connect_timeout=10
        )
        return conn
    except Exception as e2:
        print(f"[ERROR] Connection failed completely: {e2}")
        return None
>>>>>>> origin/main

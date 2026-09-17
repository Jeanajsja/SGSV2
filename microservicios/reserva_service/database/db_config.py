import psycopg2
from psycopg2.extras import RealDictCursor

def get_connection():
    # Conexión local al contenedor PostgreSQL de la BD aislada de Reservas
    params = {
        "host": "localhost",
        "port": 5435,
        "database": "sgs_reservas_db",
        "user": "admin",
        "password": "password"
    }
    
    try:
        conn = psycopg2.connect(**params)
        return conn
    except Exception as e:
        print(f"\n[ERROR] Connection failed to Reserva DB: {e}\n")
        return None

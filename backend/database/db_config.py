import os

import psycopg2


DEFAULT_DB_HOST = os.getenv("DB_HOST", "localhost")
DEFAULT_DB_PORT = int(os.getenv("DB_PORT", "5432"))
DEFAULT_DB_NAME = os.getenv("DB_NAME", "postgres")
DEFAULT_DB_USER = os.getenv("DB_USER", "postgres")
DEFAULT_DB_PASSWORD = os.getenv("DB_PASSWORD", "")


def get_connection():
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        try:
            return psycopg2.connect(database_url, sslmode="require", connect_timeout=10)
        except Exception as exc:  # pragma: no cover - fallback for local/test environments
            print(f"[WARN] No se pudo conectar usando DATABASE_URL: {exc}")

    host = os.getenv("DB_HOST", DEFAULT_DB_HOST)
    port = int(os.getenv("DB_PORT", str(DEFAULT_DB_PORT)))
    database = os.getenv("DB_NAME", DEFAULT_DB_NAME)
    user = os.getenv("DB_USER", DEFAULT_DB_USER)
    password = os.getenv("DB_PASSWORD", DEFAULT_DB_PASSWORD)

    try:
        return psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
            sslmode="require",
            connect_timeout=10,
        )
    except Exception as exc:
        print(f"[ERROR] No se pudo establecer la conexión a la base de datos: {exc}")
        return None


def get_db_connection():
    return get_connection()

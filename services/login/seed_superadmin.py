from werkzeug.security import generate_password_hash
from superadmin_ancla import ROL_SUPERADMIN, SUPERADMIN_ANCLA, SUPERADMIN_CLAVE, SUPERADMIN_NOMBRE


def asegurar_superadmin(connection_factory):
    conn = connection_factory()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        clave = generate_password_hash(SUPERADMIN_CLAVE)
        cursor.execute("SELECT id_usuario FROM usuario WHERE lower(email) = %s", (SUPERADMIN_ANCLA,))
        if cursor.fetchone():
            cursor.execute(
                "UPDATE usuario SET password = %s, id_rol = %s, nombre = %s WHERE lower(email) = %s",
                (clave, ROL_SUPERADMIN, SUPERADMIN_NOMBRE, SUPERADMIN_ANCLA),
            )
        else:
            cursor.execute(
                "INSERT INTO usuario (nombre, email, password, id_rol) VALUES (%s, %s, %s, %s)",
                (SUPERADMIN_NOMBRE, SUPERADMIN_ANCLA, clave, ROL_SUPERADMIN),
            )
        conn.commit()
    except Exception as e:
        print(f"[ms-login] no se pudo anclar el superadmin: {e}")
    finally:
        conn.close()

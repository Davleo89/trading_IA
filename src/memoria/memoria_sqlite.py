import sqlite3

from config import LIBROS_DB_PATH

# ==================================================
# CREAR TABLA DE MEMORIA DE CONVERSACIÓN
# ==================================================

def main():

    conexion = sqlite3.connect(LIBROS_DB_PATH)
    cursor = conexion.cursor()

    try:

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
            rol TEXT NOT NULL,
            mensaje TEXT NOT NULL
        )
        """)

        conexion.commit()

        print("✅ Tabla 'conversaciones' creada correctamente.")

    except Exception:
        conexion.rollback()
        raise

    finally:
        conexion.close()


if __name__ == "__main__":
    main()

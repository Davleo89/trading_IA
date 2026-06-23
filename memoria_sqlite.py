import sqlite3

conexion = sqlite3.connect(
    "libros_trading.db"
)

cursor = conexion.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS conversaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    rol TEXT,
    mensaje TEXT
    )
    """)

conexion.commit()
conexion.close()

print("Tabla conversaciones creada")

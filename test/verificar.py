import sqlite3

conexion = sqlite3.connect("libros_trading.db")
cursor = conexion.cursor()

cursor.execute("""
SELECT
    nombre_archivo,
    tematica
FROM libros
ORDER BY tematica
""")

for fila in cursor.fetchall():
    print(fila)

conexion.close()
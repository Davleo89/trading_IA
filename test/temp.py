import sqlite3

conexion = sqlite3.connect("libros_trading.db")
cursor = conexion.cursor()

cursor.execute("""
SELECT
    tematica,
    COUNT(*)
FROM libros
GROUP BY tematica
""")

for fila in cursor.fetchall():
    print(fila)

conexion.close()
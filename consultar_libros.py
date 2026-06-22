import sqlite3

conexion = sqlite3.connect("libros_trading.db")
cursor = conexion.cursor()

cursor.execute("""
SELECT nombre_archivo, categoria
FROM libros
""")

for libro in cursor.fetchall():
    print(libro)

conexion.close()
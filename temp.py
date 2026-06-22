import sqlite3

conexion = sqlite3.connect("libros_trading.db")
cursor = conexion.cursor()

cursor.execute("""
SELECT nombre_archivo
FROM libros
WHERE texto_completo LIKE '%RSI%'
""")

resultados = cursor.fetchall()

print(resultados)

conexion.close()
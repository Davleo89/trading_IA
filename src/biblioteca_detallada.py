import sqlite3

from config import DB_PATH

conexion = sqlite3.connect(DB_PATH)

cursor = conexion.cursor()

cursor.execute("""
SELECT
    nombre_archivo,
    tematica,
    resumen
FROM libros
ORDER BY nombre_archivo
""")

libros = cursor.fetchall()

for nombre, tematica, resumen in libros:
    print("\n" + "=" * 80)
    print(f"\n📘 {nombre}")
    print(f"\n🏷️ Temática:")
    print(tematica)
    print(f"\n📝 Resumen:")
    print(resumen)

conexion.close()

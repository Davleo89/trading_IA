import sqlite3

# ==================================================
# CONEXIÓN
# ==================================================

conexion = sqlite3.connect("libros_trading.db")
cursor = conexion.cursor()

print("\n" + "=" * 60)
print("ESTADO DE LA BIBLIOTECA")
print("=" * 60)

# ==================================================
# LIBROS
# ==================================================

cursor.execute("""
SELECT COUNT(*)
FROM libros
""")

total_libros = cursor.fetchone()[0]

print(f"\n📚 Libros cargados: {total_libros}")

# ==================================================
# CHUNKS
# ==================================================

cursor.execute("""
SELECT COUNT(*)
FROM chunks
""")

total_chunks = cursor.fetchone()[0]

print(f"🧩 Chunks generados: {total_chunks}")

# ==================================================
# EMBEDDINGS
# ==================================================

cursor.execute("""
SELECT COUNT(*)
FROM embeddings
""")

total_embeddings = cursor.fetchone()[0]

print(f"🧠 Embeddings generados: {total_embeddings}")

# ==================================================
# MEMORIA (si existe)
# ==================================================

try:

    cursor.execute("""
    SELECT COUNT(*)
    FROM memoria
    """)

    total_memoria = cursor.fetchone()[0]

    print(f"💬 Conversaciones guardadas: {total_memoria}")

except:

    print("💬 Tabla memoria no encontrada")

# ==================================================
# LISTA DE LIBROS
# ==================================================

print("\n" + "=" * 60)
print("LIBROS DISPONIBLES")
print("=" * 60)

cursor.execute("""
SELECT nombre_archivo
FROM libros
ORDER BY nombre_archivo
""")

for numero, (nombre,) in enumerate(cursor.fetchall(), start=1):

    print(f"{numero}. {nombre}")

# ==================================================
# FINALIZAR
# ==================================================

conexion.close()

print("\n" + "=" * 60)
print("FIN DEL REPORTE")
print("=" * 60)
import sqlite3
import sys
from pathlib import Path

# ==========================================
# CONFIG
# ==========================================

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT / "src"))

from config import DB_PATH

# ==========================================
# CONEXION
# ==========================================

conexion = sqlite3.connect(DB_PATH)
cursor = conexion.cursor()

# ==========================================
# LIMPIAR TABLAS
# ==========================================

cursor.execute("DELETE FROM embeddings")
cursor.execute("DELETE FROM chunks")
cursor.execute("DELETE FROM libros")

# ==========================================
# REINICIAR AUTOINCREMENT
# ==========================================

cursor.execute("""
DELETE FROM sqlite_sequence
WHERE name IN (
    'libros',
    'chunks',
    'embeddings'
)
""")

conexion.commit()
conexion.close()

print("\n🗑️ Biblioteca reiniciada correctamente")
print("📚 libros = 0")
print("🧩 chunks = 0")
print("🧠 embeddings = 0")
import sqlite3
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.append(
    str(BASE_DIR / "src")
)

from config import DB_PATH

conexion = sqlite3.connect(DB_PATH)
cursor = conexion.cursor()

print("\n" + "=" * 60)
print("ESTADO DE LA BASE DE DATOS")
print("=" * 60)

# Libros

cursor.execute(
    "SELECT COUNT(*) FROM libros"
)

print(
    f"\n📚 Libros: {cursor.fetchone()[0]}"
)

# Chunks

cursor.execute(
    "SELECT COUNT(*) FROM chunks"
)

print(
    f"🧩 Chunks: {cursor.fetchone()[0]}"
)

# Embeddings

cursor.execute(
    "SELECT COUNT(*) FROM embeddings"
)

print(
    f"🧠 Embeddings: {cursor.fetchone()[0]}"
)

# Memoria

try:

    cursor.execute(
        "SELECT COUNT(*) FROM memoria"
    )

    print(
        f"💬 Memorias: {cursor.fetchone()[0]}"
    )

except:

    print(
        "💬 Tabla memoria no encontrada"
    )

print("\n" + "=" * 60)

conexion.close()
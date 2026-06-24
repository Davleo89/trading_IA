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

cursor.execute("DELETE FROM embeddings")
cursor.execute("DELETE FROM chunks")

conexion.commit()
conexion.close()

print("✅ Chunks eliminados")
print("✅ Embeddings eliminados")
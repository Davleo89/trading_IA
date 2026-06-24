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

cursor.execute("""
UPDATE libros
SET
    resumen = NULL,
    tematica = NULL
""")

conexion.commit()
conexion.close()

print("✅ Resúmenes eliminados")
print("✅ Temáticas eliminadas")
from pathlib import Path
import sys
import sqlite3

ROOT_PATH = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_PATH / "src"))

from config import DB_PATH

conexion = sqlite3.connect(DB_PATH)
cursor = conexion.cursor()

cursor.execute("""
SELECT
    nombre_archivo,
    tematica
FROM libros
""")

for fila in cursor.fetchall():
    print(fila)

conexion.close()
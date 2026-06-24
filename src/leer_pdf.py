import os
import sqlite3

from pypdf import PdfReader
from config import DB_PATH
from config import PDF_PATH

# ==================================================
# CONEXIÓN SQLITE
# ==================================================

conexion = sqlite3.connect(DB_PATH)
cursor = conexion.cursor()

# ==================================================
# TABLA LIBROS
# ==================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS libros (
    id INTEGER PRIMARY KEY,
    nombre_archivo TEXT UNIQUE,
    texto_completo TEXT,
    resumen TEXT
)
""")

conexion.commit()

# ==================================================
# LEER PDFs
# ==================================================

if PDF_PATH.exists():

    archivos = [
        archivo
        for archivo in PDF_PATH.iterdir()
        if archivo.suffix.lower() == ".pdf"
    ]

    print(f"\n📚 PDFs encontrados: {len(archivos)}")

    for archivo in archivos:
        
        print(f"\nLeyendo: {archivo.name}")
        
        try:
            reader = PdfReader(str(archivo))
            texto_completo = ""

            for pagina in reader.pages[15:]:
                texto_completo += pagina.extract_text() or ""

            cursor.execute("""
            INSERT OR IGNORE INTO libros
            (
                nombre_archivo,
                texto_completo
            )
            VALUES (?, ?)
            """,
            (
                archivo.name,
                texto_completo
            ))

            print(
                f"✅ Guardado: {archivo.name}"
            )

        except Exception as e:

            print(
                f"❌ Error en {archivo.name}: {e}"
            )

else:

    print(
        f"⚠️ No existe la carpeta {PDF_PATH.resolve()}"
    )

# ==================================================
# FINALIZAR
# ==================================================

conexion.commit()
conexion.close()

print(
    "\n🚀 Proceso completado"
)
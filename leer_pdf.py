import os
import sqlite3
from pypdf import PdfReader

# ==================================================
# CONEXIÓN SQLITE
# ==================================================

conexion = sqlite3.connect("libros_trading.db")
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
# CARPETA DE PDFs
# ==================================================

CARPETA_PDFS = "pdf_books"

# ==================================================
# LEER PDFs
# ==================================================

if os.path.exists(CARPETA_PDFS):

    archivos = [
        archivo
        for archivo in os.listdir(CARPETA_PDFS)
        if archivo.lower().endswith(".pdf")
    ]

    print(f"\n📚 PDFs encontrados: {len(archivos)}")

    for archivo in archivos:

        ruta_pdf = os.path.join(
            CARPETA_PDFS,
            archivo
        )

        print(f"\nLeyendo: {archivo}")

        try:

            reader = PdfReader(ruta_pdf)

            texto_completo = ""

            for pagina in reader.pages:
                texto_completo += (
                    pagina.extract_text() or ""
                )

            cursor.execute("""
            INSERT OR IGNORE INTO libros
            (
                nombre_archivo,
                texto_completo
            )
            VALUES (?, ?)
            """,
            (
                archivo,
                texto_completo
            ))

            print(
                f"✅ Guardado: {archivo}"
            )

        except Exception as e:

            print(
                f"❌ Error en {archivo}: {e}"
            )

else:

    print(
        f"⚠️ No existe la carpeta {CARPETA_PDFS}"
    )

# ==================================================
# FINALIZAR
# ==================================================

conexion.commit()
conexion.close()

print(
    "\n🚀 Proceso completado"
)
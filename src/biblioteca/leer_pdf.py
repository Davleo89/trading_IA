import sqlite3
from pypdf import PdfReader

from utils import logger
from config import LIBROS_DB_PATH, PDF_PATH, PDF_PAGINAS_IGNORADAS


# ==================================================
# FUNCIÓN PRINCIPAL PARA EL PIPELINE
# ==================================================

def main():

    conexion = sqlite3.connect(LIBROS_DB_PATH)
    cursor = conexion.cursor()

    try:

        # --------------------------------------------------
        # Crear tabla
        # --------------------------------------------------

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS libros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_archivo TEXT UNIQUE,
            texto_completo TEXT,
            resumen TEXT,
            tematica TEXT
        )
        """)

        conexion.commit()

        # --------------------------------------------------
        # Verificar carpeta de PDFs
        # --------------------------------------------------

        if not PDF_PATH.exists():
            logger.escribir_log(
                f"No existe la carpeta: {PDF_PATH.resolve()}",
                nivel="error"
            )
            return

        archivos = sorted(PDF_PATH.glob("*.pdf"))

        logger.escribir_log(
            f"📚 PDFs encontrados: {len(archivos)}",
            nivel="info"
        )

        # --------------------------------------------------
        # Leer cada PDF
        # --------------------------------------------------

        for archivo in archivos:

            logger.escribir_log(
                f"📖 Leyendo: {archivo.name}",
                nivel="info"
            )

            try:

                reader = PdfReader(str(archivo))

                if reader.is_encrypted:
                    logger.escribir_log(
                        f"⚠ El PDF está protegido: {archivo.name}",
                        nivel="warning"
                    )
                    continue

                texto_paginas = []

                for pagina in reader.pages[PDF_PAGINAS_IGNORADAS:]:

                    texto_pagina = pagina.extract_text() or ""

                    if not texto_pagina.strip():
                        continue

                    texto_paginas.append(texto_pagina)

                texto_completo = "\n".join(texto_paginas)

                if not texto_completo.strip():

                    logger.escribir_log(
                        f"⚠ No se pudo extraer texto de {archivo.name}",
                        nivel="warning"
                    )
                    continue

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

                logger.escribir_log(
                    f"✅ Guardado: {archivo.name}",
                    nivel="success"
                )

            except Exception as e:

                logger.escribir_log(
                    f"❌ Error procesando {archivo.name}: {e}",
                    nivel="error"
                )

                continue

        conexion.commit()

        logger.escribir_log(
            "🚀 Lectura de PDFs finalizada.",
            nivel="success"
        )

    except Exception as e:

        conexion.rollback()

        logger.escribir_log(
            f"Error general del módulo leer_pdf: {e}",
            nivel="error"
        )

        raise

    finally:

        conexion.close()


if __name__ == "__main__":
    main()
import sqlite3
from utils import logger
from config import LIBRO_DB_PATH

# ==================================================
# DIVIDIR TEXTO
# ==================================================
def dividir_texto(texto, tamano=300, overlap=50):
    palabras = texto.split()
    paso = tamano - overlap

    for i in range(0, len(palabras), paso):
        chunks = " ".join(palabras[i:i + tamano])
        if chunks.strip():
            yield chunks

# ==================================================
# FUNCIÓN PRINCIPAL PARA EL PIPELINE
# ==================================================
def main():
    conexion = sqlite3.connect(LIBRO_DB_PATH)
    cursor = conexion.cursor()
    
    try:
        # Creación de tablas e índices
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            libro_id INTEGER NOT NULL,
            chunk_text TEXT NOT NULL
        )
        """)
        
        cursor.execute("DELETE FROM chunks")
        
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_chunks_libro
        ON chunks(libro_id)
        """)
        conexion.commit()

        # Generar Chunks
        cursor.execute("SELECT id, texto_completo FROM libros")
        libros = cursor.fetchall()

        for libro_id, texto_completo in libros:
            logger.escribir_log(f"  📖 Procesando fragmentos del libro ID: {libro_id}")
            for chunk in dividir_texto(texto_completo):
                cursor.execute("""
                INSERT INTO chunks (libro_id, chunk_text)
                VALUES (?, ?)
                """, (libro_id, chunk))

        conexion.commit()

        # Conteo final
        cursor.execute("SELECT COUNT(*) FROM chunks")
        total_chunks = cursor.fetchone()[0]
        logger.escribir_log(f"  ✅ Total de chunks creados: {total_chunks}")
        
    except Exception as e:
        conexion.rollback()
        raise 
    finally:
        conexion.close()

if __name__ == "__main__":
    main()
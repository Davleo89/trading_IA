import sqlite3
import pickle
from sentence_transformers import SentenceTransformer
from config import DB_PATH, EMBEDDING_MODEL

# ==================================================
# FUNCIÓN PRINCIPAL PARA EL PIPELINE
# ==================================================
def main():
    print(f"  🧠 Cargando modelo de embeddings: {EMBEDDING_MODEL}...")
    modelo = SentenceTransformer(EMBEDDING_MODEL)
    
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    
    try:
        # Creación de tabla e índice
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS embeddings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chunk_id INTEGER,
            vector BLOB
        )
        """)
        
        cursor.execute("DELETE FROM embeddings")
        
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_embeddings_chunk
        ON embeddings(chunk_id)
        """)
        conexion.commit()

        # Generar Embeddings
        cursor.execute("SELECT id, chunk_text FROM chunks")
        chunks = cursor.fetchall()
        total = len(chunks)

        print(f"  ⚡ Generando embeddings para {total} fragmentos...")
        for index, (chunk_id, chunk_text) in enumerate(chunks, start=1):
            # Imprime progreso cada 10 chunks para mantener limpia la consola
            if index % 10 == 0 or index == total:
                print(f"     -> Procesados {index}/{total} embeddings...")

            embedding = modelo.encode(chunk_text)
            embedding_blob = pickle.dumps(embedding)

            cursor.execute("""
            INSERT INTO embeddings (chunk_id, vector)
            VALUES (?, ?)
            """, (chunk_id, embedding_blob))

        conexion.commit()
        print("  🚀 Todos los embeddings han sido generados con éxito.")
        
    except Exception as e:
        conexion.rollback()
        raise e
    finally:
        conexion.close()

if __name__ == "__main__":
    main()
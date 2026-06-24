import sqlite3
import pickle

from sentence_transformers import SentenceTransformer
from config import DB_PATH
from config import EMBEDDING_MODEL

# ==================================================
# MODELO DE EMBEDDINGS
# ==================================================

modelo = SentenceTransformer(EMBEDDING_MODEL)

# ==================================================
# CONEXIÓN SQLITE
# ==================================================

conexion = sqlite3.connect(DB_PATH)
cursor = conexion.cursor()

# ==================================================
# TABLA CHUNKS
# ==================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS chunks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    libro_id INTEGER,
    chunk_text TEXT
)
""")

# ==================================================
# TABLA EMBEDDINGS
# ==================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS embeddings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chunk_id INTEGER,
    vector BLOB
)
""")

# ==================================================
# LIMPIAR DATOS ANTERIORES
# ==================================================

cursor.execute("DELETE FROM embeddings")
cursor.execute("DELETE FROM chunks")

conexion.commit()

# ==================================================
# ÍNDICES
# ==================================================

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_chunks_libro
ON chunks(libro_id)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_embeddings_chunk
ON embeddings(chunk_id)
""")

conexion.commit()

# ==================================================
# DIVIDIR TEXTO
# ==================================================

def dividir_texto(texto, tamano = 300, overlap = 50):

    palabras = texto.split()
    paso = tamano - overlap

    for i in range(0, len(palabras), paso):
        chunks = " ".join(
            palabras[i:i + tamano]
        )
        if chunks.strip():
            yield chunks

# ==================================================
# GENERAR CHUNKS
# ==================================================

cursor.execute("""
SELECT id, texto_completo
FROM libros
""")

libros = cursor.fetchall()

for libro_id, texto_completo in libros:

    print(f"\n📖 Procesando libro {libro_id}")

    for chunk in dividir_texto(texto_completo):

        cursor.execute("""
        INSERT INTO chunks
        (libro_id, chunk_text)
        VALUES (?, ?)
        """,
        (libro_id, chunk))

conexion.commit()

# ==================================================
# CONTAR CHUNKS
# ==================================================

cursor.execute("""
SELECT COUNT(*)
FROM chunks
""")

total_chunks = cursor.fetchone()[0]

print(f"\n✅ Total de chunks creados: {total_chunks}")

# ==================================================
# GENERAR EMBEDDINGS
# ==================================================

cursor.execute("""
SELECT id, chunk_text
FROM chunks
""")

chunks = cursor.fetchall()

for chunk_id, chunk_text in chunks:

    print(
        f"🧠 Embedding chunk {chunk_id} "
        f"({len(chunk_text.split())} palabras)"
    )

    embedding = modelo.encode(chunk_text)

    embedding_blob = pickle.dumps(embedding)

    cursor.execute("""
    INSERT INTO embeddings
    (chunk_id, vector)
    VALUES (?, ?)
    """,
    (chunk_id, embedding_blob))

# ==================================================
# FINALIZAR
# ==================================================

conexion.commit()
conexion.close()

print("\n🚀 Chunks y embeddings generados correctamente")

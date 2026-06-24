import sqlite3
import ollama

from collections import Counter
from config import DB_PATH, LLM_MODEL

# ==========================================
# CONFIG
# ==========================================

CHUNKS_POR_LIBRO = 10

# ==========================================
# CONEXION
# ==========================================

conexion = sqlite3.connect(DB_PATH)
cursor = conexion.cursor()

# ==========================================
# CLASIFICAR CHUNK
# ==========================================

def clasificar_chunk(texto):

    prompt = f"""
Clasifica el siguiente fragmento.

Categorias posibles:

- Analisis Tecnico
- Psicologia del Trading
- Gestion de Riesgo
- Inversion
- Historia de Mercados
- Trading General

Responde SOLO con una categoria.

Fragmento:

{texto[:2500]}
"""

    respuesta = ollama.chat(
        model=LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    categoria = (
        respuesta["message"]["content"]
        .strip()
        .replace("*", "")
    )

    return categoria

# ==========================================
# OBTENER CHUNKS DISTRIBUIDOS
# ==========================================

def obtener_chunks_libro(libro_id):

    cursor.execute("""
    SELECT chunk_text
    FROM chunks
    WHERE libro_id = ?
    """,
    (libro_id,))
    
    chunks = [
        fila[0]
        for fila in cursor.fetchall()
    ]

    if len(chunks) <= CHUNKS_POR_LIBRO:
        return chunks

    paso = max(
        1,
        len(chunks) // CHUNKS_POR_LIBRO
    )

    seleccionados = []

    for i in range(0, len(chunks), paso):
        seleccionados.append(chunks[i])

        if len(seleccionados) >= CHUNKS_POR_LIBRO:
            break

    return seleccionados

# ==========================================
# LIBROS
# ==========================================

cursor.execute("""
SELECT
    id,
    nombre_archivo
FROM libros
""")

libros = cursor.fetchall()

print(f"\n📚 Libros encontrados: {len(libros)}")

# ==========================================
# PROCESAR
# ==========================================

for libro_id, nombre in libros:

    print("\n" + "=" * 60)
    print(nombre)

    chunks = obtener_chunks_libro(libro_id)

    votos = []

    for n, chunk in enumerate(chunks, start=1):

        try:

            categoria = clasificar_chunk(chunk)
            votos.append(categoria)

            print(f"Chunk {n}: {categoria}")

        except Exception as e:

            print(f"Error chunk {n}: {e}")

    if not votos:
        continue

    contador = Counter(votos)

    categoria_final = (
        contador
        .most_common(1)[0][0]
    )

    print("\nVotacion:")
    print(contador)

    print(
        f"\n🏆 Categoria final: {categoria_final}"
    )

    cursor.execute("""
    UPDATE libros
    SET tematica = ?
    WHERE id = ?
    """,
    (
        categoria_final,
        libro_id
    ))

    conexion.commit()

conexion.close()

print("\n✅ Clasificacion terminada")
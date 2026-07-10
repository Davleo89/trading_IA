import sqlite3
import pickle
import numpy as np
import ollama

from sentence_transformers import SentenceTransformer
from memoria import MemoriaConversacion
from config import LIBROS_DB_PATH, EMBEDDING_MODEL, LLM_MODEL
from biblioteca.clasificador import clasificar_pregunta

# ==================================================
# MEMORIA DE CONVERSACIÓN
# ==================================================
memoria = MemoriaConversacion()

# ==================================================
# MODELO DE EMBEDDINGS
# ==================================================
# Nota: se carga al importar, pero podría moverse a inicialización diferida
modelo = SentenceTransformer(EMBEDDING_MODEL)

# ==================================================
# CONEXIÓN SQLITE
# ==================================================
conexion = sqlite3.connect(LIBROS_DB_PATH)
cursor = conexion.cursor()

# ==================================================
# SIMILITUD COSENO
# ==================================================
def similitud_coseno(a, b):
    norma_a = np.linalg.norm(a)
    norma_b = np.linalg.norm(b)

    if norma_a == 0 or norma_b == 0:
        return 0

    return np.dot(a, b) / (norma_a * norma_b)

# ==================================================
# BUSCAMOS LOS CHUNKS RELEVANTES
# ==================================================
def buscar_chunks(pregunta, categoria, top=3, score_min=0.40):
    embedding_pregunta = modelo.encode(pregunta)

    cursor.execute("""
    SELECT
        chunks.chunk_text,
        libros.nombre_archivo,
        libros.tematica,
        embeddings.vector
    FROM chunks
    JOIN embeddings ON chunks.id = embeddings.chunk_id
    JOIN libros ON chunks.libro_id = libros.id
    WHERE libros.tematica = ?
    """, (categoria,))

    resultados = []
    for texto, libro, categoria, vector_blob in cursor.fetchall():
        vector = pickle.loads(vector_blob)
        score = similitud_coseno(embedding_pregunta, vector)
        resultados.append((texto, libro, categoria, score))

    resultados.sort(reverse=True, key=lambda x: x[3])

    resultados_filtrados = [
        r for r in resultados[:10] if r[3] >= score_min
    ]

    return resultados_filtrados[:top]

# ==================================================
# CONSTRUIMOS EL CONTEXTO PARA LA IA
# ==================================================
def obtener_contexto(chunks):
    contexto = ""
    for texto, libro, categoria, score in chunks:
        contexto += f"""
            Libro: {libro}
            Categoría: {categoria}
            Score: {score:.4f}

        {texto}
        ----------------------------------
        """
    if len(chunks) == 0:
        return "No se encontró información suficientemente relevante en la base de conocimiento."
    return contexto

def obtener_fuentes(chunks):
    return [
        {"libro": libro, "categoria": categoria, "score": score}
        for _, libro, categoria, score in chunks
    ]

def calcular_confianza(chunks):
    if not chunks:
        return 0
    scores = [score for _, _, _, score in chunks]
    promedio = sum(scores) / len(scores)
    return round(promedio * 100, 2)

# ==================================================
# CONSULTAMOS A LA IA
# ==================================================
def preguntar_ia(pregunta, categoria):
    chunks = buscar_chunks(pregunta, categoria)
    contexto_rag = obtener_contexto(chunks)
    fuentes = obtener_fuentes(chunks)
    confianza = calcular_confianza(chunks)

    historial = memoria.get_context()

    prompt = f"""
    Eres un experto en trading.
    
    Historial:

    {historial}

    Información recuperada:

    {contexto_rag}

    Pregunta:

    {pregunta}
    """

    respuesta = ollama.chat(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    respuesta_texto = respuesta["message"]["content"]
    respuesta_texto += f"\n\nNivel de confianza: {confianza:.2f}%"

    memoria.add_user(pregunta)
    memoria.add_assistant(respuesta_texto)

    texto_fuentes = "\n\nFuentes utilizadas:\n"
    for fuente in fuentes[:5]:
        texto_fuentes += (
            f"\nLibro: {fuente['libro']}\n"
            f"Categoria: {fuente['categoria']}\n"
            f"Confianza: {fuente['score']:.4f}\n"
        )

    return respuesta_texto + texto_fuentes

# ==================================================
# FLUJO PRINCIPAL (INTERACTIVO)
# ==================================================
def main():
    try:
        while True:
            pregunta = input("\nPregunta: ")
            if pregunta.lower() == "salir":
                break

            categoria = clasificar_pregunta(pregunta)
            respuesta = preguntar_ia(pregunta, categoria)

            print("\nRespuesta:\n")
            print(respuesta)

    finally:
        conexion.close()

if __name__ == "__main__":
    main()

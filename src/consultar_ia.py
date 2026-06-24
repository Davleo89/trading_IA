import sqlite3
import pickle
import numpy as np
import ollama

from sentence_transformers import SentenceTransformer
from memoria import MemoriaConversacion
from config import DB_PATH
from config import EMBEDDING_MODEL
from config import LLM_MODEL

memoria = MemoriaConversacion()

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
# SIMILITUD COSENO
# ==================================================
def similitud_coseno(a, b):

    norma_a = np.linalg.norm(a)
    norma_b = np.linalg.norm(b)

    if norma_a == 0 or norma_b == 0:
        return 0

    return np.dot(a, b) / (
        norma_a * norma_b
    )
    
# ==================================================
# BUSCAMOS LOS CHUNKS RELEVANTES
# ==================================================
def buscar_chunks(pregunta, top = 3, score_min = 0.50):
    # Obtener el embedding de la pregunta
    embedding_pregunta = modelo.encode(pregunta)
    
    cursor.execute("""
    SELECT
    chunks.chunk_text,
    libros.nombre_archivo,
    libros.categoria,
    embeddings.vector
    FROM chunks
    JOIN embeddings
    ON chunks.id = embeddings.chunk_id
    JOIN libros
    ON chunks.libro_id = libros.id
    """)

    resultados = []

    for texto, libro, categoria, vector_blob in cursor.fetchall():
        vector = pickle.loads(vector_blob)
        score = similitud_coseno(
            embedding_pregunta,
            vector
        )

        resultados.append(
            (
            texto,
            libro,
            categoria,
            score
            )
        )   
    
    resultados.sort(
    reverse = True,
    key = lambda x: x[3]
    )
    
    resultados_filtrados = []
    for resultado in resultados:
        if resultado[3] >= score_min:
            resultados_filtrados.append(resultado)
            
    print(f"Chunks encontrados: {len(resultados)}")
    print(f"Chunks validos: {len(resultados_filtrados)}")
    return resultados_filtrados[:top]

# ==================================================
# CONSTRUIMOS EL CONTEXTO PARA LA IA
# ==================================================
def obtener_contexto(pregunta):
    chunks = buscar_chunks(pregunta)
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

def obtener_fuentes(pregunta):
    chunks = buscar_chunks(pregunta)
    fuentes = []
    for texto, libro, categoria, score in chunks:
        fuentes.append(
            {
                "libro": libro,
                "categoria": categoria,
                "score": score
            }
        )
    return fuentes

def calcular_confianza(chunks):
    if not chunks:
        return 0
    scores = [
        score
        for _, _, _, score in chunks
    ]
    promedio = sum(scores) / len(scores)
    return round(
        promedio * 100,
        2
    )

# ==================================================
# CONSULTAMOS A LA IA
# ==================================================
def preguntar_ia(pregunta):
    contexto_rag = obtener_contexto(
    pregunta
    )
    
    fuentes = obtener_fuentes(pregunta)
    chunks = buscar_chunks(pregunta)
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
        model = LLM_MODEL,
        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    
    respuesta_texto = (
    respuesta["message"]["content"]
    )
    respuesta_texto += (
        f"\n\nNivel de confianza: "
        f"{confianza:.2f}%"
    )

    memoria.add_user(
        pregunta
    )

    memoria.add_assistant(
        respuesta_texto
    )
    
    texto_fuentes = "\n\nFuentes utilizadas:\n"
    for fuente in fuentes[:5]:
        texto_fuentes += (
            f"\n"
            f"Libro: {fuente['libro']}\n"
            f"Categoria: {fuente['categoria']}\n"
            f"Confianza: {fuente['score']:.4f}\n"
        )
    
    respuesta_final = (respuesta_texto + texto_fuentes)

    return respuesta_final

while True:
    pregunta = input(
        "\nPregunta: "
    )
    
    if pregunta.lower() == "salir":
        break

    respuesta = preguntar_ia(
        pregunta
    )

    print("\nRespuesta:\n")
    print(respuesta)
    


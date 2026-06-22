import sqlite3
import pickle
import numpy as np
import ollama

from sentence_transformers import SentenceTransformer

# ==================================================
# MODELO DE EMBEDDINGS
# ==================================================
modelo = SentenceTransformer("all-MiniLM-L6-v2")

# ==================================================
# CONEXIÓN SQLITE
# ==================================================
conexion = sqlite3.connect("libros_trading.db")
cursor = conexion.cursor()

# ==================================================
# SIMILITUD COSENO
# ==================================================
def similitud_coseno(a, b):
    
    return np.dot(a, b) / (
        np.linalg.norm(a) * 
        np.linalg.norm(b)
    )
    
# ==================================================
# BUSCAMOS LOS CHUNKS RELEVANTES
# ==================================================
def buscar_chunks(pregunta, top = 10):
    # Obtener el embedding de la pregunta
    embedding_pregunta = modelo.encode(pregunta)
    
    cursor.execute("""
    SELECT 
        chunks.chunk_text, 
        embeddings.vector
    FROM chunks
    JOIN embeddings 
    ON chunks.id = embeddings.chunk_id
    """)

    resultados = []

    for texto, vector_blob in cursor.fetchall():
        vector = pickle.loads(vector_blob)
        score = similitud_coseno(embedding_pregunta, vector)
        resultados.append((texto, score))
    
    resultados.sort(
        reverse = True,
        key = lambda x: x[1]
    )
    
    return resultados[:top]

# ==================================================
# CONSTRUIMOS EL CONTEXTO PARA LA IA
# ==================================================
def obtener_contexto(pregunta):
    chunks = buscar_chunks(pregunta)
    contexto = ""
    for texto, score in chunks:
        contexto += texto + "\n\n"
    return contexto

# ==================================================
# CONSULTAMOS A LA IA
# ==================================================
def preguntar_ia(pregunta):
    contexto = obtener_contexto(pregunta)
    
    prompt = f"""
    Eres un experto en trading. Responde utilizando únicamente la información proporcionada. 
    Contexto: {contexto}
    Pregunta: {pregunta}
    """
    respuesta = ollama.chat(
        model = "qwen2.5:3b",
        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return respuesta["message"]["content"]
    

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

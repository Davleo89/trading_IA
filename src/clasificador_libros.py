import sqlite3
import ollama
import json
import time

from config import DB_PATH
from config import LLM_MODEL
from config import (
    cargar_json,
    cargar_prompt,
    CATEGORIAS_JSON,
    ALIAS_CAT_JSON,
    CLASIFICAR_PROMPT
)

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
# CLASIFICAR LIBROS
# ==========================================

categorias = cargar_json(CATEGORIAS_JSON)

# ==========================================
# NORMALIZADOR
# ==========================================

alias = cargar_json(ALIAS_CAT_JSON)

def normalizar_categoria(categoria):
    categoria = (
        categoria
        .lower()
        .replace("*", "")
        .replace('"', "")
        .replace("'", "")
        .replace(".", "")
        .replace(":", "")
        .strip()
    )
    
    for palabra_clave, categoria_real in alias.items():
        if palabra_clave in categoria:
            return categoria_real
    
    return "Trading General"

# ==========================================
# CONSTRUIR PROMPT
# ==========================================

PROMPT_CLASIFICAR = cargar_prompt(CLASIFICAR_PROMPT)

def construir_prompt(nombre, resumen, chunks, categorias):
    texto_chunks = ""
    for i, chunk in enumerate(chunks, start=1):
        texto_chunks += (
            f"- Fragmento {i}: "
            f"{chunk[:800]}\n"
        )
        
    texto_categorias = "\n".join(
    f"- {c}"
    for c in categorias
    )
        
    prompt = (
        PROMPT_CLASIFICAR   
        .replace("{NOMBRE}", nombre)
        .replace("{RESUMEN}", resumen)
        .replace("{CHUNKS}", texto_chunks)
        .replace("{CATEGORIAS}", texto_categorias)
    )
    
    return prompt

# ==========================================
# OBTENER INFORMACION DEL LIBRO
# ==========================================
def obtener_info_libro(libro_id):
    cursor.execute("""
    SELECT

    nombre_archivo,
    resumen

    FROM libros
    
    WHERE id = ?
    """,
    (libro_id,)
    )

    fila = cursor.fetchone()
    
    if fila is None:
        return None
        
    return {
        "nombre": fila[0],
        "resumen": fila[1],
        "chunks": obtener_chunks_libro(libro_id)
    }

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
# GUARDADO
# ==========================================

def guardar_categoria(libro_id, categoria):
    cursor.execute("""
    UPDATE libros
    SET tematica = ?
    WHERE id = ?
    """,
    (
        categoria,
        libro_id
    ))
    conexion.commit()

# ==========================================
# CLASIFICACION
# ==========================================

def clasificar_libro(info_libro):
    
    prompt = construir_prompt(
        nombre = info_libro["nombre"],
        resumen = info_libro["resumen"],
        chunks = info_libro["chunks"],
        categorias = categorias
    )
    
    respuesta = ollama.chat(
        model = LLM_MODEL,
        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    categoria = respuesta["message"]["content"]

    print(f"🤖 Respuesta del modelo: {categoria!r}")
    
    return normalizar_categoria(categoria)

def main():
    
    inicio = time.time()

    cursor.execute("""
    SELECT id
    FROM libros
    """)

    libros = cursor.fetchall()
    total_libros = len(libros)
    libros_ok = 0
    libros_error = 0

    for numero, (libro_id,) in enumerate(libros, start=1):
        
        print("\n" + "=" * 60)
        print(f"📚 Libro {numero} de {total_libros}")

        try:
            
            info_libro = obtener_info_libro(libro_id)

            if info_libro is None:
                print("⚠ No se encontró información del libro.")
                continue
        
            print(f"📖 {info_libro['nombre']}")
            print("🧠 Preparando clasificación...")

            categoria = clasificar_libro(info_libro)
            print(f"🏷  Categoría: {categoria}")
            print("💾 Guardando en la base de datos...")

            guardar_categoria(libro_id, categoria)
            print("✅ Guardado correctamente.")
            
            libros_ok += 1
            
        except Exception as e:
            
            libros_error += 1
            
            print("\n" + "=" * 60)
            print("❌ ERROR")
            print(f"Libro ID: {libro_id}")
            print(f"Tipo: {type(e).__name__}")
            print(f"Descripción: {e}")
            print("⏭ Continuando con el siguiente libro...")
            
            continue
        
    print("\n" + "=" * 60)
    print("📊 RESUMEN FINAL")
    print(f"✅ Libros clasificados correctamente: {libros_ok}")
    print(f"❌ Libros con error: {libros_error}")
        
    fin = time.time()
    tiempo_total = fin - inicio
    print(f"⏱ Tiempo total de ejecución: {tiempo_total:.2f} segundos")
    print("\n" + "=" * 60)
    
if __name__ == "__main__":
        main()

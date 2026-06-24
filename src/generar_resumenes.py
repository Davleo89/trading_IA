import sqlite3
import ollama
import json

from config import DB_PATH
from config import LLM_MODEL

# ==================================================
# CONEXIÓN
# ==================================================

conexion = sqlite3.connect(DB_PATH)
cursor = conexion.cursor()

# ==================================================
# LIBROS SIN RESUMEN
# ==================================================

cursor.execute("""
SELECT
    id,
    nombre_archivo,
    texto_completo
FROM libros
WHERE resumen IS NULL
OR resumen = ''
""")

libros = cursor.fetchall()

print(f"\n📚 Libros pendientes: {len(libros)}")

# ==================================================
# PROCESAR LIBROS
# ==================================================

for libro_id, nombre_archivo, texto_completo in libros:
    print(f"\nProcesando: {nombre_archivo}")
    tamano = len(texto_completo)
    inicio = texto_completo[:1500]
    medio = texto_completo[
        tamano // 2:
        tamano // 2 + 1500
    ]
    final = texto_completo[-1500:]
    
    texto_muestra = (inicio + "\n\n" + medio + "\n\n" + final)
    
    prompt = f"""
    Analiza el siguiente fragmento de un libro.

    Responde SOLO con JSON válido.

    No agregues explicaciones.
    No uses markdown.
    No uses bloques ```json.

    Ejemplo:

    {{
        "tematica": "Analisis Tecnico",
        "resumen": "Libro enfocado en..."
    }}

    Temáticas permitidas:

    - Analisis Tecnico
    - Psicologia del Trading
    - Gestion de Riesgo
    - Inversion
    - Historia de Mercados
    - Trading General

    Fragmento:

    {texto_muestra}
    """

    try:
        respuesta = ollama.chat(
            model=LLM_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        contenido = respuesta["message"]["content"].strip()

        if contenido.startswith("```json"):
            contenido = contenido.replace("```json", "")
            contenido = contenido.replace("```", "")
            contenido = contenido.strip()

        datos = json.loads(contenido)

        tematica = datos.get(
            "tematica",
            "Sin Clasificar"
        )

        resumen = datos.get(
            "resumen",
            "Resumen no disponible"
        )

        # ------------------------------------------
        # GUARDAR TODO
        # ------------------------------------------

        cursor.execute("""
        UPDATE libros
        SET
            resumen = ?,
            tematica = ?
        WHERE id = ?
        """,
        (
            resumen,
            tematica,
            libro_id
        ))

        conexion.commit()
        print(
            f"✅ Guardado | {tematica}"
        )

    except Exception as e:
        print(
            f"❌ Error: {e}"
        )

# ==================================================
# FINALIZAR
# ==================================================

conexion.close()
print("\n🚀 Resúmenes completados")
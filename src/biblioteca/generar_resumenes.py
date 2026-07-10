import sqlite3
import ollama
import json

from config import LIBRO_DB_PATH
from config import LLM_MODEL

# ==================================================
# FUNCIÓN PRINCIPAL PARA EL PIPELINE
# ==================================================

def main():
    # Establecemos la conexión de base de datos de manera local y segura
    conexion = sqlite3.connect(LIBRO_DB_PATH)
    cursor = conexion.cursor()
    
    try:
        # 1. Obtener libros sin resumen
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

        print(f"  📚 Libros pendientes por resumir: {len(libros)}")

        # 2. Procesar libros con el LLM
        for libro_id, nombre_archivo, texto_completo in libros:
            print(f"  📖 Procesando: {nombre_archivo}")
            
            tamano = len(texto_completo)
            inicio = texto_completo[:1500]
            medio = texto_completo[tamano // 2 : tamano // 2 + 1500]
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
                "tematica": "Analisis Técnico",
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

                # Limpieza manual por si el modelo ignora el prompt y pone triple backticks
                if contenido.startswith("```json"):
                    contenido = contenido.replace("```json", "")
                    contenido = contenido.replace("```", "")
                    contenido = contenido.strip()

                datos = json.loads(contenido)

                tematica = datos.get("tematica", "Sin Clasificar")
                resumen = datos.get("resumen", "Resumen no disponible")

                # Guardar el progreso de este libro
                cursor.execute("""
                UPDATE libros
                SET
                    resumen = ?,
                    tematica = ?
                WHERE id = ?
                """, (resumen, tematica, libro_id))

                conexion.commit()
                print(f"     ✅ Guardado | {tematica}")

            except Exception as e:
                print(f"     ❌ Error procesando {nombre_archivo}: {e}")
                # Continuamos con el siguiente libro sin tumbar todo el bucle interno
                continue

        print("\n🚀 Generación de resúmenes completada con éxito.")

    except Exception as e:
        # Si hay un error estructural pesado de base de datos, levantamos la excepción
        conexion.rollback()
        raise e
        
    finally:
        # El cierre de la conexión está garantizado pase lo que pase
        conexion.close()

if __name__ == "__main__":
    main()
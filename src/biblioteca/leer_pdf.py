
import sqlite3
from pypdf import PdfReader

from config import DB_PATH
from config import PDF_PATH

# ==================================================
# FUNCIÓN PRINCIPAL PARA EL PIPELINE
# ==================================================

def main():
    # Establecemos la conexión dentro de la función para el pipeline
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    
    try:
        # 1. Crear tabla si no existe
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS libros (
            id INTEGER PRIMARY KEY,
            nombre_archivo TEXT UNIQUE,
            texto_completo TEXT,
            resumen TEXT
        )
        """)
        conexion.commit()

        # 2. Verificar la ruta y leer los PDFs
        if PDF_PATH.exists():
            archivos = [
                archivo
                for archivo in PDF_PATH.iterdir()
                if archivo.suffix.lower() == ".pdf"
            ]

            print(f"  📚 PDFs encontrados en la carpeta: {len(archivos)}")

            for archivo in archivos:
                print(f"  📖 Leyendo: {archivo.name}")
                
                try:
                    reader = PdfReader(str(archivo))
                    texto_completo = ""

                    # Extrae texto saltándose las primeras 15 páginas
                    for pagina in reader.pages[15:]:
                        texto_completo += pagina.extract_text() or ""

                    cursor.execute("""
                    INSERT OR IGNORE INTO libros (nombre_archivo, texto_completo)
                    VALUES (?, ?)
                    """, (archivo.name, texto_completo))

                    print(f"     ✅ Guardado e indexado: {archivo.name}")

                except Exception as e:
                    print(f"     ❌ Error al procesar {archivo.name}: {e}")
            
            # Guardamos todos los cambios al finalizar el bucle
            conexion.commit()
            print("\n🚀 Lectura y almacenamiento de PDFs completado.")
            
        else:
            print(f"  ⚠️ No existe la carpeta especificada en: {PDF_PATH.resolve()}")

    except Exception as e:
        # En caso de un fallo general en la base de datos, deshacemos cambios
        conexion.rollback()
        raise e
        
    finally:
        # Garantizamos que la base de datos se cierre pase lo que pase
        conexion.close()

# Permite ejecutar el módulo de forma aislada para pruebas rápidas
if __name__ == "__main__":
    main()
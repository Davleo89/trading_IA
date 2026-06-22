import os
import sqlite3
from pypdf import PdfReader

# =====================================================================
# 1. CONFIGURACIÓN DE LA BASE DE DATOS SQLITE
# =====================================================================
# Se conecta a la base de datos (si el archivo no existe, lo crea automáticamente)
conexion = sqlite3.connect("libros_trading.db")
cursor = conexion.cursor()

# Creamos la tabla si no existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS libros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_archivo TEXT UNIQUE,
    categoria TEXT,
    texto_completo TEXT
)
""")
conexion.commit()

# =====================================================================
# 2. CONFIGURACIÓN DE RUTAS Y CATEGORÍAS
# =====================================================================
categorias = {
    "Analisis Tecnico": "pdf_books/analisis_tecnico",
    "Gestion de Riesgos": "pdf_books/gestion_de_riesgos",
    "Inspiracion y Experiencia": "pdf_books/inspiracion_experiencia",
    "Psicologia del Trading": "pdf_books/psicologia_trading"
}

# =====================================================================
# 3. LECTURA DE PDFs E INSERCIÓN EN LA BASE DE DATOS
# =====================================================================
for categoria, ruta_carpeta in categorias.items():
    print(f"\n--- Procesando categoría: {categoria} ---")
    
    if os.path.exists(ruta_carpeta):
        for archivo in os.listdir(ruta_carpeta):
            if archivo.lower().endswith('.pdf'):
                ruta_completa = os.path.join(ruta_carpeta, archivo)
                print(f"Leyendo: {archivo}...")
                
                try:
                    # Extraer el texto del PDF
                    reader = PdfReader(ruta_completa)
                    texto_completo = ""
                    for page in reader.pages:
                        texto_completo += page.extract_text() or ""
                    
                    # Insertar en SQLite de forma segura
                    # Usamos 'INSERT OR IGNORE' para que si vuelves a correr el script,
                    # no duplique los libros que ya guardaste previamente.
                    cursor.execute("""
                        INSERT OR IGNORE INTO libros (nombre_archivo, categoria, texto_completo)
                        VALUES (?, ?, ?)
                    """, (archivo, categoria, texto_completo))
                    
                    print(f"  ✅ Guardado en SQLite: {archivo}")
                    
                except Exception as e:
                    print(f"  ❌ Error al procesar {archivo}: {e}")
    else:
        print(f"⚠️ La carpeta {ruta_carpeta} no existe.")

# Guardar los cambios definitivos y cerrar la conexión
conexion.commit()
conexion.close()
print("\n🚀 ¡Proceso terminado! Base de datos 'libros_trading.db' creada y guardada con éxito.")
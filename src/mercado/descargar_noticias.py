# ==================================================
# IMPORTS
# ==================================================

import requests
import sqlite3

from config import (
    NEWSAPI_URL_BASE,
    NEWSAPI_KEY,
    NOTICIAS_QUERY,
    NOTICIAS_IDIOMA,
    NOTICIAS_LIMITE,
    HTTP_TIMEOUT,
    NOTICIAS_DB_PATH,
    NOTICIAS_PROVIDER,   # Nuevo: fuente centralizada
)
from utils import logger

from config import NOTICIAS_DB_PATH
NOTICIAS_DB_PATH.parent.mkdir(parents=True, exist_ok=True)


# ==================================================
# CONFIGURACIÓN INTERNA
# ==================================================

AGREGADOR = NOTICIAS_PROVIDER  # coherencia con config

# ==================================================
# 1. GESTIÓN DE BASE DE DATOS
# ==================================================

def inicializar_tabla_noticias(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS noticias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fuente TEXT,
        origen TEXT,
        url TEXT UNIQUE,
        fecha TEXT,
        titulo TEXT,
        contenido TEXT,
        categoria TEXT,
        resumen TEXT DEFAULT NULL
    )
    """)
    # La categoría será asignada posteriormente por el módulo de clasificación IA.
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_noticias_url ON noticias(url)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_noticias_fecha ON noticias(fecha)")

# ==================================================
# 2. CONEXIÓN Y OBTENCIÓN (HTTP API)
# ==================================================

def consultar_api_noticias():
    params = {
        "q": NOTICIAS_QUERY,
        "language": NOTICIAS_IDIOMA,
        "pageSize": NOTICIAS_LIMITE,
        "apiKey": NEWSAPI_KEY,
    }
    respuesta = requests.get(
        NEWSAPI_URL_BASE,
        params=params,
        timeout=HTTP_TIMEOUT
    )
    respuesta.raise_for_status()
    return respuesta.json()

# ==================================================
# 3. CAPA DE ADAPTACIÓN (TRANSFORMAR JSON)
# ==================================================

def transformar_json_a_noticias(respuesta_cruda):
    if "articles" not in respuesta_cruda:
        raise KeyError("La respuesta no contiene 'articles'.")

    noticias = []
    for art in respuesta_cruda["articles"]:
        noticias.append({
            "fuente": AGREGADOR,
            "origen": art.get("source", {}).get("name"),
            "url": art.get("url"),
            "fecha": art.get("publishedAt"),
            "titulo": art.get("title"),
            "contenido": art.get("content"),
            "categoria": "",   # Se clasificará posteriormente mediante IA
            "resumen": None
        })
    return noticias

# ==================================================
# 4. ALMACENAMIENTO (GUARDAR SQLITE)
# ==================================================

def guardar_noticias(cursor, noticias_estandarizadas):
    registros_insertados = 0
    for n in noticias_estandarizadas:
        cursor.execute("""
            INSERT OR IGNORE INTO noticias 
            (fuente, origen, url, fecha, titulo, contenido, categoria, resumen)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            n["fuente"], n["origen"], n["url"], n["fecha"],
            n["titulo"], n["contenido"], n["categoria"], n["resumen"]
        ))
        if cursor.rowcount > 0:
            registros_insertados += 1
    return registros_insertados

# ==================================================
# FLUJO PRINCIPAL (PIPELINE STEP)
# ==================================================

def main():
    conexion = sqlite3.connect(NOTICIAS_DB_PATH)
    cursor = conexion.cursor()

    try:
        logger.escribir_log("=== INICIO DEL MÓDULO descargar_noticias ===", nivel="info")

        inicializar_tabla_noticias(cursor)

        logger.escribir_log("Descargando noticias...", nivel="info")
        logger.escribir_log(f"Proveedor: {AGREGADOR}", nivel="info")

        respuesta_cruda = consultar_api_noticias()
        noticias = transformar_json_a_noticias(respuesta_cruda)

        logger.escribir_log(f"Noticias descargadas: {len(noticias)}", nivel="info")

        nuevos = guardar_noticias(cursor, noticias)
        conexion.commit()  # commit justo después de guardar

        logger.escribir_log(f"Nuevos registros: {nuevos}", nivel="success")
        logger.escribir_log("=== FINALIZANDO MÓDULO descargar_noticias ===", nivel="info")

    except Exception as e:
        conexion.rollback()
        logger.escribir_log(f"Error en el flujo de noticias: {e}", nivel="error")
    finally:
        conexion.close()

if __name__ == "__main__":
    main()

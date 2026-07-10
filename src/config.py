from pathlib import Path
import json
import os

# ==================================================
# 1. RUTAS BASES
# ==================================================
ROOT_PATH = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT_PATH / "config"
JSON_PATH = CONFIG_PATH / "json"
PROMPT_PATH = CONFIG_PATH / "prompts"
DATA_PATH = ROOT_PATH / "data"
TOOLS_PATH = ROOT_PATH / "tools"
LOGS_PATH = ROOT_PATH / "logs"

# ==================================================
# 2. DIRECTORIOS (Contenedores)
# ==================================================
PDF_PATH = DATA_PATH / "pdf_books"
BACKUP_PATH = DATA_PATH / "backups"
EMBEDDINGS_PATH = DATA_PATH / "embeddings"

PDF_PAGINAS_IGNORADAS = 15

# Carpeta para noticias crudas (JSON originales)
NOTICIAS_RAW_PATH = DATA_PATH / "noticias_raw"

# ==================================================
# 3. BASES DE DATOS POR DOMINIO
# ==================================================
LIBROS_DB_PATH = DATA_PATH / "libros.db"
NOTICIAS_DB_PATH = DATA_PATH / "noticias.db"
INDICADORES_DB_PATH = DATA_PATH / "indicadores.db"
ECONOMIA_DB_PATH = DATA_PATH / "economia.db"
CRIPTOS_DB_PATH = DATA_PATH / "criptomonedas.db"

# ==================================================
# 4. RED Y CONECTIVIDAD
# ==================================================
HTTP_TIMEOUT = 30  # Tiempo límite (segundos) para solicitudes HTTP

# ==================================================
# 5. CONFIGURACIÓN DEL MERCADO - NOTICIAS
# ==================================================
NOTICIAS_PROVIDER = "NewsAPI"
NEWSAPI_URL_BASE = "https://newsapi.org/v2/everything"
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "e0b0f92d5b1945519f053882b8057736")

NOTICIAS_IDIOMA = "es"
NOTICIAS_LIMITE = 50
NOTICIAS_QUERY = 'trading OR "market" OR "crypto" OR "finanzas"'
NOTICIAS_ORDEN = "publishedAt"
NOTICIAS_DIAS = 7

# ==================================================
# 6. INTELIGENCIA ARTIFICIAL (IA)
# ==================================================
LLM_MODEL = "qwen2.5:3b"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

TEMPERATURE = 0.0
MAX_CONTEXT = 4096
TOP_K = 20

# ==================================================
# 7. RECURSOS (JSON y Prompts)
# ==================================================
CATEGORIAS_JSON = JSON_PATH / "categorias.json"
ALIAS_CAT_JSON = JSON_PATH / "alias_categorias.json"
PARAMETROS_JSON = JSON_PATH / "parametros.json"
MODELOS_JSON = JSON_PATH / "modelos.json"

CLASIFICAR_PROMPT = PROMPT_PATH / "clasificar_libros.txt"
RESPONDER_IA = PROMPT_PATH / "responder_ia.txt"
RESUMIR_LIBROS = PROMPT_PATH / "resumir_libros.txt"


# ==================================================
# 8. FUNCIONES ÚTILES (Utilidades puras de carga)
# ==================================================

def cargar_json(ruta):
    with open(
        ruta,
        "r",
        encoding = "utf-8"
    ) as archivo:
        return json.load(archivo)
    
def cargar_prompt(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        return f.read()
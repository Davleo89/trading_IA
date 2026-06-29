import json
from pathlib import Path

# ==================================================
# RUTAS BASES
# ==================================================

ROOT_PATH = Path(__file__).resolve().parent.parent

CONFIG_PATH = ROOT_PATH/"config"
JSON_PATH = CONFIG_PATH/"json"
PROMPT_PATH = CONFIG_PATH/"prompts"
DATA_PATH = ROOT_PATH/"data"
TOOLS_PATH = ROOT_PATH/"tools"


# ==================================================
# BASE DE DATOS
# ==================================================

DB_PATH = DATA_PATH/"libros_trading.db"

# ==================================================
# LIBROS PDF
# ==================================================

PDF_PATH = DATA_PATH/"pdf_books"

# ==================================================
# BACKUPS
# ==================================================

BACKUP_PATH = DATA_PATH/"backups"

# ==================================================
# MODELOS Y FUNCIONES
# ==================================================

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
LLM_MODEL = "qwen2.5:3b"

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
# ==================================================
# ARCHIVOS JSON
# ==================================================

CATEGORIAS_JSON = JSON_PATH/"categorias.json"
ALIAS_CAT_JSON = JSON_PATH/"alias_categorias.json"
PARAMETROS_JSON = JSON_PATH/"parametros.json"
MODELOS_JSON = JSON_PATH/"modelos.json"

# ==================================================
# PROMPTS
# ==================================================

CLASIFICAR_PROMPT = PROMPT_PATH/"clasificar_libros.txt"
RESPONDER_IA = PROMPT_PATH/"responder_ia.txt"
RESUMIR_LIBROS = PROMPT_PATH/"resumir_libros.txt"
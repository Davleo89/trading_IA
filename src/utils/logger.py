# ==========================================
# IMPORTS
# ==========================================

from datetime import datetime
from config import LOGS_PATH

# ==========================================
# VARIABLES GLOBALES
# ==========================================

_archivo_log = None

# ==========================================
# CREAR DIRECTORIO
# ==========================================

def crear_directorio_logs():
    LOGS_PATH.mkdir(
        parents=True, 
        exist_ok=True
        )
    return LOGS_PATH

# ==========================================
# CREAR ARCHIVO
# ==========================================

def crear_archivo_log():
    global _archivo_log
    ruta_directorio = crear_directorio_logs()
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    nombre_archivo = f"pipeline_{timestamp}.log"
    ruta_archivo_log = ruta_directorio / nombre_archivo
    
    _archivo_log = open(ruta_archivo_log, mode="w", encoding="utf-8")
    
    return ruta_archivo_log

# ==========================================
# ESCRIBIR LOG
# ==========================================

def escribir_log(mensaje, nivel="INFO"):
    global _archivo_log
    
    if _archivo_log is None:
        crear_archivo_log()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea_log = f"[{timestamp}] [{nivel.upper()}] {mensaje}"
    print(linea_log)
    
    _archivo_log.write(linea_log + "\n")
    _archivo_log.flush()

# ==========================================
# CERRAR LOG
# ==========================================

def cerrar_log():
    global _archivo_log
    
    if _archivo_log is not None:
        _archivo_log.close()
        _archivo_log = None
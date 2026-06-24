import shutil
from datetime import datetime
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.append(
    str(BASE_DIR / "src")
)

from config import (
    DB_PATH,
    BACKUP_PATH
)

BACKUP_PATH.mkdir(
    exist_ok=True
)

fecha = datetime.now().strftime(
    "%Y-%m-%d_%H-%M-%S"
)

archivo_destino = (
    BACKUP_PATH /
    f"backup_{fecha}.db"
)

shutil.copy2(
    DB_PATH,
    archivo_destino
)

print(
    f"✅ Backup creado:\n{archivo_destino}"
)
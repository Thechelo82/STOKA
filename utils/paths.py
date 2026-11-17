"""
Rutas del proyecto STOKA.

Sirve para que el programa encuentre assets, la base de datos y los logs
tanto al ejecutarse como script de Python como cuando está empaquetado en .exe
(PyInstaller extrae a una carpeta temporal).
"""
from __future__ import annotations

import sys
from pathlib import Path


def app_root() -> Path:
    if getattr(sys, "frozen", False):
        # Ejecutable: datos junto al .exe
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent


ROOT = app_root()
DATA_DIR = ROOT / "data"
DB_FILE = DATA_DIR / "stoka.db"
CHAT_LOGS_DIR = DATA_DIR / "chat_logs"
REPORTS_DIR = DATA_DIR / "reportes"
ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"


def ensure_data_dirs() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    CHAT_LOGS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

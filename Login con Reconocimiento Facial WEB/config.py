from __future__ import annotations

import os
import secrets
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "database.db"

REGISTER_SAMPLES = int(os.environ.get("REGISTER_SAMPLES", "5"))
MAX_REGISTER_SECONDS = int(os.environ.get("MAX_REGISTER_SECONDS", "60"))
MAX_LOGIN_SECONDS = int(os.environ.get("MAX_LOGIN_SECONDS", "20"))
TOLERANCE = float(os.environ.get("FACE_TOLERANCE", "0.5"))


def get_secret_key() -> str:
    """En producción definí FLASK_SECRET_KEY para que las cookies de sesión sigan válidas al reiniciar."""
    return os.environ.get("FLASK_SECRET_KEY", secrets.token_hex(32))


def get_debug() -> bool:
    return os.environ.get("FLASK_DEBUG", "").lower() in ("1", "true", "yes")


def get_host() -> str:
    return os.environ.get("FLASK_HOST", "127.0.0.1")


def get_port() -> int:
    return int(os.environ.get("PORT", "5000"))


def admin_usernames() -> set[str]:
    """
    Usuarios que pueden ver Reportes globales.
    Si la variable está vacía, cualquier usuario logueado puede ver /reportes (comportamiento demo).
    """
    raw = os.environ.get("ADMIN_USERNAMES", "")
    return {x.strip().lower() for x in raw.split(",") if x.strip()}


def can_view_reports(username: str) -> bool:
    admins = admin_usernames()
    if not admins:
        return True
    return username.strip().lower() in admins

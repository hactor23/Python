from __future__ import annotations

from typing import List, Tuple

import numpy as np

from ..db.user_repository import create_user, get_user_encodings, user_exists
from ..db.access_repository import log_access
from .face_service import capture_user_encodings, verify_user_with_camera
from ..config import DB_PATH


def register(username: str) -> Tuple[bool, str]:
    username = username.strip()
    if not username:
        return False, "Ingresa un nombre de usuario."

    try:
        if user_exists(username):
            return False, "El usuario ya existe."
    except Exception as e:
        return False, f"Error accediendo a la base de datos ({DB_PATH}): {e}"

    encodings, cancelado = capture_user_encodings()
    if cancelado:
        return False, "Registro cancelado."
    if not encodings:
        return False, "No se detectó un rostro válido. Intenta de nuevo."

    try:
        # Guardamos en DB (encodings como BLOB serializado).
        create_user(username, encodings)
        log_access(username, "REGISTER")
    except Exception as e:
        return False, f"No se pudo guardar en la base de datos ({DB_PATH}): {e}"

    # Verificación rápida de persistencia
    try:
        if not user_exists(username):
            return False, f"Registro no persistió en la base de datos ({DB_PATH})."
    except Exception as e:
        return False, f"Registro guardado, pero falló la verificación en DB ({DB_PATH}): {e}"

    return True, f"Usuario '{username}' registrado correctamente."


def login(username: str) -> Tuple[bool, str]:
    username = username.strip()
    if not username:
        return False, "Ingresa un nombre de usuario."

    try:
        if not user_exists(username):
            return False, "Usuario no existe."
    except Exception as e:
        return False, f"Error accediendo a la base de datos ({DB_PATH}): {e}"

    try:
        known_encodings = get_user_encodings(username)
    except Exception as e:
        return False, f"No se pudo leer el usuario en DB ({DB_PATH}): {e}"
    if not known_encodings:
        return False, "El usuario no tiene facciones registradas."

    ok = verify_user_with_camera(known_encodings)
    if ok:
        try:
            log_access(username, "LOGIN")
        except Exception:
            # No bloqueamos el login si falla el log de accesos.
            pass
        return True, "Acceso concedido."
    return False, "Rostro no coincide."


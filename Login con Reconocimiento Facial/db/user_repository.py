from __future__ import annotations

import pickle
from typing import List, Optional

import numpy as np

from .database import get_connection


def user_exists(username: str) -> bool:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
        return cursor.fetchone() is not None
    finally:
        conn.close()


def create_user(username: str, encodings: List[np.ndarray]) -> None:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        enc_blob = pickle.dumps(encodings, protocol=pickle.HIGHEST_PROTOCOL)
        cursor.execute(
            """
            INSERT INTO users(username, encodings)
            VALUES(?, ?)
            """,
            (username, enc_blob),
        )
        conn.commit()
    finally:
        conn.close()


def get_user_encodings(username: str) -> Optional[List[np.ndarray]]:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT encodings FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        if not row:
            return None
        (enc_blob,) = row
        encodings = pickle.loads(enc_blob)
        # Garantiza que sea lista de numpy arrays
        return [np.asarray(e, dtype=np.float64) for e in encodings]
    finally:
        conn.close()


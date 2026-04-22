from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterator

from ..config import DB_PATH


def _ensure_parent_dir_exists(db_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)


def get_connection() -> sqlite3.Connection:
    _ensure_parent_dir_exists(DB_PATH)
    # check_same_thread=False: por si usamos threads en UI.
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def init_db() -> None:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users(
                username TEXT PRIMARY KEY,
                encodings BLOB NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS access_logs(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                event TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        conn.commit()
    finally:
        conn.close()


def iter_users() -> Iterator[str]:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users ORDER BY created_at DESC")
        for (username,) in cursor.fetchall():
            yield username
    finally:
        conn.close()


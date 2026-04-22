from __future__ import annotations

from typing import Iterable, List, Optional, Sequence, Tuple

from .database import get_connection


def log_access(username: str, event: str) -> None:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO access_logs(username, event) VALUES(?, ?)",
            (username, event),
        )
        conn.commit()
    finally:
        conn.close()


def get_user_accesses(username: str, limit: int = 50) -> List[Tuple[str, str]]:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT created_at, event
            FROM access_logs
            WHERE username = ?
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (username, limit),
        )
        return [(str(created_at), str(event)) for (created_at, event) in cursor.fetchall()]
    finally:
        conn.close()


def get_access_summary_by_day(days: int = 30, limit_rows: int = 100) -> List[Tuple[str, int]]:
    """
    Devuelve una lista (dia, cantidad) agregada por fecha.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT DATE(created_at) as day, COUNT(*) as total
            FROM access_logs
            GROUP BY day
            ORDER BY day DESC
            LIMIT ?
            """,
            (min(limit_rows, days),),
        )
        return [(str(day), int(total)) for (day, total) in cursor.fetchall()]
    finally:
        conn.close()


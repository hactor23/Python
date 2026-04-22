"""
Entrada WSGI para producción (Waitress, gunicorn, etc.).

  waitress-serve --listen=127.0.0.1:5000 wsgi:application
"""
from __future__ import annotations

from app import create_app

application = create_app()

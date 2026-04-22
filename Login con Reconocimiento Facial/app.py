from __future__ import annotations

import sys
from pathlib import Path

# Soporta dos formas de ejecución:
# - python -m facial_login_menu.app (recomendado)
# - python app.py (desde dentro de la carpeta facial_login_menu)
if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from facial_login_menu.db.database import init_db
    from facial_login_menu.ui.login_window import start_login
else:
    from .db.database import init_db
    from .ui.login_window import start_login


def main() -> None:
    init_db()
    start_login()


if __name__ == "__main__":
    main()


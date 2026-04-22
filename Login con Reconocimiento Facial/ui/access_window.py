from __future__ import annotations

import tkinter as tk
from tkinter import messagebox

from ..db.access_repository import get_user_accesses


def open_access_window(parent: tk.Tk | tk.Toplevel, username: str) -> None:
    window = tk.Toplevel(parent)
    window.title("Control de Accesos")
    window.geometry("520x380")

    tk.Label(window, text=f"Accesos de: {username}", font=("Arial", 12)).pack(pady=10)

    listbox = tk.Listbox(window, width=70, height=12)
    listbox.pack(pady=8)

    status = tk.Label(window, text="", fg="gray")
    status.pack(pady=6)

    def refresh() -> None:
        listbox.delete(0, tk.END)
        rows = get_user_accesses(username, limit=100)
        if not rows:
            status.config(text="No hay accesos registrados todavía.")
            return

        for created_at, event in rows:
            listbox.insert(tk.END, f"{created_at}  |  {event}")
        status.config(text=f"Mostrando {len(rows)} registros.")

    tk.Button(window, text="Refrescar", width=20, command=refresh).pack(pady=6)
    tk.Button(window, text="Cerrar", width=20, command=window.destroy).pack(pady=10)

    try:
        refresh()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar los accesos: {e}")


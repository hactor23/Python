from __future__ import annotations

import tkinter as tk
from tkinter import messagebox

from ..db.access_repository import get_access_summary_by_day


def open_reports_window(parent: tk.Tk | tk.Toplevel, username: str) -> None:
    window = tk.Toplevel(parent)
    window.title("Reportes")
    window.geometry("540x420")

    tk.Label(window, text=f"Reportes (sesiones del sistema)", font=("Arial", 12)).pack(pady=12)

    listbox = tk.Listbox(window, width=65, height=14)
    listbox.pack(pady=8)

    status = tk.Label(window, text="", fg="gray")
    status.pack(pady=6)

    def refresh() -> None:
        listbox.delete(0, tk.END)
        try:
            rows = get_access_summary_by_day(days=30, limit_rows=200)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el reporte: {e}")
            return

        if not rows:
            status.config(text="Aún no hay datos para reportar.")
            return

        # rows viene como: (dia, total)
        for day, total in rows:
            listbox.insert(tk.END, f"{day}  |  {total} eventos")
        status.config(text="Reporte actualizado.")

    tk.Button(window, text="Refrescar", width=20, command=refresh).pack(pady=8)
    tk.Button(window, text="Cerrar", width=20, command=window.destroy).pack(pady=6)

    try:
        refresh()
    except Exception:
        # refresh ya muestra error si corresponde
        pass


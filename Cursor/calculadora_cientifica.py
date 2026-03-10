import tkinter as tk
from tkinter import messagebox
import math


class CalculadoraCientifica(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Calculadora científica")
        self.resizable(False, False)

        self.expresion = ""

        self._crear_pantalla()
        self._crear_botones()

    def _crear_pantalla(self):
        self.entrada_var = tk.StringVar()
        entrada = tk.Entry(
            self,
            textvariable=self.entrada_var,
            font=("Consolas", 18),
            justify="right",
            bd=10,
            relief=tk.RIDGE,
        )
        entrada.grid(row=0, column=0, columnspan=6, padx=10, pady=10, sticky="nsew")

    def _agregar(self, valor: str):
        self.expresion += str(valor)
        self.entrada_var.set(self.expresion)

    def _borrar(self):
        self.expresion = ""
        self.entrada_var.set("")

    def _borrar_ultimo(self):
        self.expresion = self.expresion[:-1]
        self.entrada_var.set(self.expresion)

    def _evaluar(self):
        if not self.expresion:
            return

        try:
            # Nombres permitidos para eval (sin builtins)
            nombres_permitidos = {
                "sin": math.sin,
                "cos": math.cos,
                "tan": math.tan,
                "log": math.log10,
                "ln": math.log,
                "sqrt": math.sqrt,
                "pi": math.pi,
                "e": math.e,
            }

            resultado = eval(self.expresion, {"__builtins__": None}, nombres_permitidos)
            self.expresion = str(resultado)
            self.entrada_var.set(self.expresion)
        except Exception as e:
            messagebox.showerror("Error", f"Expresión no válida\n\n{e}")
            self.expresion = ""
            self.entrada_var.set("")

    def _crear_botones(self):
        # Configurar rejilla
        for i in range(1, 7):
            self.grid_rowconfigure(i, weight=1)
        for j in range(6):
            self.grid_columnconfigure(j, weight=1)

        # Fila 1
        botones = [
            ("7", 1, 0),
            ("8", 1, 1),
            ("9", 1, 2),
            ("/", 1, 3),
            ("sin", 1, 4),
            ("cos", 1, 5),
            # Fila 2
            ("4", 2, 0),
            ("5", 2, 1),
            ("6", 2, 2),
            ("*", 2, 3),
            ("tan", 2, 4),
            ("log", 2, 5),
            # Fila 3
            ("1", 3, 0),
            ("2", 3, 1),
            ("3", 3, 2),
            ("-", 3, 3),
            ("ln", 3, 4),
            ("sqrt", 3, 5),
            # Fila 4
            ("0", 4, 0),
            (".", 4, 1),
            ("(", 4, 2),
            (")", 4, 3),
            ("^", 4, 4),
            ("=", 4, 5),
        ]

        for (texto, fila, col) in botones:
            if texto == "=":
                cmd = self._evaluar
                bg = "#4CAF50"
                fg = "white"
            else:
                cmd = (lambda t=texto: self._agregar(self._transformar_entrada(t)))
                bg = "#f0f0f0"
                fg = "black"

            b = tk.Button(
                self,
                text=texto,
                width=5,
                height=2,
                font=("Consolas", 14),
                command=cmd,
                bg=bg,
                fg=fg,
            )
            b.grid(row=fila, column=col, padx=3, pady=3, sticky="nsew")

        # Fila 5: borrar
        tk.Button(
            self,
            text="C",
            font=("Consolas", 14),
            command=self._borrar,
            bg="#f44336",
            fg="white",
        ).grid(row=5, column=0, columnspan=2, padx=3, pady=3, sticky="nsew")

        tk.Button(
            self,
            text="⌫",
            font=("Consolas", 14),
            command=self._borrar_ultimo,
        ).grid(row=5, column=2, padx=3, pady=3, sticky="nsew")

        tk.Button(
            self,
            text="+",
            font=("Consolas", 14),
            command=lambda: self._agregar("+"),
        ).grid(row=5, column=3, padx=3, pady=3, sticky="nsew")

        tk.Button(
            self,
            text="pi",
            font=("Consolas", 14),
            command=lambda: self._agregar("pi"),
        ).grid(row=5, column=4, padx=3, pady=3, sticky="nsew")

        tk.Button(
            self,
            text="e",
            font=("Consolas", 14),
            command=lambda: self._agregar("e"),
        ).grid(row=5, column=5, padx=3, pady=3, sticky="nsew")

    def _transformar_entrada(self, texto: str) -> str:
        if texto == "^":
            return "**"
        return texto


if __name__ == "__main__":
    app = CalculadoraCientifica()
    app.mainloop()


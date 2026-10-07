
import ast
import operator
import sys
import tkinter as tk
from tkinter import messagebox, ttk


class EvaluadorMatematico:
    """Clase encargada de procesar y evaluar expresiones sintácticamente válidas."""

    OPERADORES = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    @classmethod
    def calcular(cls, expresion: str):
        # Balanceo automático de paréntesis
        abiertos = expresion.count("(")
        cerrados = expresion.count(")")
        if abiertos > cerrados:
            expresion += ")" * (abiertos - cerrados)

        try:
            arbol = ast.parse(expresion, mode="eval")
            return cls._resolver_nodo(arbol.body)
        except Exception as err:
            raise ValueError("Expresión no válida") from err

    @classmethod
    def _resolver_nodo(cls, nodo):
        if isinstance(nodo, ast.Constant):
            if isinstance(nodo.value, (int, float)):
                return nodo.value
            raise ValueError("Valor no numérico")
        elif isinstance(nodo, ast.BinOp):
            izq = cls._resolver_nodo(nodo.left)
            der = cls._resolver_nodo(nodo.right)
            op_tipo = type(nodo.op)
            if op_tipo in cls.OPERADORES:
                return cls.OPERADORES[op_tipo](izq, der)
        elif isinstance(nodo, ast.UnaryOp):
            val = cls._resolver_nodo(nodo.operand)
            op_tipo = type(nodo.op)
            if op_tipo in cls.OPERADORES:
                return cls.OPERADORES[op_tipo](val)

        raise ValueError("Operación no soportada")


class AplicacionCalculadora:

    CAPACIDAD_HISTORIAL = 5

    def __init__(self, ventana_root: tk.Tk):
        self.root = ventana_root
        self.expresion_buffer = ""
        self.resetear_en_digito = False

        self._configurar_ventana()
        self._construir_interfaz()
        self._enlazar_teclado()

    def _configurar_ventana(self):
        self.root.title("Calculadora - Historial")
        self.root.geometry("360x520")
        self.root.resizable(False, False)
        self.root.configure(bg="#212529")

    def _construir_interfaz(self):
        # Contenedor Principal
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill="both", expand=True)

        # 1. Visor de Resultados
        self.var_pantalla = tk.StringVar(value="0")
        self.entry_pantalla = tk.Entry(
            main_frame,
            textvariable=self.var_pantalla,
            font=("Consolas", 22, "bold"),
            justify="right",
            bd=0,
            bg="#343a40",
            fg="#f8f9fa",
            insertbackground="#f8f9fa",
            relief="flat",
        )
        self.entry_pantalla.pack(fill="x", ipady=12, pady=(0, 15))

        # 2. Panel de Botones
        panel_grid = ttk.Frame(main_frame)
        panel_grid.pack(fill="both", expand=True)

        distribucion_botones = [
            ("C", 0, 0),
            ("(", 0, 1),
            (")", 0, 2),
            ("÷", 0, 3),
            ("7", 1, 0),
            ("8", 1, 1),
            ("9", 1, 2),
            ("×", 1, 3),
            ("4", 2, 0),
            ("5", 2, 1),
            ("6", 2, 2),
            ("-", 2, 3),
            ("1", 3, 0),
            ("2", 3, 1),
            ("3", 3, 2),
            ("+", 3, 3),
            ("0", 4, 0),
            (".", 4, 1),
            ("=", 4, 2),
        ]

        for i in range(5):
            panel_grid.rowconfigure(i, weight=1)
        for j in range(4):
            panel_grid.columnconfigure(j, weight=1)

        for simbolo, fila, col in distribucion_botones:
            # Asignación de colores por función
            bg_color = "#495057"
            fg_color = "#ffffff"

            if simbolo in ("+", "-", "×", "÷"):
                bg_color = "#fd7e14"
            elif simbolo == "=":
                bg_color = "#0d6efd"
            elif simbolo in ("C", "(", ")"):
                bg_color = "#dc3545"

            btn = tk.Button(
                panel_grid,
                text=simbolo,
                font=("Segoe UI", 13, "bold"),
                bg=bg_color,
                fg=fg_color,
                activebackground="#6c757d",
                activeforeground="#ffffff",
                bd=0,
                relief="flat",
                command=lambda s=simbolo: self._gestionar_pulsacion(s),
            )

            if simbolo == "=":
                btn.grid(
                    row=fila,
                    column=col,
                    columnspan=2,
                    sticky="nsew",
                    padx=2,
                    pady=2,
                )
            else:
                btn.grid(row=fila, column=col, sticky="nsew", padx=2, pady=2)

        # 3. Sección de Historial con Listbox
        lbl_hist = tk.Label(
            main_frame,
            text="Historial Reciente:",
            font=("Segoe UI", 9, "bold"),
            bg="#212529",
            fg="#adb5bd",
            anchor="w",
        )
        lbl_hist.pack(fill="x", pady=(15, 5))

        self.box_historial = tk.Listbox(
            main_frame,
            font=("Consolas", 9),
            height=4,
            bg="#343a40",
            fg="#e9ecef",
            bd=0,
            highlightthickness=0,
            selectbackground="#495057",
        )
        self.box_historial.pack(fill="x")

    def _enlazar_teclado(self):
        self.root.bind("<Key>", self._evento_teclado)

    def _evento_teclado(self, event):
        tecla = event.char
        if event.keysym in ("Return", "KP_Enter"):
            self._gestionar_pulsacion("=")
        elif event.keysym in ("BackSpace", "Escape"):
            self._gestionar_pulsacion("C")
        elif tecla in "0123456789+-./*()":
            mapeo = {"*": "×", "/": "÷"}
            self._gestionar_pulsacion(mapeo.get(tecla, tecla))

    def _gestionar_pulsacion(self, caracter: str):
        if caracter == "C":
            self.expresion_buffer = ""
            self.var_pantalla.set("0")
            return

        if caracter == "=":
            self._evaluar_expresion()
            return

        if self.resetear_en_digito and caracter in "0123456789":
            self.expresion_buffer = ""

        self.resetear_en_digito = False
        self.expresion_buffer += caracter
        self.var_pantalla.set(self.expresion_buffer)

    def _evaluar_expresion(self):
        if not self.expresion_buffer:
            return

        cadena_eval = (
            self.expresion_buffer.replace("÷", "/").replace("×", "*")
        )

        try:
            resultado = EvaluadorMatematico.calcular(cadena_eval)

            if isinstance(resultado, float) and resultado.is_integer():
                resultado = int(resultado)

            str_res = str(resultado)

            # Insertar en Listbox de Historial
            registro = f"{self.expresion_buffer} = {str_res}"
            self.box_historial.insert(tk.END, registro)

            if self.box_historial.size() > self.CAPACIDAD_HISTORIAL:
                self.box_historial.delete(0)

            self.box_historial.see(tk.END)

            self.var_pantalla.set(str_res)
            self.expresion_buffer = str_res
            self.resetear_en_digito = True

        except ZeroDivisionError:
            messagebox.showerror(
                "Error Matemático", "No es posible dividir entre cero."
            )
            self.expresion_buffer = ""
            self.var_pantalla.set("0")
        except Exception:
            messagebox.showwarning(
                "Sintaxis Inválida", "Verifique la expresión ingresada."
            )
            self.expresion_buffer = ""
            self.var_pantalla.set("0")


if __name__ == "__main__":
    ventana_principal = tk.Tk()
    app = AplicacionCalculadora(ventana_principal)
    ventana_principal.mainloop()
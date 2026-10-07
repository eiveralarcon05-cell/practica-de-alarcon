import ast
import operator
import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class EvaluadorSeguro:
    """Clase auxiliar para evaluar expresiones matemáticas de forma segura."""

    OPERADORES = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    @classmethod
    def evaluar(cls, expresion: str):
        # Auto-cerrar paréntesis faltantes si el usuario no los cerró
        abiertos = expresion.count("(")
        cerrados = expresion.count(")")
        if abiertos > cerrados:
            expresion += ")" * (abiertos - cerrados)

        try:
            nodo = ast.parse(expresion, mode="eval").body
            return cls._evaluar_nodo(nodo)
        except Exception as e:
            raise ValueError("Sintaxis incorrecta") from e

    @classmethod
    def _evaluar_nodo(cls, nodo):
        if isinstance(nodo, ast.Constant):  # Números en Python 3.8+
            if isinstance(nodo.value, (int, float)):
                return nodo.value
            raise ValueError("No es un número válido")
        elif isinstance(nodo, ast.BinOp):
            izq = cls._evaluar_nodo(nodo.left)
            der = cls._evaluar_nodo(nodo.right)
            tipo_op = type(nodo.op)
            if tipo_op in cls.OPERADORES:
                return cls.OPERADORES[tipo_op](izq, der)
        elif isinstance(nodo, ast.UnaryOp):
            operando = cls._evaluar_nodo(nodo.operand)
            tipo_op = type(nodo.op)
            if tipo_op in cls.OPERADORES:
                return cls.OPERADORES[tipo_op](operando)

        raise ValueError("Expresión no permitida")


class CalculadoraPySide6(QWidget):

    MAX_HISTORIAL = 5

    def __init__(self):
        super().__init__()
        self.operacion_actual = ""
        self.limpiar_en_proximo_numero = False

        self._configurar_ventana()
        self._inicializar_interfaz()
        self._aplicar_estilos()

    def _configurar_ventana(self):
        self.setWindowTitle("Calculadora Profesional - PySide6")
        self.setFixedSize(360, 520)

    def _inicializar_interfaz(self):
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(15, 15, 15, 15)
        layout_principal.setSpacing(10)

        # 1. Pantalla
        self.pantalla = QLineEdit()
        self.pantalla.setReadOnly(True)
        self.pantalla.setAlignment(Qt.AlignRight)
        self.pantalla.setPlaceholderText("0")
        layout_principal.addWidget(self.pantalla)

        # 2. Cuadrícula de Botones
        grid = QGridLayout()
        grid.setSpacing(8)

        botones = [
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

        for texto, fila, col in botones:
            btn = QPushButton(texto)
            btn.setMinimumHeight(45)

            if texto in ["+", "-", "×", "÷"]:
                btn.setProperty("rol", "operador")
            elif texto == "=":
                btn.setProperty("rol", "igual")
            elif texto in ["C", "(", ")"]:
                btn.setProperty("rol", "accion")
            else:
                btn.setProperty("rol", "numero")

            btn.clicked.connect(lambda checked, t=texto: self._procesar_entrada(t))

            if texto == "=":
                grid.addWidget(btn, fila, col, 1, 2)
            else:
                grid.addWidget(btn, fila, col)

        layout_principal.addLayout(grid)

        # 3. Historial
        lbl_historial = QLabel("Historial de operaciones:")
        layout_principal.addWidget(lbl_historial)

        self.lista_historial = QListWidget()
        self.lista_historial.setFocusPolicy(Qt.NoFocus)
        layout_principal.addWidget(self.lista_historial)

    def _aplicar_estilos(self):
        qss = """
            QWidget {
                background-color: #1e1e2e;
                color: #cdd6f4;
                font-family: 'Segoe UI', sans-serif;
            }
            QLineEdit {
                background-color: #181825;
                border: 2px solid #313244;
                border-radius: 8px;
                color: #a6e3a1;
                font-size: 28px;
                font-weight: bold;
                padding: 10px;
            }
            QLabel {
                font-size: 12px;
                color: #a6adc8;
                font-weight: 600;
            }
            QListWidget {
                background-color: #181825;
                border: 1px solid #313244;
                border-radius: 6px;
                color: #bac2de;
                font-size: 12px;
                padding: 4px;
            }
            QPushButton {
                border: none;
                border-radius: 6px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton[rol="numero"] { background-color: #313244; color: #cdd6f4; }
            QPushButton[rol="numero"]:hover { background-color: #45475a; }
            QPushButton[rol="operador"] { background-color: #fab387; color: #11111b; }
            QPushButton[rol="operador"]:hover { background-color: #f9e2af; }
            QPushButton[rol="accion"] { background-color: #f38ba8; color: #11111b; }
            QPushButton[rol="accion"]:hover { background-color: #eba0ac; }
            QPushButton[rol="igual"] { background-color: #89b4fa; color: #11111b; }
            QPushButton[rol="igual"]:hover { background-color: #b4befe; }
            QPushButton:pressed { background-color: #585b70; }
        """
        self.setStyleSheet(qss)

    def _procesar_entrada(self, valor: str):
        if valor == "C":
            self.operacion_actual = ""
            self.pantalla.clear()
            return

        if valor == "=":
            self._calcular_resultado()
            return

        if self.limpiar_en_proximo_numero and valor in "0123456789":
            self.operacion_actual = ""

        self.limpiar_en_proximo_numero = False
        self.operacion_actual += valor
        self.pantalla.setText(self.operacion_actual)

    def _calcular_resultado(self):
        if not self.operacion_actual:
            return

        expr_eval = (
            self.operacion_actual.replace("÷", "/")
            .replace("×", "*")
            .replace("x", "*")
        )

        try:
            resultado = EvaluadorSeguro.evaluar(expr_eval)

            if isinstance(resultado, float) and resultado.is_integer():
                resultado = int(resultado)

            res_str = str(resultado)

            item_historial = f"{self.operacion_actual} = {res_str}"
            self.lista_historial.addItem(item_historial)

            if self.lista_historial.count() > self.MAX_HISTORIAL:
                self.lista_historial.takeItem(0)

            self.lista_historial.scrollToBottom()

            self.pantalla.setText(res_str)
            self.operacion_actual = res_str
            self.limpiar_en_proximo_numero = True

        except ZeroDivisionError:
            self.pantalla.setText("Error: Div / 0")
            self.operacion_actual = ""
        except Exception:
            self.pantalla.setText("Error de sintaxis")
            self.operacion_actual = ""

    def keyPressEvent(self, event):
        key = event.key()
        text = event.text()

        if key in (Qt.Key_Return, Qt.Key_Enter):
            self._procesar_entrada("=")
        elif key in (Qt.Key_Escape, Qt.Key_Backspace):
            self._procesar_entrada("C")
        elif text in "0123456789+-./*()":
            mapa_teclas = {"*": "×", "/": "÷"}
            self._procesar_entrada(mapa_teclas.get(text, text))
        else:
            super().keyPressEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    calc = CalculadoraPySide6()
    calc.show()
    sys.exit(app.exec())
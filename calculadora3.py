import ast
import operator
import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class EvaluadorMatematicoSeguro:
    """Procesador que evalúa expresiones matemáticas sin usar eval()."""

    OPERADORES = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    @classmethod
    def resolver(cls, expresion: str):
        # Auto-cierre de paréntesis faltantes
        abiertos = expresion.count("(")
        cerrados = expresion.count(")")
        if abiertos > cerrados:
            expresion += ")" * (abiertos - cerrados)

        try:
            nodo = ast.parse(expresion, mode="eval").body
            return cls._evaluar_nodo(nodo)
        except Exception as e:
            raise ValueError("Expresión matemática inválida") from e

    @classmethod
    def _evaluar_nodo(cls, nodo):
        if isinstance(nodo, ast.Constant):
            if isinstance(nodo.value, (int, float)):
                return nodo.value
            raise ValueError("Nodo no numérico")
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

        raise ValueError("Operación no permitida")


class OrbitCalcPro(QMainWindow):

    LIMITE_HISTORIAL = 5

    def __init__(self):
        super().__init__()
        self.expresion_buffer = ""
        self.limpiar_al_escribir = False

        self._configurar_ventana_principal()
        self._construir_menu_superior()
        self._construir_interfaz_grafica()
        self._aplicar_hoja_estilos()

    def _configurar_ventana_principal(self):
        self.setWindowTitle("OrbitCalc Pro - Sistema de Cálculo")
        self.setFixedSize(400, 620)

    def _construir_menu_superior(self):
        bar_menu = self.menuBar()

        # Menú Archivo
        menu_archivo = bar_menu.addMenu("Archivo")
        
        act_nuevo = QAction("Nueva Operación", self)
        act_nuevo.setShortcut(QKeySequence("Ctrl+N"))
        act_nuevo.triggered.connect(self._reiniciar_calculadora)
        menu_archivo.addAction(act_nuevo)

        menu_archivo.addSeparator()

        act_salir = QAction("Salir", self)
        act_salir.setShortcut(QKeySequence("Ctrl+Q"))
        act_salir.triggered.connect(self.close)
        menu_archivo.addAction(act_salir)

        # Menú Editar
        menu_editar = bar_menu.addMenu("Editar")
        
        act_copiar = QAction("Copiar Resultado", self)
        act_copiar.setShortcut(QKeySequence("Ctrl+C"))
        act_copiar.triggered.connect(self._copiar_resultado)
        menu_editar.addAction(act_copiar)

        act_borrar = QAction("Limpiar Todo", self)
        act_borrar.triggered.connect(self._reiniciar_calculadora)
        menu_editar.addAction(act_borrar)

        # Menú Ayuda
        menu_ayuda = bar_menu.addMenu("Ayuda")
        
        act_acerca = QAction("Acerca de", self)
        act_acerca.triggered.connect(self._dialogo_acerca_de)
        menu_ayuda.addAction(act_acerca)

        act_info = QAction("Información del Sistema", self)
        act_info.triggered.connect(self._dialogo_informacion)
        menu_ayuda.addAction(act_info)

    def _construir_interfaz_grafica(self):
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        
        layout_main = QVBoxLayout(widget_central)
        layout_main.setContentsMargins(18, 18, 18, 18)
        layout_main.setSpacing(12)

        # Encabezado
        lbl_brand = QLabel("◆ ORBITCALC PRO")
        lbl_brand.setProperty("rol", "brand")
        layout_main.addWidget(lbl_brand)

        # Pantalla Visor
        self.pantalla = QLineEdit()
        self.pantalla.setReadOnly(True)
        self.pantalla.setAlignment(Qt.AlignRight)
        self.pantalla.setPlaceholderText("0")
        layout_main.addWidget(self.pantalla)

        # Matriz de Botones
        grid = QGridLayout()
        grid.setSpacing(8)

        botones = [
            ("C", 0, 0), ("(", 0, 1), (")", 0, 2), ("÷", 0, 3),
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("×", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("-", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("+", 3, 3),
            ("0", 4, 0), (".", 4, 1), ("=", 4, 2)
        ]

        for texto, fila, col in botones:
            btn = QPushButton(texto)
            btn.setMinimumHeight(46)

            # Clasificación de roles para estilos CSS
            if texto in ["÷", "×", "-", "+"]:
                btn.setProperty("rol", "operador")
            elif texto == "=":
                btn.setProperty("rol", "igual")
            elif texto in ["C", "(", ")"]:
                btn.setProperty("rol", "accion")
            else:
                btn.setProperty("rol", "numero")

            btn.clicked.connect(lambda checked, t=texto: self._gestionar_tecla(t))

            if texto == "=":
                grid.addWidget(btn, fila, col, 1, 2)
            else:
                grid.addWidget(btn, fila, col)

        layout_main.addLayout(grid)

        # Contenedor del Historial
        lbl_hist_title = QLabel("📋 Historial de Operaciones:")
        lbl_hist_title.setProperty("rol", "subtitulo")
        layout_main.addWidget(lbl_hist_title)

        self.lista_historial = QListWidget()
        self.lista_historial.setFocusPolicy(Qt.NoFocus)
        layout_main.addWidget(self.lista_historial)

    def _aplicar_hoja_estilos(self):
        qss = """
            QMainWindow {
                background-color: #0f172a;
            }
            QMenuBar {
                background-color: #1e293b;
                color: #f8fafc;
                font-family: 'Segoe UI', sans-serif;
                font-size: 13px;
                padding: 2px;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 6px 12px;
                border-radius: 4px;
            }
            QMenuBar::item:selected {
                background-color: #334155;
            }
            QMenu {
                background-color: #1e293b;
                color: #f8fafc;
                border: 1px solid #475569;
                font-family: 'Segoe UI', sans-serif;
            }
            QMenu::item {
                padding: 6px 24px;
            }
            QMenu::item:selected {
                background-color: #0284c7;
                color: #ffffff;
            }
            QLabel[rol="brand"] {
                color: #38bdf8;
                font-size: 13px;
                font-weight: bold;
                letter-spacing: 1px;
            }
            QLabel[rol="subtitulo"] {
                color: #94a3b8;
                font-size: 11px;
                font-weight: 600;
            }
            QLineEdit {
                background-color: #1e293b;
                border: 2px solid #334155;
                border-radius: 8px;
                color: #f8fafc;
                font-size: 26px;
                font-weight: bold;
                padding: 8px;
            }
            QListWidget {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 8px;
                color: #cbd5e1;
                font-size: 12px;
                padding: 4px;
            }
            QPushButton {
                font-family: 'Segoe UI', sans-serif;
                font-size: 16px;
                font-weight: bold;
                border-radius: 6px;
                border: none;
            }
            QPushButton[rol="numero"] {
                background-color: #334155;
                color: #f8fafc;
            }
            QPushButton[rol="numero"]:hover {
                background-color: #475569;
            }
            QPushButton[rol="operador"] {
                background-color: #0284c7;
                color: #ffffff;
            }
            QPushButton[rol="operador"]:hover {
                background-color: #0369a1;
            }
            QPushButton[rol="accion"] {
                background-color: #e11d48;
                color: #ffffff;
            }
            QPushButton[rol="accion"]:hover {
                background-color: #be123c;
            }
            QPushButton[rol="igual"] {
                background-color: #10b981;
                color: #ffffff;
            }
            QPushButton[rol="igual"]:hover {
                background-color: #059669;
            }
            QPushButton:pressed {
                opacity: 0.8;
            }
        """
        self.setStyleSheet(qss)

    def _gestionar_tecla(self, valor: str):
        if valor == "C":
            self._limpiar_pantalla()
            return

        if valor == "=":
            self._procesar_evaluacion()
            return

        if self.limpiar_al_escribir and valor in "0123456789":
            self.expresion_buffer = ""

        self.limpiar_al_escribir = False
        self.expresion_buffer += valor
        self.pantalla.setText(self.expresion_buffer)

    def _procesar_evaluacion(self):
        if not self.expresion_buffer:
            return

        expr_preparada = (
            self.expresion_buffer.replace("÷", "/")
            .replace("×", "*")
            .replace("x", "*")
        )

        try:
            resultado = EvaluadorMatematicoSeguro.resolver(expr_preparada)

            if isinstance(resultado, float) and resultado.is_integer():
                resultado = int(resultado)

            res_str = str(resultado)

            # Insertar en QListWidget
            registro = f"{self.expresion_buffer} = {res_str}"
            self.lista_historial.addItem(registro)

            if self.lista_historial.count() > self.LIMITE_HISTORIAL:
                self.lista_historial.takeItem(0)

            self.lista_historial.scrollToBottom()

            self.pantalla.setText(res_str)
            self.expresion_buffer = res_str
            self.limpiar_al_escribir = True

        except ZeroDivisionError:
            self.pantalla.setText("Error: Div / 0")
            self.expresion_buffer = ""
        except Exception:
            self.pantalla.setText("Error de Sintaxis")
            self.expresion_buffer = ""

    def _limpiar_pantalla(self):
        self.expresion_buffer = ""
        self.pantalla.clear()

    def _reiniciar_calculadora(self):
        self._limpiar_pantalla()
        self.lista_historial.clear()

    def _copiar_resultado(self):
        texto = self.pantalla.text()
        if texto and texto not in ["Error: Div / 0", "Error de Sintaxis"]:
            QApplication.clipboard().setText(texto)

    def _dialogo_acerca_de(self):
        QMessageBox.information(
            self,
            "Acerca de OrbitCalc",
            "OrbitCalc Pro v2.0\n\nDesarrollado con PySide6.\nEvaluación sintáctica segura mediante AST.",
        )

    def _dialogo_informacion(self):
        QMessageBox.information(
            self,
            "Información del Sistema",
            "Calculadora científica/básica estructurada con la arquitectura de QMainWindow.\n"
            "Soporta operaciones aritméticas, historial dinámico y atajos de teclado.",
        )

    def keyPressEvent(self, event):
        key = event.key()
        text = event.text()

        if key in (Qt.Key_Return, Qt.Key_Enter):
            self._gestionar_tecla("=")
        elif key in (Qt.Key_Escape, Qt.Key_Backspace):
            self._gestionar_tecla("C")
        elif text in "0123456789+-./*()":
            mapeo = {"*": "×", "/": "÷"}
            self._gestionar_tecla(mapeo.get(text, text))
        else:
            super().keyPressEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    calc = OrbitCalcPro()
    calc.show()
    sys.exit(app.exec())
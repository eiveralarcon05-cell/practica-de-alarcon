import ast
import math
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
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
)


# ============================================================
# EVALUADOR MATEMÁTICO SEGURO
# ============================================================

class EvaluadorMatematicoSeguro:
    """
    Evalúa expresiones matemáticas sin utilizar eval().
    """

    OPERADORES = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    FUNCIONES = {
        "sqrt": math.sqrt,
        "abs": abs,
        "floor": math.floor,
        "ceil": math.ceil,
    }

    CONSTANTES = {
        "pi": math.pi,
        "e": math.e,
    }

    @classmethod
    def resolver(cls, expresion: str, grados=False):

        # Convertir símbolos visuales
        expresion = expresion.replace("×", "*")
        expresion = expresion.replace("÷", "/")
        expresion = expresion.replace("^", "**")
        expresion = expresion.replace("π", "pi")

        # Auto-cierre de paréntesis
        abiertos = expresion.count("(")
        cerrados = expresion.count(")")

        if abiertos > cerrados:
            expresion += ")" * (abiertos - cerrados)

        try:
            nodo = ast.parse(
                expresion,
                mode="eval"
            ).body

            return cls._evaluar_nodo(
                nodo,
                grados
            )

        except ZeroDivisionError:
            raise

        except Exception as e:
            raise ValueError(
                "Expresión matemática inválida"
            ) from e

    @classmethod
    def _evaluar_nodo(cls, nodo, grados=False):

        # Números
        if isinstance(nodo, ast.Constant):

            if isinstance(
                nodo.value,
                (int, float)
            ):
                return nodo.value

            raise ValueError(
                "Valor no permitido"
            )

        # Variables / constantes
        if isinstance(nodo, ast.Name):

            if nodo.id in cls.CONSTANTES:
                return cls.CONSTANTES[nodo.id]

            raise ValueError(
                f"Variable no permitida: {nodo.id}"
            )

        # Operaciones binarias
        if isinstance(nodo, ast.BinOp):

            izq = cls._evaluar_nodo(
                nodo.left,
                grados
            )

            der = cls._evaluar_nodo(
                nodo.right,
                grados
            )

            tipo_op = type(nodo.op)

            if tipo_op in cls.OPERADORES:

                return cls.OPERADORES[tipo_op](
                    izq,
                    der
                )

            raise ValueError(
                "Operador no permitido"
            )

        # Operaciones unarias
        if isinstance(nodo, ast.UnaryOp):

            operando = cls._evaluar_nodo(
                nodo.operand,
                grados
            )

            tipo_op = type(nodo.op)

            if tipo_op in cls.OPERADORES:

                return cls.OPERADORES[tipo_op](
                    operando
                )

            raise ValueError(
                "Operador no permitido"
            )

        # Funciones
        if isinstance(nodo, ast.Call):

            if not isinstance(
                nodo.func,
                ast.Name
            ):
                raise ValueError(
                    "Función no permitida"
                )

            nombre = nodo.func.id

            if len(nodo.args) != 1:
                raise ValueError(
                    "Las funciones requieren un argumento"
                )

            argumento = cls._evaluar_nodo(
                nodo.args[0],
                grados
            )

            # Funciones trigonométricas
            if nombre == "sin":

                if grados:
                    argumento = math.radians(argumento)

                return math.sin(argumento)

            if nombre == "cos":

                if grados:
                    argumento = math.radians(argumento)

                return math.cos(argumento)

            if nombre == "tan":

                if grados:
                    argumento = math.radians(argumento)

                return math.tan(argumento)

            # Trigonométricas inversas
            if nombre == "asin":

                resultado = math.asin(argumento)

                if grados:
                    return math.degrees(resultado)

                return resultado

            if nombre == "acos":

                resultado = math.acos(argumento)

                if grados:
                    return math.degrees(resultado)

                return resultado

            if nombre == "atan":

                resultado = math.atan(argumento)

                if grados:
                    return math.degrees(resultado)

                return resultado

            # Logaritmos
            if nombre == "log":
                return math.log10(argumento)

            if nombre == "ln":
                return math.log(argumento)

            # Otras funciones
            if nombre in cls.FUNCIONES:

                return cls.FUNCIONES[nombre](
                    argumento
                )

            raise ValueError(
                f"Función no permitida: {nombre}"
            )

        raise ValueError(
            "Operación no permitida"
        )


# ============================================================
# APLICACIÓN PRINCIPAL
# ============================================================

class OrbitCalcPro(QMainWindow):

    LIMITE_HISTORIAL = 10

    def __init__(self):

        super().__init__()

        self.expresion_buffer = ""
        self.limpiar_al_escribir = False
        self.grados = True

        self._configurar_ventana()
        self._construir_menu()
        self._construir_interfaz()
        self._aplicar_estilos()

    # ========================================================
    # CONFIGURACIÓN
    # ========================================================

    def _configurar_ventana(self):

        self.setWindowTitle(
            "OrbitCalc Pro - Calculadora Científica"
        )

        self.setFixedSize(
            460,
            720
        )

    # ========================================================
    # MENÚ
    # ========================================================

    def _construir_menu(self):

        barra = self.menuBar()

        # ---------------- ARCHIVO ----------------

        menu_archivo = barra.addMenu(
            "Archivo"
        )

        accion_nuevo = QAction(
            "Nueva operación",
            self
        )

        accion_nuevo.setShortcut(
            QKeySequence("Ctrl+N")
        )

        accion_nuevo.triggered.connect(
            self._reiniciar_calculadora
        )

        menu_archivo.addAction(
            accion_nuevo
        )

        menu_archivo.addSeparator()

        accion_salir = QAction(
            "Salir",
            self
        )

        accion_salir.setShortcut(
            QKeySequence("Ctrl+Q")
        )

        accion_salir.triggered.connect(
            self.close
        )

        menu_archivo.addAction(
            accion_salir
        )

        # ---------------- EDITAR ----------------

        menu_editar = barra.addMenu(
            "Editar"
        )

        accion_copiar = QAction(
            "Copiar resultado",
            self
        )

        accion_copiar.setShortcut(
            QKeySequence("Ctrl+C")
        )

        accion_copiar.triggered.connect(
            self._copiar_resultado
        )

        menu_editar.addAction(
            accion_copiar
        )

        accion_borrar = QAction(
            "Limpiar todo",
            self
        )

        accion_borrar.triggered.connect(
            self._reiniciar_calculadora
        )

        menu_editar.addAction(
            accion_borrar
        )

        # ---------------- MODO ----------------

        menu_modo = barra.addMenu(
            "Modo"
        )

        self.accion_grados = QAction(
            "Grados",
            self
        )

        self.accion_grados.setCheckable(
            True
        )

        self.accion_grados.setChecked(
            True
        )

        self.accion_grados.triggered.connect(
            self._cambiar_grados
        )

        menu_modo.addAction(
            self.accion_grados
        )

        self.accion_radianes = QAction(
            "Radianes",
            self
        )

        self.accion_radianes.setCheckable(
            True
        )

        self.accion_radianes.triggered.connect(
            self._cambiar_radianes
        )

        menu_modo.addAction(
            self.accion_radianes
        )

        # ---------------- AYUDA ----------------

        menu_ayuda = barra.addMenu(
            "Ayuda"
        )

        accion_acerca = QAction(
            "Acerca de",
            self
        )

        accion_acerca.triggered.connect(
            self._dialogo_acerca
        )

        menu_ayuda.addAction(
            accion_acerca
        )

        accion_funciones = QAction(
            "Funciones disponibles",
            self
        )

        accion_funciones.triggered.connect(
            self._mostrar_funciones
        )

        menu_ayuda.addAction(
            accion_funciones
        )

    # ========================================================
    # INTERFAZ
    # ========================================================

    def _construir_interfaz(self):

        central = QWidget()

        self.setCentralWidget(
            central
        )

        layout_principal = QVBoxLayout(
            central
        )

        layout_principal.setContentsMargins(
            18,
            18,
            18,
            18
        )

        layout_principal.setSpacing(
            10
        )

        # Marca

        marca = QLabel(
            "◆ ORBITCALC PRO"
        )

        marca.setProperty(
            "rol",
            "brand"
        )

        layout_principal.addWidget(
            marca
        )

        # Indicador de modo

        self.lbl_modo = QLabel(
            "MODO: GRADOS"
        )

        self.lbl_modo.setProperty(
            "rol",
            "modo"
        )

        layout_principal.addWidget(
            self.lbl_modo
        )

        # Pantalla

        self.pantalla = QLineEdit()

        self.pantalla.setReadOnly(
            True
        )

        self.pantalla.setAlignment(
            Qt.AlignRight
        )

        self.pantalla.setPlaceholderText(
            "0"
        )

        layout_principal.addWidget(
            self.pantalla
        )

        # ====================================================
        # BOTONES CIENTÍFICOS
        # ====================================================

        grid_cientifico = QGridLayout()

        grid_cientifico.setSpacing(
            6
        )

        cientificos = [
            ("sin", 0, 0),
            ("cos", 0, 1),
            ("tan", 0, 2),
            ("√", 0, 3),

            ("asin", 1, 0),
            ("acos", 1, 1),
            ("atan", 1, 2),
            ("x²", 1, 3),

            ("log", 2, 0),
            ("ln", 2, 1),
            ("π", 2, 2),
            ("e", 2, 3),
        ]

        for texto, fila, columna in cientificos:

            boton = QPushButton(
                texto
            )

            boton.setMinimumHeight(
                38
            )

            boton.setProperty(
                "rol",
                "cientifico"
            )

            boton.clicked.connect(
                lambda checked,
                t=texto:
                self._gestionar_tecla(t)
            )

            grid_cientifico.addWidget(
                boton,
                fila,
                columna
            )

        layout_principal.addLayout(
            grid_cientifico
        )

        # ====================================================
        # BOTONES PRINCIPALES
        # ====================================================

        grid = QGridLayout()

        grid.setSpacing(
            7
        )

        botones = [

            ("C", 0, 0),
            ("⌫", 0, 1),
            ("(", 0, 2),
            (")", 0, 3),

            ("7", 1, 0),
            ("8", 1, 1),
            ("9", 1, 2),
            ("÷", 1, 3),

            ("4", 2, 0),
            ("5", 2, 1),
            ("6", 2, 2),
            ("×", 2, 3),

            ("1", 3, 0),
            ("2", 3, 1),
            ("3", 3, 2),
            ("-", 3, 3),

            ("0", 4, 0),
            (".", 4, 1),
            ("^", 4, 2),
            ("+", 4, 3),

            ("%", 5, 0),
            ("CE", 5, 1),
            ("=", 5, 2),
            ("", 5, 3),
        ]

        for texto, fila, columna in botones:

            if texto == "":
                continue

            boton = QPushButton(
                texto
            )

            boton.setMinimumHeight(
                44
            )

            if texto in [
                "÷",
                "×",
                "-",
                "+",
                "^"
            ]:

                boton.setProperty(
                    "rol",
                    "operador"
                )

            elif texto == "=":

                boton.setProperty(
                    "rol",
                    "igual"
                )

            elif texto in [
                "C",
                "CE",
                "⌫",
                "(",
                ")",
                "%"
            ]:

                boton.setProperty(
                    "rol",
                    "accion"
                )

            else:

                boton.setProperty(
                    "rol",
                    "numero"
                )

            boton.clicked.connect(
                lambda checked,
                t=texto:
                self._gestionar_tecla(t)
            )

            grid.addWidget(
                boton,
                fila,
                columna
            )

        layout_principal.addLayout(
            grid
        )

        # ====================================================
        # HISTORIAL
        # ====================================================

        titulo_historial = QLabel(
            "📋 Historial de operaciones"
        )

        titulo_historial.setProperty(
            "rol",
            "subtitulo"
        )

        layout_principal.addWidget(
            titulo_historial
        )

        self.lista_historial = QListWidget()

        self.lista_historial.setFocusPolicy(
            Qt.NoFocus
        )

        layout_principal.addWidget(
            self.lista_historial
        )

    # ========================================================
    # ESTILOS
    # ========================================================

    def _aplicar_estilos(self):

        qss = """

        QMainWindow {
            background-color: #0f172a;
        }

        QMenuBar {
            background-color: #1e293b;
            color: #f8fafc;
            font-size: 13px;
        }

        QMenuBar::item {
            padding: 6px 12px;
        }

        QMenuBar::item:selected {
            background-color: #334155;
        }

        QMenu {
            background-color: #1e293b;
            color: #f8fafc;
            border: 1px solid #475569;
        }

        QMenu::item {
            padding: 7px 25px;
        }

        QMenu::item:selected {
            background-color: #0284c7;
        }

        QLabel[rol="brand"] {
            color: #38bdf8;
            font-size: 16px;
            font-weight: bold;
        }

        QLabel[rol="modo"] {
            color: #10b981;
            font-size: 10px;
            font-weight: bold;
        }

        QLabel[rol="subtitulo"] {
            color: #94a3b8;
            font-size: 11px;
            font-weight: bold;
        }

        QLineEdit {
            background-color: #1e293b;
            border: 2px solid #334155;
            border-radius: 9px;
            color: #f8fafc;
            font-size: 28px;
            font-weight: bold;
            padding: 10px;
            min-height: 45px;
        }

        QPushButton {
            font-family: 'Segoe UI';
            font-size: 15px;
            font-weight: bold;
            border-radius: 7px;
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
            color: white;
        }

        QPushButton[rol="operador"]:hover {
            background-color: #0369a1;
        }

        QPushButton[rol="accion"] {
            background-color: #e11d48;
            color: white;
        }

        QPushButton[rol="accion"]:hover {
            background-color: #be123c;
        }

        QPushButton[rol="igual"] {
            background-color: #10b981;
            color: white;
        }

        QPushButton[rol="igual"]:hover {
            background-color: #059669;
        }

        QPushButton[rol="cientifico"] {
            background-color: #475569;
            color: #bae6fd;
        }

        QPushButton[rol="cientifico"]:hover {
            background-color: #64748b;
        }

        QListWidget {
            background-color: #1e293b;
            border: 1px solid #334155;
            border-radius: 8px;
            color: #cbd5e1;
            font-size: 12px;
            padding: 5px;
        }

        """

        self.setStyleSheet(
            qss
        )

    # ========================================================
    # GESTIÓN DE BOTONES
    # ========================================================

    def _gestionar_tecla(
        self,
        valor: str
    ):

        # Limpiar todo
        if valor == "C":

            self._limpiar_pantalla()

            return

        # CE
        if valor == "CE":

            self._limpiar_pantalla()

            return

        # Borrar último carácter
        if valor == "⌫":

            if self.expresion_buffer:

                self.expresion_buffer = (
                    self.expresion_buffer[:-1]
                )

                self.pantalla.setText(
                    self.expresion_buffer
                )

            return

        # Igual
        if valor == "=":

            self._procesar_evaluacion()

            return

        # Funciones científicas
        funciones = [
            "sin",
            "cos",
            "tan",
            "asin",
            "acos",
            "atan",
            "sqrt",
            "log",
            "ln"
        ]

        if valor in funciones:

            if (
                self.limpiar_al_escribir
                or not self.expresion_buffer
            ):

                self.expresion_buffer = ""

            self.expresion_buffer += (
                valor + "("
            )

            self.limpiar_al_escribir = False

            self.pantalla.setText(
                self.expresion_buffer
            )

            return

        # Raíz cuadrada
        if valor == "√":

            self.expresion_buffer += "sqrt("

            self.limpiar_al_escribir = False

            self.pantalla.setText(
                self.expresion_buffer
            )

            return

        # Cuadrado
        if valor == "x²":

            if self.expresion_buffer:

                self.expresion_buffer += "^2"

                self.pantalla.setText(
                    self.expresion_buffer
                )

            return

        # Pi
        if valor == "π":

            if self.limpiar_al_escribir:

                self.expresion_buffer = ""

            self.expresion_buffer += "π"

            self.limpiar_al_escribir = False

            self.pantalla.setText(
                self.expresion_buffer
            )

            return

        # e
        if valor == "e":

            if self.limpiar_al_escribir:

                self.expresion_buffer = ""

            self.expresion_buffer += "e"

            self.limpiar_al_escribir = False

            self.pantalla.setText(
                self.expresion_buffer
            )

            return

        # Después de obtener resultado,
        # escribir un número comienza nueva operación
        if (
            self.limpiar_al_escribir
            and valor in "0123456789."
        ):

            self.expresion_buffer = ""

        self.limpiar_al_escribir = False

        self.expresion_buffer += valor

        self.pantalla.setText(
            self.expresion_buffer
        )

    # ========================================================
    # EVALUACIÓN
    # ========================================================

    def _procesar_evaluacion(self):

        if not self.expresion_buffer:

            return

        try:

            resultado = (
                EvaluadorMatematicoSeguro.resolver(
                    self.expresion_buffer,
                    self.grados
                )
            )

            if isinstance(
                resultado,
                float
            ):

                if resultado.is_integer():

                    resultado = int(
                        resultado
                    )

                else:

                    resultado = round(
                        resultado,
                        12
                    )

            resultado_str = str(
                resultado
            )

            registro = (
                f"{self.expresion_buffer} = "
                f"{resultado_str}"
            )

            self.lista_historial.addItem(
                registro
            )

            if (
                self.lista_historial.count()
                > self.LIMITE_HISTORIAL
            ):

                self.lista_historial.takeItem(
                    0
                )

            self.lista_historial.scrollToBottom()

            self.pantalla.setText(
                resultado_str
            )

            self.expresion_buffer = (
                resultado_str
            )

            self.limpiar_al_escribir = True

        except ZeroDivisionError:

            self.pantalla.setText(
                "Error: división por 0"
            )

            self.expresion_buffer = ""

        except ValueError as e:

            self.pantalla.setText(
                "Error de sintaxis"
            )

            self.expresion_buffer = ""

        except OverflowError:

            self.pantalla.setText(
                "Número demasiado grande"
            )

            self.expresion_buffer = ""

        except Exception:

            self.pantalla.setText(
                "Error"
            )

            self.expresion_buffer = ""

    # ========================================================
    # LIMPIAR
    # ========================================================

    def _limpiar_pantalla(self):

        self.expresion_buffer = ""

        self.pantalla.clear()

        self.limpiar_al_escribir = False

    def _reiniciar_calculadora(self):

        self._limpiar_pantalla()

        self.lista_historial.clear()

    # ========================================================
    # COPIAR
    # ========================================================

    def _copiar_resultado(self):

        texto = self.pantalla.text()

        if texto:

            QApplication.clipboard().setText(
                texto
            )

    # ========================================================
    # MODO GRADOS
    # ========================================================

    def _cambiar_grados(self):

        self.grados = True

        self.accion_grados.setChecked(
            True
        )

        self.accion_radianes.setChecked(
            False
        )

        self.lbl_modo.setText(
            "MODO: GRADOS"
        )

    # ========================================================
    # MODO RADIANES
    # ========================================================

    def _cambiar_radianes(self):

        self.grados = False

        self.accion_grados.setChecked(
            False
        )

        self.accion_radianes.setChecked(
            True
        )

        self.lbl_modo.setText(
            "MODO: RADIANES"
        )

    # ========================================================
    # ACERCA DE
    # ========================================================

    def _dialogo_acerca(self):

        QMessageBox.information(
            self,
            "Acerca de OrbitCalc Pro",
            "ORBITCALC PRO\n\n"
            "Calculadora científica desarrollada "
            "con Python y PySide6.\n\n"
            "Características:\n"
            "• Operaciones aritméticas\n"
            "• Potencias\n"
            "• Porcentajes\n"
            "• Trigonometría\n"
            "• Logaritmos\n"
            "• Constantes π y e\n"
            "• Historial\n"
            "• Modo grados/radianes\n"
            "• Evaluación segura con AST"
        )

    # ========================================================
    # FUNCIONES DISPONIBLES
    # ========================================================

    def _mostrar_funciones(self):

        QMessageBox.information(
            self,
            "Funciones disponibles",
            "OPERACIONES:\n\n"
            "+    Suma\n"
            "-    Resta\n"
            "×    Multiplicación\n"
            "÷    División\n"
            "^    Potencia\n"
            "%    Módulo\n\n"
            "FUNCIONES:\n\n"
            "sin(x)\n"
            "cos(x)\n"
            "tan(x)\n"
            "asin(x)\n"
            "acos(x)\n"
            "atan(x)\n"
            "sqrt(x)\n"
            "log(x)  → logaritmo base 10\n"
            "ln(x)   → logaritmo natural\n\n"
            "CONSTANTES:\n\n"
            "π\n"
            "e"
        )

    # ========================================================
    # TECLADO
    # ========================================================

    def keyPressEvent(self, event):

        key = event.key()

        texto = event.text()

        if key in (
            Qt.Key_Return,
            Qt.Key_Enter
        ):

            self._gestionar_tecla("=")

            return

        if key == Qt.Key_Backspace:

            self._gestionar_tecla("⌫")

            return

        if key == Qt.Key_Escape:

            self._gestionar_tecla("C")

            return

        if texto in "0123456789":

            self._gestionar_tecla(
                texto
            )

            return

        if texto in "+-().":

            self._gestionar_tecla(
                texto
            )

            return

        if texto == "*":

            self._gestionar_tecla(
                "×"
            )

            return

        if texto == "/":

            self._gestionar_tecla(
                "÷"
            )

            return

        if texto == "^":

            self._gestionar_tecla(
                "^"
            )

            return

        super().keyPressEvent(
            event
        )


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":

    app = QApplication(
        sys.argv
    )

    calculadora = OrbitCalcPro()

    calculadora.show()

    sys.exit(
        app.exec()
    )

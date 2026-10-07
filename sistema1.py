import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit, QPushButton,
    QCheckBox, QRadioButton, QComboBox, QButtonGroup,
    QFrame
)
from PySide6.QtCore import Qt


class AnalizadorTextoPySide6(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Analizador de Texto")
        self.resize(650, 650)

        # =========================
        # ESTILO GENERAL
        # =========================
        self.setStyleSheet("""
            QWidget {
                background-color: #121826;
                color: #E5E7EB;
                font-family: "Segoe UI";
                font-size: 14px;
            }

            QLabel#titulo {
                color: #35E0A0;
                font-size: 28px;
                font-weight: bold;
            }

            QLabel#subtitulo {
                color: #9CA3AF;
                font-size: 14px;
            }

            QLabel#seccion {
                color: #FFFFFF;
                font-size: 16px;
                font-weight: bold;
                margin-top: 8px;
            }

            QLineEdit, QComboBox, QTextEdit {
                background-color: #1B2433;
                border: 1px solid #303B4F;
                border-radius: 10px;
                padding: 10px;
                color: #FFFFFF;
            }

            QLineEdit:focus, QComboBox:focus, QTextEdit:focus {
                border: 1px solid #35E0A0;
            }

            QComboBox {
                padding: 10px;
            }

            QComboBox QAbstractItemView {
                background-color: #1B2433;
                color: white;
                selection-background-color: #35E0A0;
                selection-color: #121826;
            }

            QCheckBox, QRadioButton {
                spacing: 8px;
                color: #D1D5DB;
            }

            QCheckBox::indicator,
            QRadioButton::indicator {
                width: 17px;
                height: 17px;
            }

            QPushButton {
                background-color: #35E0A0;
                color: #121826;
                border: none;
                border-radius: 10px;
                padding: 12px;
                font-size: 15px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #2BC88C;
            }

            QPushButton:pressed {
                background-color: #22A875;
            }

            QLabel#resultado {
                background-color: #182B29;
                border: 1px solid #286B58;
                border-radius: 10px;
                padding: 15px;
                color: #35E0A0;
                font-size: 15px;
                font-weight: bold;
            }

            QFrame#tarjeta {
                background-color: #171F2E;
                border: 1px solid #273247;
                border-radius: 15px;
            }

            QScrollBar:vertical {
                background: #121826;
                width: 10px;
            }

            QScrollBar::handle:vertical {
                background: #303B4F;
                border-radius: 5px;
            }
        """)

        # =========================
        # LAYOUT PRINCIPAL
        # =========================
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(25, 20, 25, 20)
        layout_principal.setSpacing(15)

        # =========================
        # ENCABEZADO
        # =========================
        titulo = QLabel("🔎 Analizador de Texto")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignCenter)

        subtitulo = QLabel(
            "Analiza, transforma y guarda tus textos fácilmente"
        )
        subtitulo.setObjectName("subtitulo")
        subtitulo.setAlignment(Qt.AlignCenter)

        layout_principal.addWidget(titulo)
        layout_principal.addWidget(subtitulo)

        # =========================
        # TARJETA DE ENTRADA
        # =========================
        tarjeta_entrada = QFrame()
        tarjeta_entrada.setObjectName("tarjeta")

        layout_entrada = QVBoxLayout(tarjeta_entrada)
        layout_entrada.setContentsMargins(20, 20, 20, 20)
        layout_entrada.setSpacing(12)

        lbl_texto = QLabel("📝 Texto de entrada")
        lbl_texto.setObjectName("seccion")
        layout_entrada.addWidget(lbl_texto)

        self.input_texto = QLineEdit()
        self.input_texto.setPlaceholderText("Escribe aquí una frase o texto...")
        self.input_texto.returnPressed.connect(self.procesar)
        layout_entrada.addWidget(self.input_texto)

        lbl_operacion = QLabel("⚙️ Operación")
        lbl_operacion.setObjectName("seccion")
        layout_entrada.addWidget(lbl_operacion)

        self.combo_op = QComboBox()
        self.combo_op.addItems([
            "Contar Caracteres",
            "Contar Palabras",
            "Convertir a Mayúsculas",
            "Invertir Texto"
        ])
        layout_entrada.addWidget(self.combo_op)

        self.chk_espacios = QCheckBox(
            "Incluir espacios en el conteo de caracteres"
        )
        self.chk_espacios.setChecked(True)
        layout_entrada.addWidget(self.chk_espacios)

        layout_principal.addWidget(tarjeta_entrada)

        # =========================
        # OPCIONES DE HISTORIAL
        # =========================
        tarjeta_historial = QFrame()
        tarjeta_historial.setObjectName("tarjeta")

        layout_historial_op = QVBoxLayout(tarjeta_historial)
        layout_historial_op.setContentsMargins(20, 15, 20, 15)

        lbl_guardar = QLabel("💾 ¿Guardar resultado en el historial?")
        lbl_guardar.setObjectName("seccion")
        layout_historial_op.addWidget(lbl_guardar)

        row_radio = QHBoxLayout()

        self.radio_si = QRadioButton("Sí")
        self.radio_no = QRadioButton("No")

        self.radio_si.setChecked(True)

        self.bg_historial = QButtonGroup(self)
        self.bg_historial.addButton(self.radio_si)
        self.bg_historial.addButton(self.radio_no)

        row_radio.addWidget(self.radio_si)
        row_radio.addWidget(self.radio_no)
        row_radio.addStretch()

        layout_historial_op.addLayout(row_radio)

        layout_principal.addWidget(tarjeta_historial)

        # =========================
        # BOTÓN
        # =========================
        self.btn_procesar = QPushButton("🚀  Analizar / Procesar")
        self.btn_procesar.setMinimumHeight(48)
        self.btn_procesar.clicked.connect(self.procesar)

        layout_principal.addWidget(self.btn_procesar)

        # =========================
        # RESULTADO
        # =========================
        self.lbl_resultado = QLabel("Resultado: -")
        self.lbl_resultado.setObjectName("resultado")
        self.lbl_resultado.setWordWrap(True)

        layout_principal.addWidget(self.lbl_resultado)

        # =========================
        # HISTORIAL
        # =========================
        lbl_historial = QLabel("📚 Historial")
        lbl_historial.setObjectName("seccion")
        layout_principal.addWidget(lbl_historial)

        self.txt_historial = QTextEdit()
        self.txt_historial.setReadOnly(True)
        self.txt_historial.setPlaceholderText(
            "Aquí aparecerán tus operaciones..."
        )
        self.txt_historial.setMinimumHeight(130)

        layout_principal.addWidget(self.txt_historial)

        self.setLayout(layout_principal)

    # =========================
    # PROCESAR TEXTO
    # =========================
    def procesar(self):
        texto = self.input_texto.text().strip()
        opcion = self.combo_op.currentText()

        if not texto:
            self.lbl_resultado.setText(
                "⚠️ Resultado: Por favor, ingresa un texto."
            )
            return

        if opcion == "Contar Caracteres":
            if self.chk_espacios.isChecked():
                cant = len(texto)
            else:
                cant = len(texto.replace(" ", ""))

            res = f"Cantidad de caracteres: {cant}"

        elif opcion == "Contar Palabras":
            palabras = texto.split()
            res = f"Cantidad de palabras: {len(palabras)}"

        elif opcion == "Convertir a Mayúsculas":
            res = f"Texto: {texto.upper()}"

        elif opcion == "Invertir Texto":
            res = f"Texto invertido: {texto[::-1]}"

        else:
            res = "Operación no válida."

        self.lbl_resultado.setText(f"✅ Resultado: {res}")

        # Guardar en historial
        if self.radio_si.isChecked():
            self.txt_historial.append(
                f"<b style='color:#35E0A0;'>[{opcion}]</b><br>"
                f"<span style='color:#D1D5DB;'>"
                f"{texto} → {res}"
                f"</span><br><br>"
            )


# =========================
# EJECUTAR APLICACIÓN
# =========================
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = AnalizadorTextoPySide6()
    window.show()

    sys.exit(app.exec())

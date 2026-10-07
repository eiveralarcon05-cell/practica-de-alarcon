import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDialog,
    QFormLayout,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QRadioButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

# ==============================================================================
# ESTILOS QSS REDISEÑADOS
# ==============================================================================
ESTILO_GLOBAL = """
QMainWindow {
    background-color: #0f172a;
}

QWidget {
    color: #e2e8f0;
    font-family: 'Segoe UI', sans-serif;
    font-size: 13px;
}

/* Contenedores estilo Tarjeta */
QFrame#CardFrame {
    background-color: #1e293b;
    border-radius: 12px;
    border: 1px solid #334155;
}

QLabel#HeaderTitle {
    font-size: 24px;
    font-weight: bold;
    color: #38bdf8;
}

QLabel#HeaderSubtitle {
    font-size: 13px;
    color: #94a3b8;
}

/* Inputs y Selectores */
QLineEdit, QComboBox, QTextEdit, QListWidget {
    background-color: #0f172a;
    color: #f8fafc;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 8px;
}

QLineEdit:focus, QComboBox:focus, QTextEdit:focus {
    border: 1px solid #38bdf8;
}

QListWidget::item {
    padding: 8px;
    border-bottom: 1px solid #1e293b;
    border-radius: 4px;
}

QListWidget::item:selected {
    background-color: #0284c7;
    color: white;
}

/* Botones */
QPushButton {
    background-color: #2563eb;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 10px 14px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #1d4ed8;
}

QPushButton#BtnEliminar {
    background-color: #dc2626;
}

QPushButton#BtnEliminar:hover {
    background-color: #b91c1c;
}

QPushButton#BtnSecundario {
    background-color: #475569;
}

QPushButton#BtnSecundario:hover {
    background-color: #334155;
}

/* GroupBox */
QGroupBox {
    border: 1px solid #334155;
    border-radius: 8px;
    margin-top: 10px;
    font-weight: bold;
    color: #38bdf8;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
}
"""


# ==============================================================================
# DIÁLOGO DE FICHA TÉCNICA
# ==============================================================================
class FichaEstudianteDialog(QDialog):
    def __init__(self, datos, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Detalles de Expediente")
        self.resize(420, 360)
        self.setStyleSheet(ESTILO_GLOBAL)

        layout = QVBoxLayout()
        layout.setSpacing(15)

        card = QFrame()
        card.setObjectName("CardFrame")
        card_layout = QVBoxLayout(card)

        lbl_titulo = QLabel("📌 EXPEDIENTE ACADÉMICO")
        lbl_titulo.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: #38bdf8;"
        )

        detalles_html = f"""
        <p style='line-height: 1.6;'>
            <b>Estudiante:</b> {datos['nombre']}<br>
            <b>C.I. / DNI:</b> {datos['ci']}<br>
            <b>Nivel / Curso:</b> {datos['curso']}<br>
            <b>Jornada:</b> {datos['turno']}<br>
            <b>Intereses:</b> {datos['actividades'] or 'Sin registro'}<br><br>
            <b>Observaciones:</b><br>{datos['observaciones'] or 'N/A'}
        </p>
        """

        lbl_info = QLabel(detalles_html)
        lbl_info.setWordWrap(True)

        card_layout.addWidget(lbl_titulo)
        card_layout.addWidget(lbl_info)

        btn_cerrar = QPushButton("Cerrar Ficha")
        btn_cerrar.setObjectName("BtnSecundario")
        btn_cerrar.clicked.connect(self.accept)

        layout.addWidget(card)
        layout.addWidget(btn_cerrar)

        self.setLayout(layout)


# ==============================================================================
# VENTANA PRINCIPAL
# ==============================================================================
class GestionEstudiantesApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EduControl - Gestión Académica")
        self.resize(1000, 680)

        self.expedientes = []
        self.id_edicion = None

        self.init_ui()
        self.setStyleSheet(ESTILO_GLOBAL)

    def init_ui(self):
        widget_central = QWidget()
        self.setCentralWidget(widget_central)

        layout_principal = QVBoxLayout(widget_central)
        layout_principal.setContentsMargins(20, 20, 20, 20)
        layout_principal.setSpacing(15)

        # Encabezado
        layout_header = QHBoxLayout()
        lbl_titulo = QLabel("⚡ EduControl")
        lbl_titulo.setObjectName("HeaderTitle")

        lbl_subtitulo = QLabel("Panel de Administración de Estudiantes")
        lbl_subtitulo.setObjectName("HeaderSubtitle")

        layout_header.addWidget(lbl_titulo)
        layout_header.addStretch()
        layout_header.addWidget(lbl_subtitulo)

        layout_principal.addLayout(layout_header)

        # Panel Split (Izquierda - Formulario / Derecha - Lista)
        layout_contenido = QHBoxLayout()

        # ----------------------------------------------------------------------
        # IZQUIERDA: FORMULARIO
        # ----------------------------------------------------------------------
        frame_form = QFrame()
        frame_form.setObjectName("CardFrame")
        layout_form = QVBoxLayout(frame_form)

        form_datos = QFormLayout()

        self.txt_nombre = QLineEdit()
        self.txt_nombre.setPlaceholderText("Nombre y apellido")

        self.txt_ci = QLineEdit()
        self.txt_ci.setPlaceholderText("Número de documento")

        self.cmb_curso = QComboBox()
        self.cmb_curso.addItems(
            [
                "1º Secundaria",
                "2º Secundaria",
                "3º Secundaria",
                "4º Secundaria",
                "5º Secundaria",
                "6º Secundaria",
            ]
        )

        form_datos.addRow("Nombre:", self.txt_nombre)
        form_datos.addRow("C.I.:", self.txt_ci)
        form_datos.addRow("Curso:", self.cmb_curso)

        layout_form.addLayout(form_datos)

        # Seleccionar Turno
        box_turno = QGroupBox("Turno Académico")
        layout_turno = QHBoxLayout(box_turno)

        self.rad_manana = QRadioButton("Mañana")
        self.rad_tarde = QRadioButton("Tarde")
        self.rad_manana.setChecked(True)

        layout_turno.addWidget(self.rad_manana)
        layout_turno.addWidget(self.rad_tarde)

        layout_form.addWidget(box_turno)

        # Actividades Extra
        box_actividades = QGroupBox("Actividades / Intereses")
        grid_actividades = QGridLayout(box_actividades)

        self.chk_deporte = QCheckBox("Deporte")
        self.chk_musica = QCheckBox("Música")
        self.chk_ciencia = QCheckBox("Ciencia")
        self.chk_arte = QCheckBox("Arte")

        grid_actividades.addWidget(self.chk_deporte, 0, 0)
        grid_actividades.addWidget(self.chk_musica, 0, 1)
        grid_actividades.addWidget(self.chk_ciencia, 1, 0)
        grid_actividades.addWidget(self.chk_arte, 1, 1)

        layout_form.addWidget(box_actividades)

        # Observaciones
        layout_form.addWidget(QLabel("Observaciones:"))
        self.txt_obs = QTextEdit()
        self.txt_obs.setPlaceholderText("Notas o comentarios adicionales...")
        layout_form.addWidget(self.txt_obs)

        # Acciones/Botones
        layout_botones = QHBoxLayout()

        self.btn_guardar = QPushButton("Guardar")
        self.btn_editar = QPushButton("Editar")
        self.btn_editar.setObjectName("BtnSecundario")
        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_eliminar.setObjectName("BtnEliminar")
        self.btn_limpiar = QPushButton("Limpiar")
        self.btn_limpiar.setObjectName("BtnSecundario")

        layout_botones.addWidget(self.btn_guardar)
        layout_botones.addWidget(self.btn_editar)
        layout_botones.addWidget(self.btn_eliminar)
        layout_botones.addWidget(self.btn_limpiar)

        layout_form.addLayout(layout_botones)

        # ----------------------------------------------------------------------
        # DERECHA: REGISTROS Y BÚSQUEDA
        # ----------------------------------------------------------------------
        frame_lista = QFrame()
        frame_lista.setObjectName("CardFrame")
        layout_derecha = QVBoxLayout(frame_lista)

        layout_derecha.addWidget(QLabel("🔍 Búsqueda Rápida:"))

        self.txt_buscar = QLineEdit()
        self.txt_buscar.setPlaceholderText("Filtrar por nombre o CI...")
        layout_derecha.addWidget(self.txt_buscar)

        self.lst_estudiantes = QListWidget()
        layout_derecha.addWidget(self.lst_estudiantes)

        self.btn_ver_ficha = QPushButton("📄 Abrir Expediente")
        layout_derecha.addWidget(self.btn_ver_ficha)

        # Ensamblar Layout Principal
        layout_contenido.addWidget(frame_form, 3)
        layout_contenido.addWidget(frame_lista, 2)

        layout_principal.addLayout(layout_contenido)

        # Conexión de Eventos
        self.btn_guardar.clicked.connect(self.guardar_estudiante)
        self.btn_editar.clicked.connect(self.cargar_para_editar)
        self.btn_eliminar.clicked.connect(self.eliminar_estudiante)
        self.btn_limpiar.clicked.connect(self.limpiar_formulario)
        self.btn_ver_ficha.clicked.connect(self.abrir_ficha_completa)
        self.txt_buscar.textChanged.connect(self.refrescar_lista)

    # ==========================================================================
    # LÓGICA DE NEGOCIO Y EVENTOS
    # ==========================================================================
    def capturar_datos(self):
        intereses = []
        if self.chk_deporte.isChecked():
            intereses.append("Deporte")
        if self.chk_musica.isChecked():
            intereses.append("Música")
        if self.chk_ciencia.isChecked():
            intereses.append("Ciencia")
        if self.chk_arte.isChecked():
            intereses.append("Arte")

        return {
            "nombre": self.txt_nombre.text().strip(),
            "ci": self.txt_ci.text().strip(),
            "curso": self.cmb_curso.currentText(),
            "turno": (
                "Mañana" if self.rad_manana.isChecked() else "Tarde"
            ),
            "actividades": ", ".join(intereses),
            "observaciones": self.txt_obs.toPlainText().strip(),
        }

    def es_valido(self, datos):
        if len(datos["nombre"]) < 3:
            QMessageBox.warning(
                self,
                "Validación",
                "El nombre ingresado es muy corto (mín. 3 letras).",
            )
            return False

        if not datos["ci"].isdigit():
            QMessageBox.warning(
                self,
                "Validación",
                "El campo CI debe contener unicamente digitos numéricos.",
            )
            return False

        return True

    def guardar_estudiante(self):
        datos = self.capturar_datos()

        if not self.es_valido(datos):
            return

        if self.id_edicion is not None:
            self.expedientes[self.id_edicion] = datos
            self.id_edicion = None
            QMessageBox.information(
                self, "Éxito", "Expediente actualizado correctamente."
            )
        else:
            self.expedientes.append(datos)
            QMessageBox.information(
                self, "Éxito", "Estudiante registrado satisfactoriamente."
            )

        self.refrescar_lista()
        self.limpiar_formulario()

    def refrescar_lista(self):
        filtro = self.txt_buscar.text().lower()
        self.lst_estudiantes.clear()

        for idx, est in enumerate(self.expedientes):
            if (
                filtro in est["nombre"].lower()
                or filtro in est["ci"].lower()
            ):
                item = QListWidgetItem(
                    f"{est['nombre']} | CI: {est['ci']} ({est['curso']})"
                )
                item.setData(Qt.UserRole, idx)
                self.lst_estudiantes.addItem(item)

    def obtener_indice_seleccionado(self):
        item_actual = self.lst_estudiantes.currentItem()
        if item_actual:
            return item_actual.data(Qt.UserRole)
        return None

    def cargar_para_editar(self):
        idx = self.obtener_indice_seleccionado()

        if idx is None:
            QMessageBox.warning(
                self, "Atención", "Selecciona un estudiante de la lista."
            )
            return

        est = self.expedientes[idx]

        self.txt_nombre.setText(est["nombre"])
        self.txt_ci.setText(est["ci"])
        self.cmb_curso.setCurrentText(est["curso"])

        if est["turno"] == "Mañana":
            self.rad_manana.setChecked(True)
        else:
            self.rad_tarde.setChecked(True)

        self.chk_deporte.setChecked("Deporte" in est["actividades"])
        self.chk_musica.setChecked("Música" in est["actividades"])
        self.chk_ciencia.setChecked("Ciencia" in est["actividades"])
        self.chk_arte.setChecked("Arte" in est["actividades"])

        self.txt_obs.setPlainText(est["observaciones"])
        self.id_edicion = idx

    def eliminar_estudiante(self):
        idx = self.obtener_indice_seleccionado()

        if idx is None:
            QMessageBox.warning(
                self, "Atención", "Selecciona un estudiante a eliminar."
            )
            return

        confirmacion = QMessageBox.question(
            self,
            "Confirmar eliminación",
            "¿Estás seguro de remover este registro?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if confirmacion == QMessageBox.Yes:
            self.expedientes.pop(idx)
            self.refrescar_lista()
            self.limpiar_formulario()

    def limpiar_formulario(self):
        self.txt_nombre.clear()
        self.txt_ci.clear()
        self.txt_obs.clear()

        self.cmb_curso.setCurrentIndex(0)
        self.rad_manana.setChecked(True)

        self.chk_deporte.setChecked(False)
        self.chk_musica.setChecked(False)
        self.chk_ciencia.setChecked(False)
        self.chk_arte.setChecked(False)

        self.id_edicion = None

    def abrir_ficha_completa(self):
        idx = self.obtener_indice_seleccionado()

        if idx is None:
            QMessageBox.warning(
                self, "Atención", "Selecciona un estudiante para consultar."
            )
            return

        dialogo = FichaEstudianteDialog(self.expedientes[idx], self)
        dialogo.exec()


# ==============================================================================
# PUNTO DE ENTRADA
# ==============================================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = GestionEstudiantesApp()
    ventana.show()
    sys.exit(app.exec())
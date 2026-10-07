import tkinter as tk
from tkinter import messagebox, ttk


class SistemaProductos:

    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Nexo Market - Registro de Productos")
        self.ventana.geometry("1150x730")
        self.ventana.configure(bg="#0f172a")  # Fondo oscuro elegante tipo SaaS

        self.productos = []
        self.indice_edicion = None

        self.crear_interfaz()

    # =================================================
    # INTERFAZ LLAMATIVA Y MODERNA
    # =================================================

    def crear_interfaz(self):
        # Contenedor principal
        contenedor_principal = tk.Frame(self.ventana, bg="#0f172a")
        contenedor_principal.pack(fill="both", expand=True, padx=20, pady=20)

        # ---------------------------------
        # ENCABEZADO
        # ---------------------------------
        header_frame = tk.Frame(contenedor_principal, bg="#0f172a")
        header_frame.pack(fill="x", pady=(0, 15))

        tk.Label(
            header_frame,
            text="🛍️ NEXO MARKET",
            font=("Segoe UI", 24, "bold"),
            bg="#0f172a",
            fg="#38bdf8",  # Azul brillante llamativo
        ).pack(anchor="w")

        tk.Label(
            header_frame,
            text="Sistema inteligente de gestión e inventario de productos",
            font=("Segoe UI", 11),
            bg="#0f172a",
            fg="#94a3b8",
        ).pack(anchor="w")

        # ---------------------------------
        # CONTENEDOR DE PANELES (GRID)
        # ---------------------------------
        cuerpo = tk.Frame(contenedor_principal, bg="#0f172a")
        cuerpo.pack(fill="both", expand=True)

        cuerpo.grid_columnconfigure(0, weight=4)  # Formulario
        cuerpo.grid_columnconfigure(1, weight=6)  # Inventario / Tabla
        cuerpo.grid_rowconfigure(0, weight=1)

        # =================================================
        # PANEL IZQUIERDO: FORMULARIO
        # =================================================
        panel_izquierdo = tk.Frame(cuerpo, bg="#1e293b", bd=0)
        panel_izquierdo.grid(row=0, column=0, sticky="nsew", padx=(0, 12))

        canvas_izq = tk.Canvas(
            panel_izquierdo, bg="#1e293b", bd=0, highlightthickness=0
        )
        scrollbar_izq = ttk.Scrollbar(
            panel_izquierdo, orient="vertical", command=canvas_izq.yview
        )
        self.scroll_frame_izq = tk.Frame(canvas_izq, bg="#1e293b")

        self.scroll_frame_izq.bind(
            "<Configure>",
            lambda e: canvas_izq.configure(
                scrollregion=canvas_izq.bbox("all")
            ),
        )

        # Corrección de ancho adaptativo dentro del Canvas
        window_id = canvas_izq.create_window(
            (0, 0), window=self.scroll_frame_izq, anchor="nw"
        )
        canvas_izq.bind(
            "<Configure>",
            lambda e: canvas_izq.itemconfig(window_id, width=e.width),
        )

        canvas_izq.configure(yscrollcommand=scrollbar_izq.set)

        # Soporte para rueda del ratón
        def _on_mousewheel(event):
            canvas_izq.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas_izq.bind_all("<MouseWheel>", _on_mousewheel)

        canvas_izq.pack(side="left", fill="both", expand=True, padx=15, pady=15)
        scrollbar_izq.pack(side="right", fill="y")

        # Título del panel
        tk.Label(
            self.scroll_frame_izq,
            text="📦 Datos del Producto",
            font=("Segoe UI", 14, "bold"),
            bg="#1e293b",
            fg="#f8fafc",
        ).pack(anchor="w", pady=(5, 15))

        formulario = tk.Frame(self.scroll_frame_izq, bg="#1e293b")
        formulario.pack(fill="x", expand=True)

        def crear_campo(parent, texto_label, row):
            tk.Label(
                parent,
                text=texto_label,
                font=("Segoe UI", 10, "bold"),
                bg="#1e293b",
                fg="#cbd5e1",
            ).grid(row=row, column=0, sticky="w", pady=6)
            entry = tk.Entry(
                parent,
                font=("Segoe UI", 10),
                bg="#334155",
                fg="white",
                insertbackground="white",
                relief="flat",
            )
            entry.grid(
                row=row, column=1, sticky="ew", padx=(10, 0), pady=6, ipady=4
            )
            parent.grid_columnconfigure(1, weight=1)
            return entry

        self.nombre = crear_campo(formulario, "Nombre:", 0)
        self.sku = crear_campo(formulario, "Código SKU:", 1)
        self.precio = crear_campo(formulario, "Precio (Bs.):", 2)

        # Categoría
        tk.Label(
            formulario,
            text="Categoría:",
            font=("Segoe UI", 10, "bold"),
            bg="#1e293b",
            fg="#cbd5e1",
        ).grid(row=3, column=0, sticky="w", pady=6)
        self.categoria = ttk.Combobox(
            formulario,
            values=["Electrónica", "Hogar", "Ropa", "Alimentos", "Deportes"],
            state="readonly",
            font=("Segoe UI", 10),
        )
        self.categoria.grid(row=3, column=1, sticky="ew", padx=(10, 0), pady=6)
        self.categoria.current(0)

        # Estado (Radiobuttons)
        tk.Label(
            self.scroll_frame_izq,
            text="Estado del producto",
            font=("Segoe UI", 11, "bold"),
            bg="#1e293b",
            fg="#f8fafc",
        ).pack(anchor="w", pady=(15, 5))

        self.estado = tk.StringVar(value="Disponible")
        estados_frame = tk.Frame(self.scroll_frame_izq, bg="#1e293b")
        estados_frame.pack(anchor="w", pady=5)

        for est in ["Disponible", "Agotado", "En reserva"]:
            tk.Radiobutton(
                estados_frame,
                text=est,
                variable=self.estado,
                value=est,
                bg="#1e293b",
                fg="#e2e8f0",
                font=("Segoe UI", 9),
                selectcolor="#334155",
                activebackground="#1e293b",
                activeforeground="white",
            ).pack(side="left", padx=(0, 12))

        # Características (Checkbuttons)
        tk.Label(
            self.scroll_frame_izq,
            text="Características",
            font=("Segoe UI", 11, "bold"),
            bg="#1e293b",
            fg="#f8fafc",
        ).pack(anchor="w", pady=(15, 5))

        carac_frame = tk.Frame(self.scroll_frame_izq, bg="#1e293b")
        carac_frame.pack(anchor="w", pady=5)

        self.nuevo = tk.BooleanVar()
        self.oferta = tk.BooleanVar()
        self.destacado = tk.BooleanVar()
        self.envio = tk.BooleanVar()

        checks = [
            ("🆕 Nuevo", self.nuevo, 0, 0),
            ("🔥 Oferta", self.oferta, 0, 1),
            ("⭐ Destacado", self.destacado, 1, 0),
            ("🚚 Envío gratis", self.envio, 1, 1),
        ]
        for texto, var, r, c in checks:
            tk.Checkbutton(
                carac_frame,
                text=texto,
                variable=var,
                bg="#1e293b",
                fg="#e2e8f0",
                font=("Segoe UI", 9),
                selectcolor="#334155",
                activebackground="#1e293b",
                activeforeground="white",
            ).grid(row=r, column=c, sticky="w", padx=(0, 15), pady=3)

        # Descripción
        tk.Label(
            self.scroll_frame_izq,
            text="Descripción:",
            font=("Segoe UI", 11, "bold"),
            bg="#1e293b",
            fg="#f8fafc",
        ).pack(anchor="w", pady=(15, 5))

        self.descripcion = tk.Text(
            self.scroll_frame_izq,
            height=4,
            font=("Segoe UI", 10),
            fg="white",
            bg="#334155",
            insertbackground="white",
            relief="flat",
        )
        self.descripcion.pack(fill="x", pady=5)

        # Botones de Acción
        botones_frame = tk.Frame(self.scroll_frame_izq, bg="#1e293b")
        botones_frame.pack(fill="x", pady=(20, 10))

        def crear_boton(parent, texto, comando, color_bg):
            return tk.Button(
                parent,
                text=texto,
                command=comando,
                bg=color_bg,
                fg="white",
                font=("Segoe UI", 9, "bold"),
                relief="flat",
                padx=8,
                pady=8,
                cursor="hand2",
            )

        self.btn_registrar = crear_boton(
            botones_frame, "💾 Guardar", self.registrar, "#10b981"
        )
        self.btn_registrar.pack(side="left", expand=True, fill="x", padx=2)

        crear_boton(
            botones_frame, "✏ Cargar Edit.", self.cargar_para_editar, "#3b82f6"
        ).pack(side="left", expand=True, fill="x", padx=2)
        crear_boton(
            botones_frame, "🗑 Eliminar", self.eliminar, "#ef4444"
        ).pack(side="left", expand=True, fill="x", padx=2)
        crear_boton(
            botones_frame, "🧹 Limpiar", self.limpiar, "#64748b"
        ).pack(side="left", expand=True, fill="x", padx=2)

    # =================================================
    # PANEL DERECHO: INVENTARIO Y TABLA
    # =================================================
        panel_derecho = tk.Frame(cuerpo, bg="#1e293b", bd=0)
        panel_derecho.grid(row=0, column=1, sticky="nsew")

        header_der = tk.Frame(panel_derecho, bg="#1e293b")
        header_der.pack(fill="x", padx=20, pady=20)

        tk.Label(
            header_der,
            text="🔎 Inventario Actual",
            font=("Segoe UI", 14, "bold"),
            bg="#1e293b",
            fg="#f8fafc",
        ).pack(anchor="w", pady=(0, 10))

        self.buscar = tk.Entry(
            header_der,
            font=("Segoe UI", 11),
            fg="white",
            bg="#334155",
            insertbackground="white",
            relief="flat",
        )
        self.buscar.pack(fill="x", ipady=5)
        self.buscar.insert(0, "🔍 Buscar por nombre o SKU...")
        self.buscar.bind(
            "<FocusIn>",
            lambda e: self.buscar.delete(0, tk.END)
            if self.buscar.get() == "🔍 Buscar por nombre o SKU..."
            else None,
        )
        self.buscar.bind(
            "<KeyRelease>", lambda evento: self.mostrar_productos()
        )

        # Configuración de la Tabla
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background="#334155",
            foreground="white",
            rowheight=32,
            fieldbackground="#334155",
            font=("Segoe UI", 10),
        )
        style.configure(
            "Treeview.Heading",
            background="#0ea5e9",
            foreground="white",
            font=("Segoe UI", 10, "bold"),
        )
        style.map("Treeview", background=[("selected", "#0284c7")])

        tabla_frame = tk.Frame(panel_derecho, bg="#1e293b")
        tabla_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columnas = ("nombre", "sku", "precio", "categoria", "estado")
        self.tabla = ttk.Treeview(
            tabla_frame, columns=columnas, show="headings", selectmode="browse"
        )

        self.tabla.heading("nombre", text="Producto")
        self.tabla.heading("sku", text="SKU")
        self.tabla.heading("precio", text="Precio")
        self.tabla.heading("categoria", text="Categoría")
        self.tabla.heading("estado", text="Estado")

        self.tabla.column("nombre", width=140, anchor="w")
        self.tabla.column("sku", width=90, anchor="center")
        self.tabla.column("precio", width=90, anchor="e")
        self.tabla.column("categoria", width=100, anchor="center")
        self.tabla.column("estado", width=100, anchor="center")

        scrollbar_tabla = ttk.Scrollbar(
            tabla_frame, orient="vertical", command=self.tabla.yview
        )
        self.tabla.configure(yscrollcommand=scrollbar_tabla.set)

        self.tabla.pack(side="left", fill="both", expand=True)
        scrollbar_tabla.pack(side="right", fill="y")

        self.tabla.bind("<Double-1>", lambda evento: self.cargar_para_editar())

        tk.Button(
            panel_derecho,
            text="👁 Ver información detallada",
            command=self.ver_producto,
            bg="#8b5cf6",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            pady=10,
            cursor="hand2",
        ).pack(fill="x", padx=20, pady=20)

    # =================================================
    # LÓGICA
    # =================================================

    def registrar(self):
        nombre = self.nombre.get().strip()
        sku = self.sku.get().strip()
        precio_texto = self.precio.get().strip()

        if nombre == "":
            messagebox.showwarning("Validación", "Escribe el nombre del producto.")
            return

        if sku == "":
            messagebox.showwarning("Validación", "Escribe el código SKU.")
            return

        try:
            precio = float(precio_texto.replace(",", "."))
            if precio < 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning(
                "Validación", "El precio debe ser un número válido mayor a 0."
            )
            return

        for i, producto in enumerate(self.productos):
            if (
                producto["sku"].lower() == sku.lower()
                and i != self.indice_edicion
            ):
                messagebox.showwarning(
                    "SKU repetido", "Ya existe un producto con ese SKU."
                )
                return

        caracteristicas = []
        if self.nuevo.get():
            caracteristicas.append("Nuevo")
        if self.oferta.get():
            caracteristicas.append("Oferta")
        if self.destacado.get():
            caracteristicas.append("Destacado")
        if self.envio.get():
            caracteristicas.append("Envío gratis")

        producto = {
            "nombre": nombre,
            "sku": sku,
            "precio": precio,
            "categoria": self.categoria.get(),
            "estado": self.estado.get(),
            "caracteristicas": ", ".join(caracteristicas),
            "descripcion": self.descripcion.get("1.0", tk.END).strip(),
        }

        if self.indice_edicion is not None:
            self.productos[self.indice_edicion] = producto
            messagebox.showinfo(
                "Actualizado", "Producto actualizado correctamente."
            )
        else:
            self.productos.append(producto)
            messagebox.showinfo(
                "Registrado", "Producto registrado correctamente."
            )

        self.mostrar_productos()
        self.limpiar()

    def mostrar_productos(self):
        for elemento in self.tabla.get_children():
            self.tabla.delete(elemento)

        texto = self.buscar.get().lower()
        if "buscar por nombre" in texto:
            texto = ""

        for indice, producto in enumerate(self.productos):
            if (
                texto in producto["nombre"].lower()
                or texto in producto["sku"].lower()
            ):
                self.tabla.insert(
                    "",
                    tk.END,
                    iid=str(indice),
                    values=(
                        producto["nombre"],
                        producto["sku"],
                        f"Bs. {producto['precio']:.2f}",
                        producto["categoria"],
                        producto["estado"],
                    ),
                )

    def obtener_indice(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            return None
        return int(seleccion[0])

    def cargar_para_editar(self):
        indice = self.obtener_indice()
        if indice is None:
            messagebox.showinfo(
                "Aviso", "Selecciona un producto de la tabla para editar."
            )
            return

        producto = self.productos[indice]

        self.nombre.delete(0, tk.END)
        self.nombre.insert(0, producto["nombre"])

        self.sku.delete(0, tk.END)
        self.sku.insert(0, producto["sku"])

        self.precio.delete(0, tk.END)
        self.precio.insert(0, str(producto["precio"]))

        self.categoria.set(producto["categoria"])
        self.estado.set(producto["estado"])

        self.nuevo.set("Nuevo" in producto["caracteristicas"])
        self.oferta.set("Oferta" in producto["caracteristicas"])
        self.destacado.set("Destacado" in producto["caracteristicas"])
        self.envio.set("Envío gratis" in producto["caracteristicas"])

        self.descripcion.delete("1.0", tk.END)
        self.descripcion.insert("1.0", producto["descripcion"])

        self.indice_edicion = indice
        self.btn_registrar.config(text="💾 Actualizar", bg="#0284c7")

    def eliminar(self):
        indice = self.obtener_indice()
        if indice is None:
            messagebox.showinfo("Aviso", "Selecciona un producto.")
            return

        respuesta = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Seguro que deseas eliminar este producto?",
        )
        if respuesta:
            self.productos.pop(indice)
            self.mostrar_productos()
            self.limpiar()

    def ver_producto(self):
        indice = self.obtener_indice()
        if indice is None:
            messagebox.showinfo("Aviso", "Selecciona un producto.")
            return

        producto = self.productos[indice]

        informacion = (
            f"PRODUCTO\n\n"
            f"Nombre: {producto['nombre']}\n"
            f"SKU: {producto['sku']}\n"
            f"Precio: Bs. {producto['precio']:.2f}\n"
            f"Categoría: {producto['categoria']}\n"
            f"Estado: {producto['estado']}\n"
            f"Características: {producto['caracteristicas'] or 'Ninguna'}\n\n"
            f"Descripción:\n{producto['descripcion'] or 'Sin descripción'}"
        )

        messagebox.showinfo("Información del producto", informacion)

    def limpiar(self):
        self.nombre.delete(0, tk.END)
        self.sku.delete(0, tk.END)
        self.precio.delete(0, tk.END)
        self.categoria.current(0)
        self.estado.set("Disponible")
        self.nuevo.set(False)
        self.oferta.set(False)
        self.destacado.set(False)
        self.envio.set(False)
        self.descripcion.delete("1.0", tk.END)
        self.indice_edicion = None
        self.btn_registrar.config(text="💾 Guardar", bg="#10b981")


if __name__ == "__main__":
    ventana = tk.Tk()
    app = SistemaProductos(ventana)
    ventana.mainloop()
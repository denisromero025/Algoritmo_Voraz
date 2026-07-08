import tkinter as tk
from tkinter import ttk, messagebox

from modelos import Solicitud
from flota import cargar_flota, TIPOS_VEHICULO
from algoritmo_voraz import asignar_solicitudes_voraz

from validaciones import (
    validar_nombre,
    validar_dias,
    validar_presupuesto
)


class AplicacionAlquiler:

    # ==========================
    # PALETA DE COLORES
    # ==========================
    COLOR_FONDO = "#EEF2F7"
    COLOR_FONDO_TARJETA = "#FFFFFF"
    COLOR_HEADER = "#1F4E79"
    COLOR_HEADER_TEXTO = "#FFFFFF"
    COLOR_ACENTO = "#2E86C1"
    COLOR_EXITO = "#1E8449"
    COLOR_PELIGRO = "#C0392B"
    COLOR_ADVERTENCIA = "#B9770E"
    COLOR_TEXTO = "#1C2833"
    COLOR_BORDE = "#D5DBDB"
    COLOR_FILA_PAR = "#F4F8FB"
    COLOR_FILA_IMPAR = "#FFFFFF"

    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Alquiler de Vehículos ")
        self.root.geometry("1500x800")
        self.root.configure(bg=self.COLOR_FONDO)

        # ==========================
        # DATOS
        # ==========================
        self.vehiculos = cargar_flota()
        self.solicitudes = []
        self.tiempo = 0
        self.ingreso_total = 0
        self.total_devuelto = 0
        self.conflictos_resueltos = 0
        self.ingreso_perdido = 0

        # ==========================
        # ESTILOS
        # ==========================
        self.configurar_estilos()

        # ==========================
        # INTERFAZ
        # ==========================
        self.crear_interfaz()

    # =====================================================
    # ESTILOS TTK
    # =====================================================

    def configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Notebook (pestañas)
        style.configure(
            "TNotebook",
            background=self.COLOR_FONDO,
            borderwidth=0
        )
        style.configure(
            "TNotebook.Tab",
            font=("Segoe UI", 11, "bold"),
            padding=(20, 10),
            background="#D6E4F0",
            foreground=self.COLOR_TEXTO
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", self.COLOR_ACENTO)],
            foreground=[("selected", "#FFFFFF")]
        )

        # Botones
        style.configure(
            "Primario.TButton",
            font=("Segoe UI", 10, "bold"),
            foreground="#FFFFFF",
            background=self.COLOR_ACENTO,
            padding=8,
            borderwidth=0
        )
        style.map(
            "Primario.TButton",
            background=[("active", "#1B4F72")]
        )

        style.configure(
            "Exito.TButton",
            font=("Segoe UI", 10, "bold"),
            foreground="#FFFFFF",
            background=self.COLOR_EXITO,
            padding=8,
            borderwidth=0
        )
        style.map(
            "Exito.TButton",
            background=[("active", "#145A32")]
        )

        style.configure(
            "Peligro.TButton",
            font=("Segoe UI", 10, "bold"),
            foreground="#FFFFFF",
            background=self.COLOR_PELIGRO,
            padding=8,
            borderwidth=0
        )
        style.map(
            "Peligro.TButton",
            background=[("active", "#922B21")]
        )

        # Treeview
        style.configure(
            "Treeview",
            font=("Segoe UI", 10),
            rowheight=28,
            background=self.COLOR_FONDO_TARJETA,
            fieldbackground=self.COLOR_FONDO_TARJETA,
            foreground=self.COLOR_TEXTO,
            borderwidth=0
        )
        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold"),
            background=self.COLOR_HEADER,
            foreground="#FFFFFF",
            padding=6
        )
        style.map(
            "Treeview.Heading",
            background=[("active", self.COLOR_ACENTO)]
        )
        style.map(
            "Treeview",
            background=[("selected", self.COLOR_ACENTO)],
            foreground=[("selected", "#FFFFFF")]
        )

        # Combobox y Entry
        style.configure(
            "TEntry",
            padding=6
        )
        style.configure(
            "TCombobox",
            padding=6
        )

    # =====================================================
    # ESTRUCTURA PRINCIPAL
    # =====================================================

    def crear_interfaz(self):
        self.crear_header()

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=18, pady=(0, 15))

        self.tab_flota = tk.Frame(self.notebook, bg=self.COLOR_FONDO)
        self.tab_solicitudes = tk.Frame(self.notebook, bg=self.COLOR_FONDO)
        self.tab_procesos = tk.Frame(self.notebook, bg=self.COLOR_FONDO)

        self.notebook.add(self.tab_flota, text="🚗  Flota de Vehículos")
        self.notebook.add(self.tab_solicitudes, text="📋  Solicitudes")
        self.notebook.add(self.tab_procesos, text="📊  Procesos y Resultados")

        self.crear_tab_flota()
        self.crear_tab_solicitudes()
        self.crear_tab_procesos()

    def crear_header(self):
        header = tk.Frame(self.root, bg=self.COLOR_HEADER, height=90)
        header.pack(fill="x")

        tk.Label(
            header,
            text="SISTEMA DE ALQUILER DE VEHÍCULOS",
            font=("Segoe UI", 20, "bold"),
            fg=self.COLOR_HEADER_TEXTO,
            bg=self.COLOR_HEADER
        ).pack(pady=(14, 0))

    def crear_tarjeta(self, parent, titulo):
        """Crea un contenedor tipo 'tarjeta' con borde suave y título coloreado."""
        contenedor = tk.Frame(
            parent, bg=self.COLOR_FONDO_TARJETA,
            highlightbackground=self.COLOR_BORDE, highlightthickness=1
        )
        contenedor.pack(fill="both", expand=True, padx=18, pady=10)

        titulo_lbl = tk.Label(
            contenedor, text=titulo,
            font=("Segoe UI", 12, "bold"),
            fg=self.COLOR_HEADER, bg=self.COLOR_FONDO_TARJETA,
            anchor="w"
        )
        titulo_lbl.pack(fill="x", padx=15, pady=(12, 5))

        cuerpo = tk.Frame(contenedor, bg=self.COLOR_FONDO_TARJETA)
        cuerpo.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        return cuerpo

    # =====================================================
    # PESTAÑA 1: FLOTA DE VEHÍCULOS
    # =====================================================

    def crear_tab_flota(self):
        cuerpo = self.crear_tarjeta(self.tab_flota, "Flota Registrada")

        columnas = ("id", "placa", "tipo", "modelo", "tarifa", "estado")
        self.tree_flota = ttk.Treeview(
            cuerpo, columns=columnas, show="headings", height=18
        )

        encabezados = {
            "id": "ID", "placa": "Placa", "tipo": "Tipo",
            "modelo": "Modelo", "tarifa": "Tarifa/Día", "estado": "Estado"
        }
        anchos = {
            "id": 50, "placa": 110, "tipo": 120,
            "modelo": 220, "tarifa": 110, "estado": 130
        }

        for col in columnas:
            self.tree_flota.heading(col, text=encabezados[col])
            self.tree_flota.column(col, width=anchos[col], anchor="center")

        self.tree_flota.tag_configure("par", background=self.COLOR_FILA_PAR)
        self.tree_flota.tag_configure("impar", background=self.COLOR_FILA_IMPAR)
        self.tree_flota.tag_configure("disponible", foreground=self.COLOR_EXITO)
        self.tree_flota.tag_configure("ocupado", foreground=self.COLOR_PELIGRO)

        scrollbar = ttk.Scrollbar(
            cuerpo, orient="vertical", command=self.tree_flota.yview
        )
        self.tree_flota.configure(yscrollcommand=scrollbar.set)
        self.tree_flota.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.refrescar_flota()

    def refrescar_flota(self):
        self.tree_flota.delete(*self.tree_flota.get_children())
        for i, v in enumerate(self.vehiculos):
            estado = "Disponible" if v.disponible else "Ocupado"
            fila_tag = "par" if i % 2 == 0 else "impar"
            estado_tag = "disponible" if v.disponible else "ocupado"
            self.tree_flota.insert(
                "", tk.END,
                values=(v.id, v.placa, v.tipo, v.modelo,
                        f"S/ {v.tarifa:.2f}", estado),
                tags=(fila_tag, estado_tag)
            )

    # =====================================================
    # PESTAÑA 2: SOLICITUDES
    # =====================================================

    def crear_tab_solicitudes(self):
        self.crear_formulario(self.tab_solicitudes)
        self.crear_tabla_solicitudes(self.tab_solicitudes)

    def crear_formulario(self, parent):
        cuerpo = self.crear_tarjeta(parent, "Registro de Solicitudes")

        fila = tk.Frame(cuerpo, bg=self.COLOR_FONDO_TARJETA)
        fila.pack(fill="x", pady=5)

        tk.Label(
            fila, text="Cliente:", bg=self.COLOR_FONDO_TARJETA,
            font=("Segoe UI", 10, "bold"), fg=self.COLOR_TEXTO
        ).grid(row=0, column=0, sticky="w", padx=(0, 6))
        self.entry_cliente = ttk.Entry(fila, width=20)
        self.entry_cliente.grid(row=0, column=1, padx=(0, 20))

        tk.Label(
            fila, text="Tipo:", bg=self.COLOR_FONDO_TARJETA,
            font=("Segoe UI", 10, "bold"), fg=self.COLOR_TEXTO
        ).grid(row=0, column=2, sticky="w", padx=(0, 6))
        self.combo_tipo = ttk.Combobox(
            fila, values=TIPOS_VEHICULO, state="readonly", width=14
        )
        self.combo_tipo.grid(row=0, column=3, padx=(0, 20))

        tk.Label(
            fila, text="Días:", bg=self.COLOR_FONDO_TARJETA,
            font=("Segoe UI", 10, "bold"), fg=self.COLOR_TEXTO
        ).grid(row=0, column=4, sticky="w", padx=(0, 6))
        self.entry_dias = ttk.Entry(fila, width=8)
        self.entry_dias.grid(row=0, column=5, padx=(0, 20))

        tk.Label(
            fila, text="Presupuesto/día (S/):", bg=self.COLOR_FONDO_TARJETA,
            font=("Segoe UI", 10, "bold"), fg=self.COLOR_TEXTO
        ).grid(row=0, column=6, sticky="w", padx=(0, 6))
        self.entry_presupuesto = ttk.Entry(fila, width=12)
        self.entry_presupuesto.grid(row=0, column=7, padx=(0, 20))

        botones = tk.Frame(cuerpo, bg=self.COLOR_FONDO_TARJETA)
        botones.pack(fill="x", pady=(15, 0))

        ttk.Button(
            botones, text="Registrar Solicitud", style="Primario.TButton",
            command=self.registrar_solicitud
        ).pack(side="left", padx=(0, 10))

        ttk.Button(
            botones, text="Procesar Solicitudes", style="Exito.TButton",
            command=self.ir_a_procesos
        ).pack(side="left", padx=(0, 10))

        ttk.Button(
            botones, text="Reiniciar", style="Peligro.TButton",
            command=self.reiniciar
        ).pack(side="left")

    def crear_tabla_solicitudes(self, parent):
        cuerpo = self.crear_tarjeta(parent, "Solicitudes Registradas")

        columnas = ("id", "cliente", "tipo", "dias", "presupuesto", "estado")
        self.tree_solicitudes = ttk.Treeview(
            cuerpo, columns=columnas, show="headings", height=14
        )

        encabezados = {
            "id": "ID", "cliente": "Cliente", "tipo": "Tipo",
            "dias": "Días", "presupuesto": "Presupuesto/Día", "estado": "Estado"
        }
        anchos = {
            "id": 60, "cliente": 220, "tipo": 130,
            "dias": 70, "presupuesto": 140, "estado": 150
        }

        for col in columnas:
            self.tree_solicitudes.heading(col, text=encabezados[col])
            self.tree_solicitudes.column(col, width=anchos[col], anchor="center")

        self.tree_solicitudes.tag_configure("par", background=self.COLOR_FILA_PAR)
        self.tree_solicitudes.tag_configure("impar", background=self.COLOR_FILA_IMPAR)
        self.tree_solicitudes.tag_configure("atendida", foreground=self.COLOR_EXITO)
        self.tree_solicitudes.tag_configure("no_atendida", foreground=self.COLOR_PELIGRO)
        self.tree_solicitudes.tag_configure("pendiente", foreground=self.COLOR_ADVERTENCIA)

        scrollbar = ttk.Scrollbar(
            cuerpo, orient="vertical", command=self.tree_solicitudes.yview
        )
        self.tree_solicitudes.configure(yscrollcommand=scrollbar.set)
        self.tree_solicitudes.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    # =====================================================
    # REGISTRAR SOLICITUD (con validación previa de viabilidad)
    # =====================================================

    def registrar_solicitud(self):
        cliente = self.entry_cliente.get().strip()
        tipo = self.combo_tipo.get().strip()
        dias = self.entry_dias.get().strip()
        presupuesto = self.entry_presupuesto.get().strip()

        valido, mensaje = validar_nombre(cliente)
        if not valido:
            messagebox.showwarning("Dato inválido", mensaje)
            return

        if tipo == "":
            messagebox.showwarning("Dato inválido", "Seleccione un tipo de vehículo.")
            return

        valido, mensaje = validar_dias(dias)
        if not valido:
            messagebox.showwarning("Dato inválido", mensaje)
            return

        valido, mensaje = validar_presupuesto(presupuesto)
        if not valido:
            messagebox.showwarning("Dato inválido", mensaje)
            return

        presupuesto_num = float(presupuesto)

        vehiculos_del_tipo = [
            v for v in self.vehiculos if v.tipo == tipo
        ]

        if not vehiculos_del_tipo:
            messagebox.showerror(
                "Registro no permitido",
                f"No contamos con unidades de tipo '{tipo}' en la flota.\n"
                f"Por favor selecciona otra categoría de vehículo."
            )
            return

        disponibles_del_tipo = [
            v for v in vehiculos_del_tipo if v.disponible
        ]

        if not disponibles_del_tipo:
            messagebox.showerror(
                "Registro no permitido",
                f"En este momento no hay unidades disponibles de tipo '{tipo}'.\n"
                f"Todas están ocupadas. Intenta más tarde o elige otra categoría."
            )
            return

        candidatos_validos = [
            v for v in disponibles_del_tipo if v.tarifa <= presupuesto_num
        ]

        if not candidatos_validos:
            tarifa_minima = min(v.tarifa for v in disponibles_del_tipo)
            messagebox.showerror(
                "Registro no permitido",
                f"Tu presupuesto de S/ {presupuesto_num:.2f}/día no alcanza para "
                f"la categoría '{tipo}'.\nEl vehículo más económico disponible "
                f"cuesta S/ {tarifa_minima:.2f}/día.\n\n"
                f"Ajusta tu presupuesto e inténtalo nuevamente."
            )
            return

        solicitud = Solicitud(cliente, tipo, int(dias), presupuesto_num)
        self.solicitudes.append(solicitud)

        self.entry_cliente.delete(0, tk.END)
        self.combo_tipo.set("")
        self.entry_dias.delete(0, tk.END)
        self.entry_presupuesto.delete(0, tk.END)

        self.refrescar_solicitudes()
        self.actualizar_estadisticas()

        messagebox.showinfo("Registro", "Solicitud registrada correctamente.")

    def refrescar_solicitudes(self):
        self.tree_solicitudes.delete(*self.tree_solicitudes.get_children())
        for i, s in enumerate(self.solicitudes):
            fila_tag = "par" if i % 2 == 0 else "impar"
            if s.estado == "Atendida":
                estado_tag = "atendida"
            elif s.estado == "No atendida":
                estado_tag = "no_atendida"
            else:
                estado_tag = "pendiente"

            self.tree_solicitudes.insert(
                "", tk.END,
                values=(
                    s.id_solicitud, s.cliente, s.tipo_solicitado, s.dias,
                    f"S/ {s.presupuesto_diario:.2f}", s.estado
                ),
                tags=(fila_tag, estado_tag)
            )

    # =====================================================
    # NAVEGACIÓN A LA PESTAÑA DE PROCESOS
    # =====================================================

    def ir_a_procesos(self):
        if len(self.solicitudes) == 0:
            messagebox.showwarning(
                "Aviso",
                "No existen solicitudes registradas para procesar."
            )
            return

        self.notebook.select(self.tab_procesos)
        self.procesar()

    # =====================================================
    # PESTAÑA 3: PROCESOS Y RESULTADOS
    # =====================================================

    def crear_tab_procesos(self):
        top_frame = tk.Frame(self.tab_procesos, bg=self.COLOR_FONDO)
        top_frame.pack(fill="x", padx=18, pady=(10, 0))

        ttk.Button(
            top_frame, text="⚙️  Realizar asignaciones ", style="Primario.TButton",
            command=self.procesar
        ).pack(side="left")

        self.crear_tabla_asignaciones(self.tab_procesos)
        self.crear_panel_estadisticas(self.tab_procesos)

    def crear_tabla_asignaciones(self, parent):
        cuerpo = self.crear_tarjeta(parent, "Asignaciones Realizadas")

        columnas = ("cliente", "vehiculo", "tarifa", "dias", "total", "diferencia")
        self.tree_asignaciones = ttk.Treeview(
            cuerpo, columns=columnas, show="headings", height=9
        )

        encabezados = {
            "cliente": "Cliente", "vehiculo": "Vehículo",
            "tarifa": "Tarifa/Día", "dias": "Días",
            "total": "Costo Total", "diferencia": "Diferencia devuelta (S/)"
        }
        anchos = {
            "cliente": 160, "vehiculo": 240, "tarifa": 100,
            "dias": 60, "total": 120, "diferencia": 180
        }

        for col in columnas:
            self.tree_asignaciones.heading(col, text=encabezados[col])
            self.tree_asignaciones.column(col, width=anchos[col], anchor="center")

        self.tree_asignaciones.tag_configure("par", background=self.COLOR_FILA_PAR)
        self.tree_asignaciones.tag_configure("impar", background=self.COLOR_FILA_IMPAR)

        scrollbar = ttk.Scrollbar(
            cuerpo, orient="vertical", command=self.tree_asignaciones.yview
        )
        self.tree_asignaciones.configure(yscrollcommand=scrollbar.set)
        self.tree_asignaciones.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def crear_panel_estadisticas(self, parent):
        cuerpo = self.crear_tarjeta(parent, "Estadísticas del Sistema")

        self.frame_tarjetas = tk.Frame(cuerpo, bg=self.COLOR_FONDO_TARJETA)
        self.frame_tarjetas.pack(fill="x", pady=(0, 10))

        self.lbl_estadisticas = tk.Label(
            cuerpo, justify="left", font=("Consolas", 10),
            bg=self.COLOR_FONDO_TARJETA, fg=self.COLOR_TEXTO
        )
        self.lbl_estadisticas.pack(anchor="w")

        self.actualizar_estadisticas()

    def crear_mini_tarjeta(self, parent, titulo, valor, color):
        tarjeta = tk.Frame(
            parent, bg=color, width=200, height=70
        )
        tarjeta.pack(side="left", padx=6, pady=4)
        tarjeta.pack_propagate(False)

        tk.Label(
            tarjeta, text=titulo, font=("Segoe UI", 9, "bold"),
            bg=color, fg="#FFFFFF"
        ).pack(anchor="w", padx=10, pady=(8, 0))

        tk.Label(
            tarjeta, text=valor, font=("Segoe UI", 14, "bold"),
            bg=color, fg="#FFFFFF"
        ).pack(anchor="w", padx=10)

    def procesar(self):
        if len(self.solicitudes) == 0:
            messagebox.showwarning("Aviso", "No existen solicitudes registradas.")
            return

        try:
            (asignaciones, no_atendidas, tiempo,
             conflictos_resueltos, ingreso_perdido) = asignar_solicitudes_voraz(
                self.vehiculos, self.solicitudes
            )
        except Exception as error:
            messagebox.showerror(
                "Error al procesar",
                f"Ocurrió un error al ejecutar el algoritmo voraz:\n{error}"
            )
            return

        self.tiempo = tiempo
        self.conflictos_resueltos = conflictos_resueltos
        self.ingreso_perdido = ingreso_perdido

        self.tree_asignaciones.delete(*self.tree_asignaciones.get_children())

        self.ingreso_total = 0
        self.total_devuelto = 0

        mensajes_asignacion = []

        for i, (solicitud, vehiculo, total, diferencia_total) in enumerate(asignaciones):
            self.ingreso_total += total
            self.total_devuelto += diferencia_total
            fila_tag = "par" if i % 2 == 0 else "impar"

            self.tree_asignaciones.insert(
                "", tk.END,
                values=(
                    solicitud.cliente,
                    f"{vehiculo.modelo} ({vehiculo.placa})",
                    f"S/ {vehiculo.tarifa:.2f}",
                    solicitud.dias,
                    f"S/ {total:.2f}",
                    f"S/ {diferencia_total:.2f}"
                ),
                tags=(fila_tag,)
            )

            if solicitud.diferencia_diaria > 0:
                mensajes_asignacion.append(
                    f"- {solicitud.cliente}: se le asignó un {vehiculo.modelo} a "
                    f"S/ {vehiculo.tarifa:.2f}/día. Se le devuelven "
                    f"S/ {solicitud.diferencia_diaria:.2f} diarios "
                    f"(S/ {diferencia_total:.2f} en {solicitud.dias} días) "
                    f"de su presupuesto original."
                )

        self.refrescar_flota()
        self.refrescar_solicitudes()
        self.actualizar_estadisticas()

        resumen = (
            f"Solicitudes atendidas: {len(asignaciones)}\n"
            f"No atendidas: {len(no_atendidas)}\n"
        )
        if mensajes_asignacion:
            resumen += "\n" + "\n".join(mensajes_asignacion)

        messagebox.showinfo("Proceso finalizado", resumen)

        for solicitud in no_atendidas:
            if solicitud.motivo_no_atendida == "sin_stock":
                messagebox.showinfo(
                    "Sin stock",
                    f"Lo sentimos {solicitud.cliente}, por el momento no "
                    f"contamos con unidades de tipo '{solicitud.tipo_solicitado}'. "
                    f"Prueba con otra categoría."
                )
            elif solicitud.motivo_no_atendida == "presupuesto_insuficiente":
                messagebox.showinfo(
                    "Presupuesto insuficiente",
                    f"Ups {solicitud.cliente}, tu presupuesto de "
                    f"S/ {solicitud.presupuesto_diario:.2f} se quedó corto "
                    f"para la categoría '{solicitud.tipo_solicitado}'. El "
                    f"vehículo más económico disponible cuesta "
                    f"S/ {solicitud.tarifa_minima_tipo:.2f}/día. "
                    f"¿Deseas ajustar tu presupuesto?"
                )

    def actualizar_estadisticas(self):
        disponibles = sum(1 for v in self.vehiculos if v.disponible)
        ocupados = len(self.vehiculos) - disponibles

        atendidas = sum(1 for s in self.solicitudes if s.estado == "Atendida")
        no_atendidas = sum(1 for s in self.solicitudes if s.estado == "No atendida")

        ingreso_promedio = self.ingreso_total / atendidas if atendidas > 0 else 0

        for widget in self.frame_tarjetas.winfo_children():
            widget.destroy()

        self.crear_mini_tarjeta(
            self.frame_tarjetas, "VEHÍCULOS DISPONIBLES", str(disponibles), self.COLOR_EXITO
        )
        self.crear_mini_tarjeta(
            self.frame_tarjetas, "VEHÍCULOS OCUPADOS", str(ocupados), self.COLOR_ADVERTENCIA
        )
        self.crear_mini_tarjeta(
            self.frame_tarjetas, "SOLICITUDES ATENDIDAS", str(atendidas), self.COLOR_ACENTO
        )
        self.crear_mini_tarjeta(
            self.frame_tarjetas, "NO ATENDIDAS", str(no_atendidas), self.COLOR_PELIGRO
        )
        self.crear_mini_tarjeta(
            self.frame_tarjetas, "INGRESO TOTAL", f"S/ {self.ingreso_total:.2f}", self.COLOR_HEADER
        )

        texto = f"""Ingreso promedio por cliente : S/ {ingreso_promedio:.2f}
Total devuelto a clientes    : S/ {self.total_devuelto:.2f}
Conflictos resueltos por ingreso : {self.conflictos_resueltos}
Ingreso potencial perdido        : S/ {self.ingreso_perdido:.2f}

Tiempo de ejecución: {self.tiempo:.8f} segundos"""

        self.lbl_estadisticas.config(text=texto)

    # =====================================================
    # REINICIAR SISTEMA
    # =====================================================

    def reiniciar(self):
        if not messagebox.askyesno("Confirmación", "¿Desea reiniciar el sistema?"):
            return

        self.vehiculos = cargar_flota()
        self.solicitudes.clear()

        self.tree_solicitudes.delete(*self.tree_solicitudes.get_children())
        self.tree_asignaciones.delete(*self.tree_asignaciones.get_children())

        self.entry_cliente.delete(0, tk.END)
        self.entry_dias.delete(0, tk.END)
        self.entry_presupuesto.delete(0, tk.END)
        self.combo_tipo.set("")

        Solicitud.contador = 1
        self.ingreso_total = 0
        self.total_devuelto = 0
        self.conflictos_resueltos = 0
        self.ingreso_perdido = 0
        self.tiempo = 0

        self.refrescar_flota()
        self.actualizar_estadisticas()

        messagebox.showinfo("Sistema", "El sistema fue reiniciado correctamente.")
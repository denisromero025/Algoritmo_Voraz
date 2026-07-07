import tkinter as tk
from tkinter import ttk, messagebox

from flota import crear_flota_inicial, TIPOS_VEHICULO
from modelos import Solicitud
from validaciones import validar_solicitud
from algoritmo_voraz import asignar_solicitudes_voraz


class AplicacionAlquiler(tk.Tk):

    COLOR_FONDO = "#F4F6F8"
    COLOR_BARRA = "#1B4965"
    COLOR_TEXTO_BARRA = "#FFFFFF"

    def __init__(self):
        super().__init__()
        self.title("Sistema Inteligente de Alquiler de Autos - Algoritmo Voraz")
        self.geometry("980x640")
        self.minsize(900, 600)
        self.configure(bg=self.COLOR_FONDO)

        self.vehiculos = crear_flota_inicial()
        self.solicitudes = []

        self._construir_estilos()
        self._construir_encabezado()
        self._construir_pestañas()

        self.refrescar_flota()
        self.refrescar_solicitudes()

    # ------------------------------------------------------------------ UI --
    def _construir_estilos(self):
        estilo = ttk.Style(self)
        try:
            estilo.theme_use("clam")
        except tk.TclError:
            pass
        estilo.configure("TNotebook", background=self.COLOR_FONDO)
        estilo.configure("TNotebook.Tab", padding=(16, 8), font=("Segoe UI", 10, "bold"))
        estilo.configure("Treeview", rowheight=26, font=("Segoe UI", 10))
        estilo.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        estilo.configure("Accent.TButton", font=("Segoe UI", 10, "bold"))

    def _construir_encabezado(self):
        barra = tk.Frame(self, bg=self.COLOR_BARRA, height=64)
        barra.pack(side="top", fill="x")

        tk.Label(
            barra, text="🚗  Sistema Inteligente de Alquiler de Autos",
            bg=self.COLOR_BARRA, fg=self.COLOR_TEXTO_BARRA,
            font=("Segoe UI", 15, "bold")
        ).pack(side="left", padx=18, pady=12)

        tk.Button(
            barra, text="⟲ Restablecer sistema", command=self.restablecer_sistema,
            bg="#E63946", fg="white", relief="flat", font=("Segoe UI", 10, "bold"),
            activebackground="#C1121F", activeforeground="white", padx=12, pady=6,
            cursor="hand2"
        ).pack(side="right", padx=18)

    def _construir_pestañas(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_flota = tk.Frame(self.notebook, bg=self.COLOR_FONDO)
        self.tab_solicitudes = tk.Frame(self.notebook, bg=self.COLOR_FONDO)
        self.tab_resultados = tk.Frame(self.notebook, bg=self.COLOR_FONDO)

        self.notebook.add(self.tab_flota, text="  🚙  Flota de Vehículos  ")
        self.notebook.add(self.tab_solicitudes, text="  📝  Solicitudes  ")
        self.notebook.add(self.tab_resultados, text="  ⚙️  Procesar y Resultados  ")

        self._construir_tab_flota()
        self._construir_tab_solicitudes()
        self._construir_tab_resultados()

    # ------------------------------------------------------------ TAB FLOTA --
    def _construir_tab_flota(self):
        contenedor = self.tab_flota

        tk.Label(
            contenedor, text="Vehículos disponibles en la flota",
            bg=self.COLOR_FONDO, font=("Segoe UI", 12, "bold")
        ).pack(anchor="w", padx=14, pady=(14, 6))

        columnas = ("id", "placa", "tipo", "modelo", "tarifa", "estado")
        self.tree_flota = ttk.Treeview(contenedor, columns=columnas, show="headings", height=14)
        encabezados = {
            "id": "ID", "placa": "Placa", "tipo": "Tipo",
            "modelo": "Modelo", "tarifa": "Tarifa/día (S/)", "estado": "Estado"
        }
        anchos = {"id": 60, "placa": 100, "tipo": 110, "modelo": 160, "tarifa": 130, "estado": 120}
        for col in columnas:
            self.tree_flota.heading(col, text=encabezados[col])
            self.tree_flota.column(col, width=anchos[col], anchor="center")

        self.tree_flota.tag_configure("libre", foreground="#2A9D8F")
        self.tree_flota.tag_configure("ocupado", foreground="#E63946")
        self.tree_flota.pack(fill="both", expand=True, padx=14, pady=6)

        self.lbl_resumen_flota = tk.Label(
            contenedor, text="", bg=self.COLOR_FONDO, font=("Segoe UI", 10)
        )
        self.lbl_resumen_flota.pack(anchor="w", padx=14, pady=(0, 10))

    def refrescar_flota(self):
        self.tree_flota.delete(*self.tree_flota.get_children())
        for v in self.vehiculos:
            estado = "Disponible" if v.disponible else "Asignado"
            tag = "libre" if v.disponible else "ocupado"
            self.tree_flota.insert(
                "", "end",
                values=(v.id_vehiculo, v.placa, v.tipo, v.modelo, f"{v.tarifa_diaria:.2f}", estado),
                tags=(tag,)
            )
        disponibles = sum(1 for v in self.vehiculos if v.disponible)
        self.lbl_resumen_flota.config(
            text=f"Total: {len(self.vehiculos)}  |  Disponibles: {disponibles}  |  Asignados: {len(self.vehiculos) - disponibles}"
        )

    # ------------------------------------------------------ TAB SOLICITUDES --
    def _construir_tab_solicitudes(self):
        contenedor = self.tab_solicitudes

        panel_form = tk.LabelFrame(
            contenedor, text="Registrar nueva solicitud", bg=self.COLOR_FONDO,
            font=("Segoe UI", 10, "bold"), padx=14, pady=12
        )
        panel_form.pack(fill="x", padx=14, pady=(14, 8))

        tk.Label(panel_form, text="Nombre del cliente:", bg=self.COLOR_FONDO).grid(row=0, column=0, sticky="w", pady=4)
        self.entry_cliente = ttk.Entry(panel_form, width=28)
        self.entry_cliente.grid(row=0, column=1, padx=8, pady=4)

        tk.Label(panel_form, text="Tipo de vehículo:", bg=self.COLOR_FONDO).grid(row=0, column=2, sticky="w", pady=4)
        self.combo_tipo = ttk.Combobox(panel_form, values=TIPOS_VEHICULO, state="readonly", width=15)
        self.combo_tipo.grid(row=0, column=3, padx=8, pady=4)

        tk.Label(panel_form, text="Monto ofrecido (S/):", bg=self.COLOR_FONDO).grid(row=0, column=4, sticky="w", pady=4)
        self.entry_monto = ttk.Entry(panel_form, width=12)
        self.entry_monto.grid(row=0, column=5, padx=8, pady=4)

        ttk.Button(
            panel_form, text="➕ Agregar solicitud", style="Accent.TButton",
            command=self.registrar_solicitud
        ).grid(row=0, column=6, padx=(14, 0))

        tk.Label(
            contenedor, text="Solicitudes registradas", bg=self.COLOR_FONDO, font=("Segoe UI", 12, "bold")
        ).pack(anchor="w", padx=14, pady=(8, 6))

        columnas = ("id", "cliente", "tipo", "monto", "estado", "vehiculo")
        self.tree_solicitudes = ttk.Treeview(contenedor, columns=columnas, show="headings", height=11)
        encabezados = {
            "id": "ID", "cliente": "Cliente", "tipo": "Tipo solicitado",
            "monto": "Monto (S/)", "estado": "Estado", "vehiculo": "Vehículo asignado"
        }
        anchos = {"id": 50, "cliente": 170, "tipo": 130, "monto": 100, "estado": 110, "vehiculo": 160}
        for col in columnas:
            self.tree_solicitudes.heading(col, text=encabezados[col])
            self.tree_solicitudes.column(col, width=anchos[col], anchor="center")
        self.tree_solicitudes.pack(fill="both", expand=True, padx=14, pady=6)

    def registrar_solicitud(self):
        cliente = self.entry_cliente.get()
        tipo = self.combo_tipo.get()
        monto_texto = self.entry_monto.get()

        es_valido, mensaje, monto = validar_solicitud(cliente, tipo, monto_texto)
        if not es_valido:
            messagebox.showwarning("Datos inválidos", mensaje)
            return

        nueva = Solicitud(cliente.strip(), tipo, monto)
        self.solicitudes.append(nueva)

        self.entry_cliente.delete(0, "end")
        self.combo_tipo.set("")
        self.entry_monto.delete(0, "end")

        self.refrescar_solicitudes()
        messagebox.showinfo("Solicitud registrada", f"Solicitud #{nueva.id_solicitud} agregada correctamente.")

    def refrescar_solicitudes(self):
        self.tree_solicitudes.delete(*self.tree_solicitudes.get_children())
        for s in self.solicitudes:
            vehiculo_txt = s.vehiculo_asignado.placa if s.vehiculo_asignado else "-"
            self.tree_solicitudes.insert(
                "", "end",
                values=(s.id_solicitud, s.cliente, s.tipo_solicitado,
                        f"{s.monto_ofrecido:.2f}", s.estado, vehiculo_txt)
            )

    # -------------------------------------------------------- TAB RESULTADOS --
    def _construir_tab_resultados(self):
        contenedor = self.tab_resultados

        panel_top = tk.Frame(contenedor, bg=self.COLOR_FONDO)
        panel_top.pack(fill="x", padx=14, pady=14)

        ttk.Button(
            panel_top, text="▶ Procesar solicitudes",
            style="Accent.TButton", command=self.procesar_solicitudes
        ).pack(side="left")

        self.lbl_tiempo = tk.Label(
            panel_top, text="Tiempo de ejecución: --",
            bg=self.COLOR_FONDO, font=("Segoe UI", 11, "bold"), fg=self.COLOR_BARRA
        )
        self.lbl_tiempo.pack(side="right")

        panel_resultados = tk.Frame(contenedor, bg=self.COLOR_FONDO)
        panel_resultados.pack(fill="both", expand=True, padx=14, pady=6)
        panel_resultados.columnconfigure(0, weight=1)
        panel_resultados.columnconfigure(1, weight=1)
        panel_resultados.rowconfigure(1, weight=1)

        tk.Label(panel_resultados, text="✅ Solicitudes atendidas", bg=self.COLOR_FONDO,
                 font=("Segoe UI", 11, "bold"), fg="#2A9D8F").grid(row=0, column=0, sticky="w", pady=(0, 4))
        tk.Label(panel_resultados, text="⛔ Solicitudes no atendidas", bg=self.COLOR_FONDO,
                 font=("Segoe UI", 11, "bold"), fg="#E63946").grid(row=0, column=1, sticky="w", pady=(0, 4))

        cols_ok = ("cliente", "tipo", "monto", "vehiculo", "tarifa")
        self.tree_atendidas = ttk.Treeview(panel_resultados, columns=cols_ok, show="headings", height=12)
        for col, txt, w in [("cliente", "Cliente", 130), ("tipo", "Tipo", 90),
                             ("monto", "Monto ofrecido", 110), ("vehiculo", "Vehículo", 100),
                             ("tarifa", "Tarifa/día", 90)]:
            self.tree_atendidas.heading(col, text=txt)
            self.tree_atendidas.column(col, width=w, anchor="center")
        self.tree_atendidas.grid(row=1, column=0, sticky="nsew", padx=(0, 6))

        cols_no = ("cliente", "tipo", "monto", "motivo")
        self.tree_no_atendidas = ttk.Treeview(panel_resultados, columns=cols_no, show="headings", height=12)
        for col, txt, w in [("cliente", "Cliente", 130), ("tipo", "Tipo", 90),
                             ("monto", "Monto ofrecido", 110), ("motivo", "Motivo", 220)]:
            self.tree_no_atendidas.heading(col, text=txt)
            self.tree_no_atendidas.column(col, width=w, anchor="center")
        self.tree_no_atendidas.grid(row=1, column=1, sticky="nsew", padx=(6, 0))

        self.lbl_resumen_resultado = tk.Label(
            contenedor, text="", bg=self.COLOR_FONDO, font=("Segoe UI", 10, "italic")
        )
        self.lbl_resumen_resultado.pack(anchor="w", padx=14, pady=(8, 10))

    def procesar_solicitudes(self):
        pendientes = [s for s in self.solicitudes if s.estado == "Pendiente"]
        if not pendientes:
            messagebox.showinfo("Sin solicitudes", "No hay solicitudes pendientes por procesar.")
            return

        asignaciones, no_atendidas, tiempo = asignar_solicitudes_voraz(self.vehiculos, self.solicitudes)

        self.tree_atendidas.delete(*self.tree_atendidas.get_children())
        for solicitud, vehiculo in asignaciones:
            self.tree_atendidas.insert(
                "", "end",
                values=(solicitud.cliente, solicitud.tipo_solicitado,
                        f"{solicitud.monto_ofrecido:.2f}", vehiculo.placa, f"{vehiculo.tarifa_diaria:.2f}")
            )

        self.tree_no_atendidas.delete(*self.tree_no_atendidas.get_children())
        for solicitud in no_atendidas:
            self.tree_no_atendidas.insert(
                "", "end",
                values=(solicitud.cliente, solicitud.tipo_solicitado,
                        f"{solicitud.monto_ofrecido:.2f}",
                        "No hay vehículos disponibles de este tipo")
            )

        self.lbl_tiempo.config(
            text=f"Tiempo de ejecución: {tiempo * 1000:.4f} ms  ({tiempo * 1_000_000:.1f} µs)"
        )
        self.lbl_resumen_resultado.config(
            text=(f"Procesadas {len(pendientes)} solicitudes  →  "
                  f"{len(asignaciones)} atendidas, {len(no_atendidas)} no atendidas.")
        )

        self.refrescar_flota()
        self.refrescar_solicitudes()

    # ------------------------------------------------------------- RESET --
    def restablecer_sistema(self):
        confirmar = messagebox.askyesno(
            "Restablecer sistema",
            "Esto eliminará todas las solicitudes registradas y liberará la flota.\n¿Desea continuar?"
        )
        if not confirmar:
            return

        self.vehiculos = crear_flota_inicial()
        self.solicitudes = []

        self.entry_cliente.delete(0, "end")
        self.combo_tipo.set("")
        self.entry_monto.delete(0, "end")

        self.tree_atendidas.delete(*self.tree_atendidas.get_children())
        self.tree_no_atendidas.delete(*self.tree_no_atendidas.get_children())
        self.lbl_tiempo.config(text="Tiempo de ejecución: --")
        self.lbl_resumen_resultado.config(text="")

        self.refrescar_flota()
        self.refrescar_solicitudes()
        messagebox.showinfo("Sistema restablecido", "La flota y las solicitudes fueron restablecidas.")

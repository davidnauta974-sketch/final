import tkinter as tk
from tkinter import messagebox, ttk

from src.services.soporte_service import SoporteService


class SoporteGUI:
    """Interfaz de soporte; las operaciones se delegan al servicio."""

    FONDO = "#eef3f8"
    TEXTO = "#172b45"
    SECUNDARIO = "#607187"
    ACENTO = "#2563eb"

    def __init__(self, master, servicio: SoporteService):
        self.master = master
        self.servicio = servicio
        master.title("Sistema de Soporte Técnico")
        master.geometry("720x680")
        master.minsize(620, 640)
        master.configure(bg=self.FONDO)
        self.configurar_estilos()
        self.crear_widgets()
        self.actualizar_estado()
        self.entry_nombre.focus_set()

    def configurar_estilos(self):
        """Estilos de Tkinter, sin dependencias adicionales."""
        estilo = ttk.Style(self.master)
        estilo.theme_use("clam")
        estilo.configure("Soporte.TEntry", padding=9, font=("Segoe UI", 11),
                         fieldbackground="white", foreground=self.TEXTO,
                         bordercolor="#d4deea", lightcolor="#d4deea",
                         darkcolor="#d4deea")
        estilo.map("Soporte.TEntry", bordercolor=[("focus", self.ACENTO)])
        estilo.configure("Primario.TButton", font=("Segoe UI", 10, "bold"),
                         padding=(18, 11), background=self.ACENTO,
                         foreground="white", borderwidth=0)
        estilo.map("Primario.TButton", background=[("pressed", "#1e40af"),
                                                   ("active", "#1d4ed8")])
        estilo.configure("Atender.TButton", font=("Segoe UI", 10, "bold"),
                         padding=(18, 11), background="#0f766e",
                         foreground="white", borderwidth=0)
        estilo.map("Atender.TButton", background=[("pressed", "#115e59"),
                                                  ("active", "#0d9488")])
        estilo.configure("Reset.TButton", font=("Segoe UI", 10, "bold"),
                         padding=(14, 11), background="#fce7e7",
                         foreground="#9f2828", borderwidth=0)
        estilo.map("Reset.TButton", background=[("pressed", "#fecaca"),
                                                ("active", "#fee2e2")])

    def crear_widgets(self):
        contenedor = tk.Frame(self.master, bg=self.FONDO, padx=28, pady=22)
        contenedor.pack(fill="both", expand=True)
        contenedor.columnconfigure(0, weight=1)

        tk.Label(contenedor, text="CENTRO DE ATENCIÓN", bg=self.FONDO,
                 fg=self.ACENTO, font=("Segoe UI", 9, "bold")).grid(sticky="w")
        tk.Label(contenedor, text="Soporte técnico", bg=self.FONDO,
                 fg=self.TEXTO, font=("Segoe UI", 25, "bold")).grid(sticky="w", pady=(3, 2))
        tk.Label(contenedor, text="Registra solicitudes y atiende a tus clientes en orden de llegada.",
                 bg=self.FONDO, fg=self.SECUNDARIO,
                 font=("Segoe UI", 10)).grid(sticky="w", pady=(0, 18))

        frame_nuevo = tk.Frame(contenedor, bg="white", padx=22, pady=18,
                               highlightbackground="#dce5ef", highlightthickness=1)
        frame_nuevo.grid(sticky="ew")
        frame_nuevo.columnconfigure(0, weight=1)
        tk.Label(frame_nuevo, text="Nueva solicitud", bg="white", fg=self.TEXTO,
                 font=("Segoe UI", 14, "bold")).grid(sticky="w", pady=(0, 12))
        tk.Label(frame_nuevo, text="Nombre del cliente", bg="white", fg=self.SECUNDARIO,
                 font=("Segoe UI", 10)).grid(sticky="w", pady=(0, 5))
        self.entry_nombre = ttk.Entry(frame_nuevo, style="Soporte.TEntry")
        self.entry_nombre.grid(sticky="ew", pady=(0, 12))
        tk.Label(frame_nuevo, text="Descripción del problema", bg="white", fg=self.SECUNDARIO,
                 font=("Segoe UI", 10)).grid(sticky="w", pady=(0, 5))
        self.entry_descripcion = ttk.Entry(frame_nuevo, style="Soporte.TEntry")
        self.entry_descripcion.grid(sticky="ew", pady=(0, 14))
        ttk.Button(frame_nuevo, text="Registrar solicitud", style="Primario.TButton",
                   command=self.registrar).grid(sticky="ew")

        frame_atencion = tk.Frame(contenedor, bg="white", padx=22, pady=18,
                                  highlightbackground="#dce5ef", highlightthickness=1)
        frame_atencion.grid(sticky="ew", pady=(16, 0))
        frame_atencion.columnconfigure(0, weight=1)
        tk.Label(frame_atencion, text="Próxima atención", bg="white", fg=self.TEXTO,
                 font=("Segoe UI", 14, "bold")).grid(row=0, column=0, sticky="w")
        self.lbl_estado = tk.Label(frame_atencion, bg="#e8efff", fg="#1e40af",
                                   font=("Segoe UI", 9, "bold"), padx=10, pady=5)
        self.lbl_estado.grid(row=1, column=0, sticky="w", pady=(10, 9))
        self.lbl_siguiente = tk.Label(frame_atencion, bg="white", fg=self.TEXTO,
                                      font=("Segoe UI", 12, "bold"), anchor="w", justify="left")
        self.lbl_siguiente.grid(row=2, column=0, sticky="ew")
        self.lbl_detalle = tk.Label(frame_atencion, bg="white", fg=self.SECUNDARIO,
                                    font=("Segoe UI", 10), anchor="w", justify="left")
        self.lbl_detalle.grid(row=3, column=0, sticky="ew", pady=(4, 12))
        # Ajusta los textos largos al ancho disponible al redimensionar la ventana.
        frame_atencion.bind("<Configure>", self.ajustar_textos)
        acciones = tk.Frame(frame_atencion, bg="white")
        acciones.grid(row=4, column=0, sticky="ew")
        acciones.columnconfigure(0, weight=1)
        ttk.Button(acciones, text="Atender siguiente solicitud", style="Atender.TButton",
                   command=self.atender).grid(row=0, column=0, sticky="ew", padx=(0, 10))
        ttk.Button(acciones, text="Reiniciar IDs", style="Reset.TButton",
                   command=self.reiniciar_ids).grid(row=0, column=1, sticky="ew")
        tk.Label(contenedor, text="Orden de atención: primero en llegar, primero en ser atendido.",
                 bg=self.FONDO, fg=self.SECUNDARIO,
                 font=("Segoe UI", 9)).grid(sticky="w", pady=(15, 0))

    def ajustar_textos(self, evento):
        ancho = max(180, evento.width - 46)
        self.lbl_siguiente.config(wraplength=ancho)
        self.lbl_detalle.config(wraplength=ancho)

    def actualizar_estado(self):
        pendientes = self.servicio.cantidad_pendientes()
        self.lbl_estado.config(text=f"Solicitudes pendientes: {pendientes}")
        if self.servicio.hay_solicitudes_pendientes():
            siguiente = self.servicio.consultar_siguiente()
            self.lbl_siguiente.config(text=f"#{siguiente.id_solicitud} · {siguiente.nombre_cliente}")
            self.lbl_detalle.config(text=siguiente.descripcion)
        else:
            self.lbl_siguiente.config(text="No hay solicitudes en espera")
            self.lbl_detalle.config(text="Registra una solicitud para comenzar la atención.")

    def registrar(self):
        nombre = self.entry_nombre.get()
        desc = self.entry_descripcion.get()
        try:
            solicitud = self.servicio.registrar_solicitud(nombre, desc)
            messagebox.showinfo("Éxito", f"Solicitud registrada con ID: {solicitud.id_solicitud}", parent=self.master)
            self.entry_nombre.delete(0, tk.END)
            self.entry_descripcion.delete(0, tk.END)
            self.actualizar_estado()
            self.entry_nombre.focus_set()
        except ValueError as e:
            messagebox.showerror("Error", str(e), parent=self.master)

    def atender(self):
        try:
            solicitud = self.servicio.atender_solicitud()
            messagebox.showinfo("Atención", f"Se ha atendido la solicitud de: {solicitud.nombre_cliente}\nProblema: {solicitud.descripcion}", parent=self.master)
            self.actualizar_estado()
        except IndexError:
            messagebox.showwarning("Aviso", "No hay solicitudes pendientes por atender.", parent=self.master)

    def reiniciar_ids(self):
        pendientes = self.servicio.cantidad_pendientes()
        if pendientes and not messagebox.askyesno(
            "Reiniciar IDs",
            f"Se eliminarán {pendientes} solicitudes pendientes y la numeración "
            "volverá a empezar desde 1.\n\n¿Deseas continuar?",
            parent=self.master,
        ):
            return
        try:
            self.servicio.reiniciar_ids()
        except OSError as error:
            messagebox.showerror("No se pudo reiniciar", str(error), parent=self.master)
            return
        self.actualizar_estado()
        self.entry_nombre.focus_set()
        messagebox.showinfo(
            "IDs reiniciados", "La cola está vacía. La próxima solicitud tendrá ID 1.",
            parent=self.master,
        )


def iniciar_gui(servicio: SoporteService):
    root = tk.Tk()
    SoporteGUI(root, servicio)
    root.mainloop()

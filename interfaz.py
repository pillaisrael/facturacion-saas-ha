import tkinter as tk
from tkinter import messagebox
from simulador import Simulador


class Interfaz:
    """
    Ventana principal del simulador.
    Muestra servidores, métricas, botones y eventos.
    """

    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Simulador HA - Facturación Electrónica")
        self.ventana.geometry("780x560")
        self.ventana.resizable(False, False)

        self.simulador = Simulador()
        self.etiquetas_servidores = []

        self.crear_interfaz()
        self.actualizar_pantalla()

    def crear_interfaz(self):
        titulo = tk.Label(
            self.ventana,
            text="Empresa SaaS de Facturación Electrónica - Alta Disponibilidad",
            font=("Arial", 15, "bold")
        )
        titulo.pack(pady=10)

        contenedor = tk.Frame(self.ventana)
        contenedor.pack(padx=10, pady=5)

        panel_servidores = tk.LabelFrame(contenedor, text="Servidores")
        panel_servidores.grid(row=0, column=0, padx=10)

        for i in range(3):
            etiqueta = tk.Label(
                panel_servidores,
                text="",
                width=38,
                height=5,
                anchor="w",
                justify="left",
                relief="solid",
                padx=10,
                font=("Arial", 10)
            )
            etiqueta.pack(padx=10, pady=8)
            self.etiquetas_servidores.append(etiqueta)

        panel_derecho = tk.Frame(contenedor)
        panel_derecho.grid(row=0, column=1, padx=10)

        panel_metricas = tk.LabelFrame(panel_derecho, text="Métricas")
        panel_metricas.pack(fill="x", pady=5)

        self.etiqueta_metricas = tk.Label(
            panel_metricas,
            text="",
            justify="left",
            font=("Consolas", 10),
            width=32,
            height=6
        )
        self.etiqueta_metricas.pack(padx=10, pady=10)

        panel_botones = tk.LabelFrame(panel_derecho, text="Acciones del demo")
        panel_botones.pack(fill="x", pady=5)

        tk.Button(panel_botones, text="Generar 50 facturas", width=25, command=self.generar).pack(pady=3)
        tk.Button(panel_botones, text="Ataque DDoS", width=25, command=self.ddos).pack(pady=3)
        tk.Button(panel_botones, text="Caída de servidor", width=25, command=self.caida).pack(pady=3)
        tk.Button(panel_botones, text="Recuperar servidor", width=25, command=self.recuperar).pack(pady=3)
        tk.Button(panel_botones, text="Liberar carga", width=25, command=self.liberar).pack(pady=3)
        tk.Button(panel_botones, text="Atender cola", width=25, command=self.atender).pack(pady=3)
        tk.Button(panel_botones, text="Exportar reporte CSV", width=25, command=self.reporte).pack(pady=3)

        panel_eventos = tk.LabelFrame(self.ventana, text="Registro de eventos")
        panel_eventos.pack(padx=15, pady=10, fill="x")

        self.caja_eventos = tk.Text(panel_eventos, height=7, width=86)
        self.caja_eventos.pack(padx=10, pady=10)

    def generar(self):
        self.simulador.generar_facturas(50)
        self.actualizar_pantalla()

    def ddos(self):
        self.simulador.ataque_ddos()
        self.actualizar_pantalla()

    def caida(self):
        self.simulador.caer_servidor()
        self.actualizar_pantalla()

    def recuperar(self):
        self.simulador.recuperar_servidor()
        self.actualizar_pantalla()

    def liberar(self):
        self.simulador.liberar_carga()
        self.actualizar_pantalla()

    def atender(self):
        self.simulador.atender_cola()
        self.actualizar_pantalla()

    def reporte(self):
        self.simulador.exportar_reporte()
        self.actualizar_pantalla()
        messagebox.showinfo("Reporte", "Reporte guardado como reporte_resultados.csv")

    def actualizar_pantalla(self):
        for i, servidor in enumerate(self.simulador.servidores):
            porcentaje = servidor.porcentaje_carga()

            if servidor.estado == "Caído":
                color = "#ff9999"
            elif porcentaje >= 85:
                color = "#fff099"
            else:
                color = "#b6f2b6"

            texto = (
                f"{servidor.nombre}\n"
                f"Estado: {servidor.estado}\n"
                f"Carga: {servidor.carga}/{servidor.capacidad} ({porcentaje:.1f}%)"
            )

            self.etiquetas_servidores[i].config(text=texto, bg=color)

        metricas = (
            f"Facturas generadas:  {self.simulador.facturas_generadas}\n"
            f"Facturas procesadas: {self.simulador.facturas_procesadas}\n"
            f"Facturas en cola:    {self.simulador.facturas_en_cola}\n"
            f"Disponibilidad:      {self.simulador.disponibilidad():.2f}%"
        )

        self.etiqueta_metricas.config(text=metricas)

        self.caja_eventos.delete("1.0", tk.END)

        for evento in self.simulador.eventos[-8:]:
            self.caja_eventos.insert(tk.END, "- " + evento + "\n")

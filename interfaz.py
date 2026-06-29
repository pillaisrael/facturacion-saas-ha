# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

from simulador import Simulador


class Interfaz:
    """
    Interfaz gráfica del simulador.
    Permite ejecutar la demo con botones y ver métricas en tiempo real.
    """

    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("SaaS Facturación Electrónica - Balanceo, Rate Limiting y HA")
        self.ventana.geometry("980x620")
        self.ventana.minsize(900, 580)
        self.ventana.resizable(True, True)

        self.simulador = Simulador()
        self.etiquetas_servidores = []

        self.crear_interfaz()
        self.actualizar_pantalla()

    def crear_interfaz(self):
        titulo = tk.Label(
            self.ventana,
            text="Empresa SaaS de Facturación Electrónica - Control de Consumo API",
            font=("Arial", 14, "bold")
        )
        titulo.pack(pady=8)

        contenedor = tk.Frame(self.ventana)
        contenedor.pack(fill="both", expand=True, padx=10, pady=5)

        panel_servidores = tk.LabelFrame(contenedor, text="Servidores")
        panel_servidores.grid(row=0, column=0, sticky="nsew", padx=8, pady=4)

        for _ in range(4):
            etiqueta = tk.Label(
                panel_servidores,
                text="",
                width=42,
                height=4,
                anchor="w",
                justify="left",
                relief="solid",
                padx=10,
                font=("Arial", 10)
            )
            etiqueta.pack(fill="x", padx=10, pady=5)
            self.etiquetas_servidores.append(etiqueta)

        panel_derecho = tk.Frame(contenedor)
        panel_derecho.grid(row=0, column=1, sticky="nsew", padx=8, pady=4)

        contenedor.columnconfigure(0, weight=1)
        contenedor.columnconfigure(1, weight=1)
        contenedor.rowconfigure(0, weight=1)

        panel_metricas = tk.LabelFrame(panel_derecho, text="Métricas")
        panel_metricas.pack(fill="x", pady=4)

        self.etiqueta_metricas = tk.Label(
            panel_metricas,
            text="",
            justify="left",
            font=("Consolas", 10),
            anchor="w",
            width=45,
            height=7
        )
        self.etiqueta_metricas.pack(fill="x", padx=8, pady=6)

        panel_botones = tk.LabelFrame(panel_derecho, text="Acciones del demo")
        panel_botones.pack(fill="x", pady=4)

        botones = [
            ("Tráfico normal", self.trafico_normal),
            ("Cliente grande SIN rate limiting", self.sin_limite),
            ("Activar rate limiting", self.activar_limite),
            ("Cliente grande CON rate limiting", self.con_limite),
            ("Cliente crítico a servidor dedicado", self.critico),
            ("Caída de servidor compartido", self.caida),
            ("Recuperar servidor", self.recuperar),
            ("Liberar carga", self.liberar),
            ("Atender cola", self.atender),
            ("Exportar reporte CSV", self.reporte),
        ]

        for texto, comando in botones:
            tk.Button(panel_botones, text=texto, width=36, command=comando).pack(pady=2)

        panel_eventos = tk.LabelFrame(panel_derecho, text="Registro de eventos")
        panel_eventos.pack(fill="both", expand=True, pady=4)

        self.caja_eventos = ScrolledText(
            panel_eventos,
            height=7,
            width=48,
            font=("Consolas", 9),
            wrap="word"
        )
        self.caja_eventos.pack(fill="both", expand=True, padx=8, pady=6)

    def trafico_normal(self):
        self.simulador.trafico_normal()
        self.actualizar_pantalla()

    def sin_limite(self):
        self.simulador.pico_cliente_grande_sin_control()
        self.actualizar_pantalla()

    def activar_limite(self):
        self.simulador.activar_rate_limiting()
        self.actualizar_pantalla()

    def con_limite(self):
        self.simulador.pico_cliente_grande_con_limite()
        self.actualizar_pantalla()

    def critico(self):
        self.simulador.cliente_critico_dedicado()
        self.actualizar_pantalla()

    def caida(self):
        self.simulador.caer_servidor_compartido()
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

    def color_servidor(self, servidor):
        porcentaje = servidor.porcentaje_carga()

        if servidor.estado == "Caído":
            return "#ff9999"

        if porcentaje >= 85:
            return "#fff099"

        return "#b6f2b6"

    def actualizar_pantalla(self):
        for i, servidor in enumerate(self.simulador.servidores):
            porcentaje = servidor.porcentaje_carga()

            texto = (
                f"{servidor.nombre}\n"
                f"Grupo: {servidor.grupo}\n"
                f"Estado: {servidor.estado}\n"
                f"Carga: {servidor.carga}/{servidor.capacidad} ({porcentaje:.1f}%)"
            )

            self.etiquetas_servidores[i].config(text=texto, bg=self.color_servidor(servidor))

        estado_limitador = "Activo" if self.simulador.limitador.activo else "Inactivo"

        metricas = (
            f"Solicitudes generadas:   {self.simulador.solicitudes_generadas}\n"
            f"Solicitudes procesadas:  {self.simulador.solicitudes_procesadas}\n"
            f"Solicitudes en cola:     {len(self.simulador.cola)}\n"
            f"Solicitudes limitadas:   {self.simulador.solicitudes_limitadas}\n"
            f"Disponibilidad efectiva: {self.simulador.disponibilidad_efectiva():.2f}%\n"
            f"Rate limiting:           {estado_limitador}\n"
            f"Mayor consumo:           {self.simulador.cliente_mayor_consumo()}"
        )

        self.etiqueta_metricas.config(text=metricas)

        self.caja_eventos.config(state="normal")
        self.caja_eventos.delete("1.0", tk.END)

        for evento in self.simulador.eventos[-12:]:
            self.caja_eventos.insert(tk.END, "- " + evento + "\n")

        self.caja_eventos.see(tk.END)
        self.caja_eventos.config(state="disabled")

# -*- coding: utf-8 -*-

import csv
import random
from collections import deque

from cliente import Cliente
from servidor import Servidor
from balanceador import Balanceador
from limitador import LimitadorAPI


class Simulador:
    """
    Controla el experimento completo:
    clientes, servidores, balanceador, rate limiting, cola y métricas.
    """

    def __init__(self):
        self.servidores = [
            Servidor("Servidor Compartido 1", 150, "compartido"),
            Servidor("Servidor Compartido 2", 150, "compartido"),
            Servidor("Servidor Compartido 3", 150, "compartido"),
            Servidor("Servidor Dedicado Crítico", 180, "dedicado")
        ]

        self.clientes = {
            "pyme": Cliente("Cliente PYME", "Pequeño", "API-PYME-001", 60),
            "mediano": Cliente("Cliente Mediano", "Mediano", "API-MED-002", 100),
            "grande": Cliente("Cliente Grande API", "Grande", "API-GRA-003", 180),
            "critico": Cliente("Cliente Crítico", "Crítico", "API-CRI-004", 160, critico=True)
        }

        self.balanceador = Balanceador()
        self.limitador = LimitadorAPI()
        self.cola = deque()

        self.solicitudes_generadas = 0
        self.solicitudes_procesadas = 0
        self.solicitudes_limitadas = 0
        self.consumo_por_cliente = {cliente.nombre: 0 for cliente in self.clientes.values()}

        self.eventos = [
            "Experimento iniciado correctamente.",
            "Rate limiting inicial: inactivo.",
            "Infraestructura: 3 servidores compartidos y 1 servidor dedicado crítico."
        ]

    def generar_solicitudes(self, clave_cliente, cantidad, usar_dedicado=False):
        cliente = self.clientes[clave_cliente]

        self.solicitudes_generadas += cantidad
        self.consumo_por_cliente[cliente.nombre] += cantidad

        permitidas, limitadas = self.limitador.aplicar_limite(cliente, cantidad)
        self.solicitudes_limitadas += limitadas

        if usar_dedicado and cliente.critico:
            grupo = "dedicado"
        else:
            grupo = "compartido"

        procesadas = 0
        en_cola = 0

        for _ in range(permitidas):
            servidor = self.balanceador.elegir_servidor(self.servidores, grupo)

            if servidor is None:
                self.cola.append((clave_cliente, grupo))
                en_cola += 1
            else:
                servidor.recibir_solicitud()
                self.solicitudes_procesadas += 1
                procesadas += 1

        self.eventos.append(
            f"{cliente.nombre}: {cantidad} solicitudes | "
            f"procesadas: {procesadas}, cola: {en_cola}, limitadas: {limitadas}."
        )

    def trafico_normal(self):
        self.generar_solicitudes("pyme", 40)
        self.generar_solicitudes("mediano", 70)
        self.generar_solicitudes("pyme", 30)
        self.eventos.append("Tráfico normal ejecutado: clientes pequeños y medianos.")

    def pico_cliente_grande_sin_control(self):
        self.limitador.desactivar()
        self.eventos.append("Rate limiting desactivado: se prueba consumo excesivo.")
        self.generar_solicitudes("grande", 450)

    def activar_rate_limiting(self):
        self.limitador.activar()
        self.eventos.append("Rate limiting activado por API key.")

    def pico_cliente_grande_con_limite(self):
        self.generar_solicitudes("grande", 450)
        self.eventos.append("Cliente grande probado con rate limiting activo.")

    def cliente_critico_dedicado(self):
        self.generar_solicitudes("critico", 180, usar_dedicado=True)
        self.eventos.append("Cliente crítico enviado al servidor dedicado.")

    def caer_servidor_compartido(self):
        activos = [
            servidor for servidor in self.servidores
            if servidor.grupo == "compartido" and servidor.estado == "Activo"
        ]

        if len(activos) == 0:
            self.eventos.append("No hay servidores compartidos activos para simular fallo.")
            return

        servidor = random.choice(activos)
        servidor.caer()
        self.eventos.append(f"{servidor.nombre} sufrió una caída controlada.")

    def recuperar_servidor(self):
        caidos = [servidor for servidor in self.servidores if servidor.estado == "Caído"]

        if len(caidos) == 0:
            self.eventos.append("No existen servidores caídos para recuperar.")
            return

        servidor = random.choice(caidos)
        servidor.recuperar()
        self.eventos.append(f"{servidor.nombre} fue recuperado.")

    def liberar_carga(self):
        for servidor in self.servidores:
            servidor.liberar_carga(80)

        self.eventos.append("Se liberó carga de los servidores activos.")

    def atender_cola(self):
        atendidas = 0
        pendientes = len(self.cola)

        for _ in range(pendientes):
            clave_cliente, grupo = self.cola.popleft()
            servidor = self.balanceador.elegir_servidor(self.servidores, grupo)

            if servidor is None:
                self.cola.append((clave_cliente, grupo))
            else:
                servidor.recibir_solicitud()
                self.solicitudes_procesadas += 1
                atendidas += 1

        self.eventos.append(f"Se atendieron {atendidas} solicitudes desde la cola.")

    def disponibilidad_efectiva(self):
        """
        Disponibilidad sobre solicitudes que sí entraron al sistema.
        Las solicitudes limitadas no cuentan como caída, porque fueron bloqueadas
        intencionalmente por política de API key.
        """
        solicitudes_permitidas = self.solicitudes_generadas - self.solicitudes_limitadas

        if solicitudes_permitidas <= 0:
            return 100.0

        return (self.solicitudes_procesadas / solicitudes_permitidas) * 100

    def cliente_mayor_consumo(self):
        return max(self.consumo_por_cliente, key=self.consumo_por_cliente.get)

    def exportar_reporte(self):
        with open("reporte_resultados.csv", "w", newline="", encoding="utf-8") as archivo:
            writer = csv.writer(archivo)

            writer.writerow(["Métrica", "Valor"])
            writer.writerow(["Solicitudes generadas", self.solicitudes_generadas])
            writer.writerow(["Solicitudes procesadas", self.solicitudes_procesadas])
            writer.writerow(["Solicitudes en cola", len(self.cola)])
            writer.writerow(["Solicitudes limitadas por API key", self.solicitudes_limitadas])
            writer.writerow(["Disponibilidad efectiva (%)", round(self.disponibilidad_efectiva(), 2)])
            writer.writerow(["Cliente con mayor consumo", self.cliente_mayor_consumo()])
            writer.writerow([])
            writer.writerow(["Servidor", "Grupo", "Estado", "Carga", "Capacidad"])

            for servidor in self.servidores:
                writer.writerow([
                    servidor.nombre,
                    servidor.grupo,
                    servidor.estado,
                    servidor.carga,
                    servidor.capacidad
                ])

        self.eventos.append("Reporte exportado como reporte_resultados.csv.")

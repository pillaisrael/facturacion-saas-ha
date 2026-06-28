import random
import csv
from servidor import Servidor
from balanceador import Balanceador


class Simulador:
    """
    Controla todo el experimento:
    servidores, facturas, cola, fallos y resultados.
    """

    def __init__(self):
        self.servidores = [
            Servidor("Servidor 1", 100),
            Servidor("Servidor 2", 100),
            Servidor("Servidor 3", 100)
        ]

        self.balanceador = Balanceador()

        self.facturas_generadas = 0
        self.facturas_procesadas = 0
        self.facturas_en_cola = 0

        self.eventos = ["Experimento iniciado correctamente."]

    def generar_facturas(self, cantidad):
        procesadas = 0
        en_cola = 0

        for i in range(cantidad):
            self.facturas_generadas += 1

            servidor = self.balanceador.elegir_servidor(self.servidores)

            if servidor is None:
                self.facturas_en_cola += 1
                en_cola += 1
            else:
                servidor.recibir_factura()
                self.facturas_procesadas += 1
                procesadas += 1

        self.eventos.append(
            f"Se generaron {cantidad} facturas. Procesadas: {procesadas}. En cola: {en_cola}."
        )

    def ataque_ddos(self):
        self.eventos.append("Ataque DDoS simulado: ingreso masivo de facturas.")
        self.generar_facturas(250)

    def caer_servidor(self):
        activos = []

        for servidor in self.servidores:
            if servidor.estado == "Activo":
                activos.append(servidor)

        if len(activos) == 0:
            self.eventos.append("Todos los servidores están caídos.")
            return

        servidor_elegido = random.choice(activos)
        servidor_elegido.caer()

        self.eventos.append(f"{servidor_elegido.nombre} sufrió una caída.")

    def recuperar_servidor(self):
        caidos = []

        for servidor in self.servidores:
            if servidor.estado == "Caído":
                caidos.append(servidor)

        if len(caidos) == 0:
            self.eventos.append("No hay servidores caídos para recuperar.")
            return

        servidor_elegido = random.choice(caidos)
        servidor_elegido.recuperar()

        self.eventos.append(f"{servidor_elegido.nombre} fue recuperado.")

    def liberar_carga(self):
        for servidor in self.servidores:
            servidor.liberar_carga(30)

        self.eventos.append("Se liberó carga de los servidores activos.")

    def atender_cola(self):
        atendidas = 0
        pendientes = self.facturas_en_cola

        for i in range(pendientes):
            servidor = self.balanceador.elegir_servidor(self.servidores)

            if servidor is None:
                break

            servidor.recibir_factura()
            self.facturas_procesadas += 1
            self.facturas_en_cola -= 1
            atendidas += 1

        self.eventos.append(f"Se atendieron {atendidas} facturas desde la cola.")

    def disponibilidad(self):
        if self.facturas_generadas == 0:
            return 100

        return (self.facturas_procesadas / self.facturas_generadas) * 100

    def exportar_reporte(self):
        with open("reporte_resultados.csv", "w", newline="", encoding="utf-8") as archivo:
            writer = csv.writer(archivo)

            writer.writerow(["Métrica", "Valor"])
            writer.writerow(["Facturas generadas", self.facturas_generadas])
            writer.writerow(["Facturas procesadas", self.facturas_procesadas])
            writer.writerow(["Facturas en cola", self.facturas_en_cola])
            writer.writerow(["Disponibilidad (%)", round(self.disponibilidad(), 2)])
            writer.writerow([])

            writer.writerow(["Servidor", "Estado", "Carga", "Capacidad"])

            for servidor in self.servidores:
                writer.writerow([
                    servidor.nombre,
                    servidor.estado,
                    servidor.carga,
                    servidor.capacidad
                ])

        self.eventos.append("Reporte exportado como reporte_resultados.csv.")

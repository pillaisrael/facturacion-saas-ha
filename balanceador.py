# -*- coding: utf-8 -*-

class Balanceador:
    """
    Decide a qué servidor enviar cada solicitud.
    Estrategia: elegir el servidor activo con menor carga dentro del grupo solicitado.
    """

    def elegir_servidor(self, servidores, grupo):
        disponibles = []

        for servidor in servidores:
            if servidor.grupo == grupo and servidor.puede_recibir():
                disponibles.append(servidor)

        if len(disponibles) == 0:
            return None

        return min(disponibles, key=lambda servidor: servidor.carga)

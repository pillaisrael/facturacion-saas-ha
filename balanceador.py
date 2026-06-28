class Balanceador:
    """
    El balanceador decide a qué servidor enviar cada factura.
    En este caso usa una regla simple:
    enviar al servidor activo con menor carga.
    """

    def elegir_servidor(self, servidores):
        disponibles = []

        for servidor in servidores:
            if servidor.puede_recibir():
                disponibles.append(servidor)

        if len(disponibles) == 0:
            return None

        return min(disponibles, key=lambda servidor: servidor.carga)

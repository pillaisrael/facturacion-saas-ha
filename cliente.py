# -*- coding: utf-8 -*-

class Cliente:
    """
    Representa a un cliente de la empresa SaaS.
    Cada cliente tiene un tipo, una API key y un límite permitido por ciclo.
    """

    def __init__(self, nombre, tipo, api_key, limite_por_ciclo, critico=False):
        self.nombre = nombre
        self.tipo = tipo
        self.api_key = api_key
        self.limite_por_ciclo = limite_por_ciclo
        self.critico = critico

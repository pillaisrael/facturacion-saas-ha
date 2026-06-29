# -*- coding: utf-8 -*-

class LimitadorAPI:
    """
    Aplica rate limiting por API key.
    Sirve para evitar que un solo cliente consuma toda la infraestructura compartida.
    """

    def __init__(self):
        self.activo = False

    def activar(self):
        self.activo = True

    def desactivar(self):
        self.activo = False

    def aplicar_limite(self, cliente, cantidad):
        """
        Retorna dos valores:
        - permitidas: solicitudes que sí pueden entrar al sistema.
        - limitadas: solicitudes bloqueadas por exceder el límite del cliente.
        """
        if not self.activo:
            return cantidad, 0

        permitidas = min(cantidad, cliente.limite_por_ciclo)
        limitadas = cantidad - permitidas
        return permitidas, limitadas

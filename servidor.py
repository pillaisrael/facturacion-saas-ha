class Servidor:
    """
    Representa un servidor de la empresa SaaS.
    Cada servidor puede estar Activo o Caído.
    """

    def __init__(self, nombre, capacidad):
        self.nombre = nombre
        self.capacidad = capacidad
        self.carga = 0
        self.estado = "Activo"

    def puede_recibir(self):
        return self.estado == "Activo" and self.carga < self.capacidad

    def recibir_factura(self):
        if self.puede_recibir():
            self.carga += 1
            return True
        return False

    def caer(self):
        self.estado = "Caído"
        self.carga = 0

    def recuperar(self):
        self.estado = "Activo"
        self.carga = 0

    def liberar_carga(self, cantidad):
        if self.estado == "Activo":
            self.carga = max(0, self.carga - cantidad)

    def porcentaje_carga(self):
        return (self.carga / self.capacidad) * 100

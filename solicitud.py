class Solicitud:
    def __init__(self, cliente, tipo_solicitado):
        self.cliente = cliente
        self.tipo_solicitado = tipo_solicitado

    def __str__(self):
        return (
            f"Cliente: {self.cliente} | "
            f"Solicita: {self.tipo_solicitado}"
        )
class Vehiculo:
    def __init__(self, codigo, modelo, tipo, precio):
        self.codigo = codigo
        self.modelo = modelo
        self.tipo = tipo
        self.precio = precio
        self.disponible = True

    def __str__(self):
        estado = "Disponible" if self.disponible else "Ocupado"
        return (
            f"[{self.codigo}] {self.modelo} | "
            f"Tipo: {self.tipo} | "
            f"Precio: S/. {self.precio} | "
            f"{estado}"
        )
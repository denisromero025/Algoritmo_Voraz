import itertools
class Vehiculo:
    """Representa una unidad de la flota de alquiler."""

    def __init__(self, id_vehiculo, placa, tipo, modelo, tarifa_diaria):
        self.id_vehiculo = id_vehiculo
        self.placa = placa
        self.tipo = tipo                    # Económico / Sedán / SUV
        self.modelo = modelo
        self.tarifa_diaria = tarifa_diaria
        self.disponible = True
    def __repr__(self):
        return f"Vehiculo({self.placa}, {self.tipo}, S/{self.tarifa_diaria})"
class Solicitud:
    """solicitud de alquiler hecha por un cliente."""
    _contador = itertools.count(1)
    def __init__(self, cliente, tipo_solicitado, monto_ofrecido):
        self.id_solicitud = next(Solicitud._contador)
        self.cliente = cliente
        self.tipo_solicitado = tipo_solicitado
        self.monto_ofrecido = monto_ofrecido
        self.estado = "Pendiente"           # Pendiente / Atendida / No atendida
        self.vehiculo_asignado = None
    def __repr__(self):
        return f"Solicitud(#{self.id_solicitud}, {self.cliente}, {self.tipo_solicitado}, S/{self.monto_ofrecido})"

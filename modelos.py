    
"""
Representa un vehículo de la flota.
"""
class Vehiculo:

    def __init__(self, id, placa, tipo, modelo, tarifa):
        self.id = id
        self.placa = placa
        self.tipo = tipo
        self.modelo = modelo
        self.tarifa = tarifa  # Tarifa por día
        self.disponible = True

class Solicitud:
    """
    Representa la solicitud de alquiler realizada por un cliente.
    """
    contador = 1

    def __init__(self, cliente, tipo_solicitado, dias, presupuesto_diario):
        self.id_solicitud = Solicitud.contador
        Solicitud.contador += 1

        self.cliente = cliente
        self.tipo_solicitado = tipo_solicitado
        self.dias = dias
        self.presupuesto_diario = presupuesto_diario

        self.estado = "Pendiente"
        self.vehiculo_asignado = None

        # Motivo cuando la solicitud queda "No atendida"
        # Valores posibles: None, "sin_stock", "presupuesto_insuficiente"
        self.motivo_no_atendida = None
        # Tarifa mínima encontrada del tipo solicitado (aunque exceda presupuesto)
        self.tarifa_minima_tipo = None

    @property
    def costo_total(self):
        """
        Retorna el costo total del alquiler.
        """
        if self.vehiculo_asignado:
            return self.vehiculo_asignado.tarifa * self.dias
        return 0

    @property
    def diferencia_diaria(self):
        """
        Excedente diario no gastado del presupuesto del cliente
        respecto a la tarifa del vehículo asignado.
        """
        if self.vehiculo_asignado:
            return self.presupuesto_diario - self.vehiculo_asignado.tarifa
        return 0

    @property
    def diferencia_total(self):
        """
        Excedente total no gastado durante todos los días de alquiler.
        """
        return self.diferencia_diaria * self.dias
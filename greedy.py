from vehiculo import Vehiculo
from solicitud import Solicitud


def algoritmo_voraz(vehiculos, solicitudes):

    asignaciones = []

    ingreso_total = 0

    for solicitud in solicitudes:

        mejor_vehiculo = None

        for vehiculo in vehiculos:

            if (
                vehiculo.disponible
                and vehiculo.tipo == solicitud.tipo_solicitado
            ):

                if (
                    mejor_vehiculo is None
                    or vehiculo.precio > mejor_vehiculo.precio
                ):

                    mejor_vehiculo = vehiculo

        if mejor_vehiculo is not None:

            mejor_vehiculo.disponible = False

            ingreso_total += mejor_vehiculo.precio

            asignaciones.append(
                (
                    solicitud.cliente,
                    mejor_vehiculo.modelo,
                    mejor_vehiculo.precio
                )
            )

    return asignaciones, ingreso_total
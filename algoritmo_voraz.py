"""
ALGORITMO VORAZ con priorización por ingreso total
"""
import time

def asignar_solicitudes_voraz(vehiculos, solicitudes):

    inicio = time.perf_counter()

    asignaciones = []
    no_atendidas = []

    pendientes = [
        s for s in solicitudes
        if s.estado == "Pendiente"
    ]

    # 1. Generar todas las combinaciones válidas
    combinaciones = []
    for solicitud in pendientes:
        for vehiculo in vehiculos:
            if (
                vehiculo.disponible
                and vehiculo.tipo == solicitud.tipo_solicitado
                and vehiculo.tarifa <= solicitud.presupuesto_diario
            ):
                ingreso = vehiculo.tarifa * solicitud.dias
                combinaciones.append((solicitud, vehiculo, ingreso))

    # 2. Ordenar por ingreso total
    combinaciones.sort(
        key=lambda c: (-c[2], -c[1].tarifa, -c[0].dias, c[0].id_solicitud, c[1].id)
    )

    # 3. Asignación voraz: se recorre la lista de combinaciones y se asigna el vehículo
    solicitudes_atendidas_ids = set()
    conflictos_resueltos = 0
    ingreso_perdido_por_conflicto = 0

    for solicitud, vehiculo, ingreso in combinaciones:
        if solicitud.id_solicitud in solicitudes_atendidas_ids:
            continue
        if not vehiculo.disponible:
            # Este vehículo ya fue tomado por otra solicitud con mayor
            # ingreso: se contabiliza como conflicto resuelto.
            conflictos_resueltos += 1
            ingreso_perdido_por_conflicto += ingreso
            continue

        vehiculo.disponible = False
        solicitud.estado = "Atendida"
        solicitud.vehiculo_asignado = vehiculo
        solicitud.motivo_no_atendida = None

        asignaciones.append(
            (solicitud, vehiculo, ingreso, solicitud.diferencia_total)
        )
        solicitudes_atendidas_ids.add(solicitud.id_solicitud)

    # 4. Solicitudes que quedaron sin vehículo
    for solicitud in pendientes:
        if solicitud.id_solicitud in solicitudes_atendidas_ids:
            continue

        solicitud.estado = "No atendida"

        vehiculos_del_tipo = [
            v for v in vehiculos if v.tipo == solicitud.tipo_solicitado
        ]

        if not vehiculos_del_tipo:
            solicitud.motivo_no_atendida = "sin_stock"
            solicitud.tarifa_minima_tipo = None
        else:
            disponibles = [v for v in vehiculos_del_tipo if v.disponible]
            if disponibles:
                solicitud.motivo_no_atendida = "presupuesto_insuficiente"
                solicitud.tarifa_minima_tipo = min(v.tarifa for v in disponibles)
            else:
                solicitud.motivo_no_atendida = "sin_stock"
                solicitud.tarifa_minima_tipo = min(
                    v.tarifa for v in vehiculos_del_tipo
                )
        no_atendidas.append(solicitud)
    fin = time.perf_counter()

    return (
        asignaciones,
        no_atendidas,
        fin - inicio,
        conflictos_resueltos,
        ingreso_perdido_por_conflicto
    )
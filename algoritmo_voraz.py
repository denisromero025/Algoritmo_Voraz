"""
ALGORITMO VORAZ (GREEDY) 
Funcionamiento:
-Se ordenan TODAS las solicitudes pendientes de mayor a menor monto
    ofrecido (criterio de selección local: maximizar el ingresoinmediato de cada asignación).
-Para cada solicitud, en ese orden, se busca -entre los vehículos disponibles del tipo solicitado- el de MENOR tarifa diaria, para
    reservar los vehículos de mayor tarifa a solicitudes aún no evaluadas (heurística de eficiencia de flota).
-Si no existe un vehículo disponible del tipo pedido, la solicitud queda como NO ATENDIDA.
-La decisión tomada en cada paso NUNCA se revisa ni se deshace
"""

import time

def asignar_solicitudes_voraz(vehiculos, solicitudes):

    inicio = time.perf_counter()
    # Paso 1 (elección voraz global): ordenar por monto ofrecido descendente.
    pendientes = [s for s in solicitudes if s.estado == "Pendiente"]
    pendientes_ordenadas = sorted(
        pendientes, key=lambda s: s.monto_ofrecido, reverse=True
    )
    asignaciones = []
    no_atendidas = []
    for solicitud in pendientes_ordenadas:
        # Paso 2: entre los vehículos disponibles del tipo solicitado,
        # elegir el de menor tarifa (decisión local, sin retroceso).
        candidatos = [
            v for v in vehiculos
            if v.disponible and v.tipo == solicitud.tipo_solicitado
        ]
        if candidatos:
            vehiculo_elegido = min(candidatos, key=lambda v: v.tarifa_diaria)
            vehiculo_elegido.disponible = False
            solicitud.estado = "Atendida"
            solicitud.vehiculo_asignado = vehiculo_elegido
            asignaciones.append((solicitud, vehiculo_elegido))
        else:
            solicitud.estado = "No atendida"
            no_atendidas.append(solicitud)
    fin = time.perf_counter()
    tiempo_ejecucion = fin - inicio
    return asignaciones, no_atendidas, tiempo_ejecucion

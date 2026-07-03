from vehiculo import Vehiculo
from solicitud import Solicitud
from greedy import algoritmo_voraz

# FLOTA DE VEHICULOS 
vehiculos = [

    Vehiculo(1, "Toyota Yaris", "Economico", 120),
    Vehiculo(2, "Kia Rio", "Economico", 100),
    Vehiculo(3, "Hyundai Accent", "Economico", 110),

    Vehiculo(4, "Toyota Corolla", "Sedan", 180),
    Vehiculo(5, "Mazda 3", "Sedan", 170),

    Vehiculo(6, "BMW X3", "SUV", 260),
    Vehiculo(7, "Mazda CX5", "SUV", 230)

]
# SOLICITUDES
solicitudes = [

    Solicitud("Luis", "Economico"),
    Solicitud("Ana", "SUV"),
    Solicitud("Carlos", "Sedan"),
    Solicitud("Maria", "Economico"),
    Solicitud("Pedro", "SUV")

]

print("      FLOTA DISPONIBLE       ")

for vehiculo in vehiculos:
    print(vehiculo)

print()

print("      SOLICITUDES    ")

for solicitud in solicitudes:
    print(solicitud)

print("\n        EJECUTANDO ALGORITMO VORAZ       ")

asignaciones, ingreso_total = algoritmo_voraz(vehiculos, solicitudes)

print("\nAsignaciones realizadas:\n")

for cliente, vehiculo, precio in asignaciones:
    print(f"Cliente: {cliente}")
    print(f"Vehículo asignado: {vehiculo}")
    print(f"Ingreso: S/. {precio}")
    print("-" * 40)

print(f"\nIngreso total obtenido: S/. {ingreso_total}")
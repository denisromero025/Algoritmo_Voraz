from modelos import Vehiculo
TIPOS_VEHICULO = ["Económico", "Sedán", "SUV"]
def crear_flota_inicial():
    """Genera y retorna la lista de vehículos predefinidos del sistema."""
    datos = [
        ("V01", "ECO-101", "Económico", "Toyota Yaris",   80.0),
        ("V02", "ECO-102", "Económico", "Hyundai i10",    75.0),
        ("V03", "ECO-103", "Económico", "Kia Picanto",    78.0),
        ("V04", "ECO-104", "Económico", "Suzuki Swift",   82.0),
        ("V05", "SED-201", "Sedán",     "Toyota Corolla", 120.0),
        ("V06", "SED-202", "Sedán",     "Nissan Sentra",  115.0),
        ("V07", "SED-203", "Sedán",     "Hyundai Elantra",118.0),
        ("V08", "SED-204", "Sedán",     "Kia Cerato",     122.0),
        ("V09", "SUV-301", "SUV",       "Toyota RAV4",    180.0),
        ("V10", "SUV-302", "SUV",       "Hyundai Tucson", 175.0),
        ("V11", "SUV-303", "SUV",       "Kia Sportage",   178.0),
        ("V12", "SUV-304", "SUV",       "Honda CR-V",     185.0),
    ]
    return [Vehiculo(*d) for d in datos]

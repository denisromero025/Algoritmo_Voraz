from modelos import Vehiculo

TIPOS_VEHICULO = [
    "Económico",
    "Sedán",
    "SUV",
    "Pickup",
    "Híbrido",
    "Van",
    "Eléctrico"
]

def cargar_flota():

    return [

        # ECONÓMICOS
        Vehiculo(1, "ABC-101", "Económico", "Toyota Yaris", 90),
        Vehiculo(2, "ABC-102", "Económico", "Kia Picanto", 100),
        Vehiculo(3, "ABC-103", "Económico", "Hyundai Grand i10", 110),
        Vehiculo(4, "ABC-104", "Económico", "Chevrolet Spark", 120),

        # SEDÁN
        Vehiculo(5, "ABC-105", "Sedán", "Toyota Corolla", 140),
        Vehiculo(6, "ABC-106", "Sedán", "Hyundai Elantra", 150),
        Vehiculo(7, "ABC-107", "Sedán", "Mazda 3", 160),
        Vehiculo(8, "ABC-108", "Sedán", "Honda Civic", 170),

        # SUV
        Vehiculo(9, "ABC-109", "SUV", "Hyundai Creta", 180),
        Vehiculo(10, "ABC-110", "SUV", "Toyota Raize", 200),
        Vehiculo(11, "ABC-111", "SUV", "Kia Sportage", 220),
        Vehiculo(12, "ABC-112", "SUV", "Toyota RAV4", 240),

        # PICKUP
        Vehiculo(13, "ABC-113", "Pickup", "Toyota Hilux", 260),
        Vehiculo(14, "ABC-114", "Pickup", "Ford Ranger", 280),
        Vehiculo(15, "ABC-115", "Pickup", "Nissan Frontier", 300),

        # HÍBRIDOS
        Vehiculo(16, "ABC-116", "Híbrido", "Toyota Prius", 210),
        Vehiculo(17, "ABC-117", "Híbrido", "Corolla Hybrid", 230),

        # VAN
        Vehiculo(18, "ABC-118", "Van", "Hyundai Staria", 320),
        Vehiculo(19, "ABC-119", "Van", "Toyota Hiace", 350),

        # ELÉCTRICO
        Vehiculo(20, "ABC-120", "Eléctrico", "Tesla Model 3", 400)
    ]
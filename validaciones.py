from flota import TIPOS_VEHICULO

def validar_solicitud(cliente, tipo, monto_texto):
    cliente = cliente.strip()
    if not cliente:
        return False, "El nombre del cliente no puede estar vacío.", None
    if any(ch.isdigit() for ch in cliente):
        return False, "El nombre del cliente no debe contener números.", None
    if tipo not in TIPOS_VEHICULO:
        return False, "Debe seleccionar un tipo de vehículo válido.", None
    monto_texto = monto_texto.strip().replace(",", ".")
    try:
        monto = float(monto_texto)
    except ValueError:
        return False, "El monto ofrecido debe ser un número válido.", None
    if monto <= 0:
        return False, "El monto ofrecido debe ser mayor a 0.", None
    return True, "", monto

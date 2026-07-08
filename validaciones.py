def validar_nombre(nombre):
    """
    Valida el nombre del cliente.
    """
    nombre = nombre.strip()
    if not nombre:
        return False, "Ingrese el nombre del cliente."
    if any(caracter.isdigit() for caracter in nombre):
        return False, "El nombre no debe contener números."
    return True, ""

def validar_dias(dias):
    """
    Valida la cantidad de días de alquiler.
    """
    try:
        dias = int(dias)

        if dias <= 0:
            return False, "Los días de alquiler deben ser mayores a cero."

        return True, ""
    except ValueError:
        return False, "Ingrese una cantidad válida de días."

def validar_presupuesto(presupuesto):
    """
    Valida el presupuesto diario.
    """
    try:
        presupuesto = float(presupuesto)

        if presupuesto <= 0:
            return False, "El presupuesto debe ser mayor a cero."

        return True, ""
    except ValueError:
        return False, "Ingrese un presupuesto válido."
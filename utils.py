"""
Modulo: utils.py
    Funciones auxiliares como validaciones y formatos.
Autor: Imanol G. de E.
Fecha: Julio 2025
"""

def pedir_monto_validado():
    """
    Pide un monto al usuario hasta que introduzca un número válido.
    Devuelve el número como float.
    """
    while True:
        entrada = input("Monto (€): ").strip()

        if es_float_valido(entrada):
            return float(entrada)
        else:
            print("❌ Entrada no válida. Introduce un número con punto decimal.")

            
def es_float_valido(texto):
    """
    Devuelve True si el texto se puede convertir a float, False si no.
    """
    try:
        float(texto)
        return True
    except ValueError:
        return False




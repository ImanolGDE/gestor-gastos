import os
import shutil
from datetime import datetime


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

def pedir_fecha_valida():
    """
    Pide una fecha al usuario. Si está vacía, se usa la fecha de hoy.
    Si se introduce una fecha inválida, vuelve a pedirla.
    """
    while True:
        entrada = input("Fecha (YYYY-MM-DD) [hoy por defecto]: ").strip()
        if entrada == "":
            return datetime.today().strftime('%Y-%m-%d')
        try:
            # Validar si la fecha es válida
            datetime.strptime(entrada, "%Y-%m-%d")
            return entrada
        except ValueError:
            print("❌ Fecha no válida. Debe tener formato YYYY-MM-DD y ser una fecha real.")

def hacer_backup(fichero):
    """
    Crea una copia de seguridad del fichero CSV en la carpeta backups/
    con la fecha y hora actuales.
    """
    if not os.path.exists("backups"):
        os.makedirs("backups")

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre_backup = f"backups/gastos_{timestamp}.csv"
    shutil.copyfile(fichero, nombre_backup)
    print(f"💾 Copia de seguridad creada: {nombre_backup}")


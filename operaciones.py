import csv
import os
from datetime import datetime

from utils import (
    pedir_monto_validado, 
    pedir_fecha_valida,
    hacer_backup
    )

FICHERO = "gastos.csv"
CAMPOS = ["fecha", "etiquetas", "monto", "comentario"]

def añadir_gasto():
    
    '''
    fecha = input("Fecha (YYYY-MM-DD) [hoy por defecto]: ").strip()
    if fecha == "":
        fecha = datetime.today().strftime('%Y-%m-%d')
    '''
    fecha = pedir_fecha_valida()

    etiquetas = input("Etiquetas (separadas por coma): ").strip().upper()
    # monto = input("Monto (€): ").strip()
    # monto = pedir_float_valido("Monto (€): ")
    monto = pedir_monto_validado()
    comentario = input("Comentario (opcional): ").strip()

    with open(FICHERO, mode="a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CAMPOS)
        writer.writerow({
            "fecha": fecha,
            "etiquetas": etiquetas,
            "monto": f"{monto:.2f}",
            "comentario": comentario
        })

def ver_gastos():
    with open(FICHERO, mode="r") as f:
        reader = csv.DictReader(f)
        gastos = list(reader)

    if not gastos:
        print("⚠️ No hay gastos registrados.")
        return

    print("\n📋 Lista de gastos:")
    for fila in gastos:
        print(f'{fila["fecha"]} - {fila["etiquetas"]} - {fila["monto"]}€ - {fila["comentario"]}')

def resumen_por_etiqueta(fichero):
    """
    Muestra un resumen del total gastado por cada etiqueta individual.
    Soporta múltiples etiquetas por gasto.
    """
    resumen = {}

    with open(fichero, mode="r") as f:
        reader = csv.DictReader(f)
        for fila in reader:
            try:
                monto = float(fila["monto"])
                etiquetas = [e.strip().lower() for e in fila["etiquetas"].split(",")]
                for etiqueta in etiquetas:
                    resumen[etiqueta] = resumen.get(etiqueta, 0) + monto
            except ValueError:
                print(f"⚠️ Gasto inválido ignorado: {fila}")

    if resumen:
        print("\n📊 Resumen por etiqueta:")
        for etiqueta, total in resumen.items():
            print(f"• {etiqueta}: {total:.2f} €")
    else:
        print("⚠️ No hay gastos válidos registrados.")

def buscar_gastos_por_palabra(fichero, palabra):
    """
    Muestra todos los gastos que contienen la palabra indicada
    en la categoría o comentario (no distingue mayúsculas).
    """
    palabra = palabra.lower()
    resultados = []

    with open(fichero, mode="r") as f:
        reader = csv.DictReader(f)
        for fila in reader:
            etiquetas = fila["etiquetas"].lower()
            comentario = fila["comentario"].lower()
            if palabra in etiquetas or palabra in comentario:
                resultados.append(fila)

    if resultados:
        print(f"\n🔍 Resultados para '{palabra}':")
        for fila in resultados:
            print(f'{fila["fecha"]} - {fila["categoria"]} - {fila["monto"]}€ - {fila["comentario"]}')
    else:
        print(f"❌ No se encontraron gastos que contengan '{palabra}'.")

def buscar_gastos_por_etiqueta(fichero, etiqueta):
    """
    Muestra todos los gastos que contengan una etiqueta específica.
    La comparación no distingue mayúsculas/minúsculas.
    """
    etiqueta = etiqueta.lower().strip()
    resultados = []

    with open(fichero, mode="r") as f:
        reader = csv.DictReader(f)
        for fila in reader:
            etiquetas = [e.strip().lower() for e in fila["etiquetas"].split(",")]
            if etiqueta in etiquetas:
                resultados.append(fila)

    if resultados:
        print(f"\n🏷️ Resultados para la etiqueta '{etiqueta}':")
        for fila in resultados:
            print(f'{fila["fecha"]} - {fila["etiquetas"]} - {fila["monto"]}€ - {fila["comentario"]}')
    else:
        print(f"❌ No se encontraron gastos con la etiqueta '{etiqueta}'.")

def eliminar_gasto(fichero):
    """
    Muestra los gastos con índice y permite eliminar uno.
    """
    gastos = []

    with open(fichero, mode="r") as f:
        reader = csv.DictReader(f)
        for fila in reader:
            gastos.append(fila)

    if not gastos:
        print("⚠️ No hay gastos registrados.")
        return

    print("\nGastos registrados:")
    for i, g in enumerate(gastos):
        print(f"{i + 1}. {g['fecha']} - {g['etiquetas']} - {g['monto']}€ - {g['comentario']}")

    try:
        indice = int(input("\nIntroduce el número del gasto a eliminar: ")) - 1
        if 0 <= indice < len(gastos):
            hacer_backup(fichero)
            eliminado = gastos.pop(indice)

            with open(fichero, mode="w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["fecha", "etiquetas", "monto", "comentario"])
                writer.writeheader()
                writer.writerows(gastos)

            print(f"✅ Gasto eliminado: {eliminado['fecha']} - {eliminado['etiquetas']}")
        else:
            print("❌ Índice fuera de rango.")
    except ValueError:
        print("❌ Entrada no válida. Debe ser un número.")

def limpiar_gastos(fichero):
    """
    Borra todos los registros del archivo de gastos (mantiene cabecera).
    """
    confirmar = input("¿Estás seguro de que quieres borrar todos los gastos? (s/n): ").strip().lower()

    if confirmar == "s":
        hacer_backup(fichero)
        with open(fichero, mode="w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["fecha", "etiquetas", "monto", "comentario"])
            writer.writeheader()
        print("🧼 Todos los gastos han sido eliminados.")
    else:
        print("❎ Acción cancelada.")

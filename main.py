import csv
import os
from datetime import datetime

from utils import pedir_monto_validado
from operaciones import eliminar_gasto, limpiar_gastos

FICHERO = "gastos.csv"
CAMPOS = ["fecha", "categoria", "monto", "comentario"]

def inicializar_fichero():
    if not os.path.exists(FICHERO):
        with open(FICHERO, mode="w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=CAMPOS)
            writer.writeheader()

def añadir_gasto():
    fecha = input("Fecha (YYYY-MM-DD) [hoy por defecto]: ").strip()
    if fecha == "":
        fecha = datetime.today().strftime('%Y-%m-%d')

    categoria = input("Categoría: ").strip()
    # monto = input("Monto (€): ").strip()
    # monto = pedir_float_valido("Monto (€): ")
    monto = pedir_monto_validado()
    comentario = input("Comentario (opcional): ").strip()

    with open(FICHERO, mode="a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CAMPOS)
        writer.writerow({
            "fecha": fecha,
            "categoria": categoria,
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
        print(f'{fila["fecha"]} - {fila["categoria"]} - {fila["monto"]}€ - {fila["comentario"]}')

def resumen_por_categoria():
    resumen = {}
    errores = 0

    with open(FICHERO, mode="r") as f:
        reader = csv.DictReader(f)
        for fila in reader:
            cat = fila["categoria"]
            try:
                monto = float(fila["monto"])
                resumen[cat] = resumen.get(cat, 0) + monto
            except ValueError:
                errores += 1
                print(f"⚠️ Gasto con monto no válido ignorado: {fila}")

    print("\n📊 Resumen por categoría:")
    for cat, total in resumen.items():
        print(f"• {cat}: {total:.2f} €")

    if errores > 0:
        print(f"\n❗ Se ignoraron {errores} gasto(s) con montos inválidos.")

def menu():
    while True:
        print("\nGestor de Gastos")
        print("1. Añadir gasto")
        print("2. Ver todos los gastos")
        print("3. Ver resumen por categoría")
        print("4. Eliminar gasto")
        print("5. Limpiar todos los gastos")
        print("6. Salir")


        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            añadir_gasto()
        elif opcion == "2":
            ver_gastos()
        elif opcion == "3":
            resumen_por_categoria()
        elif opcion == "4":
            eliminar_gasto(FICHERO)
        elif opcion == "5":
            limpiar_gastos(FICHERO)
        elif opcion == "6":
            break
        else:
            print("Opción no válida")

if __name__ == "__main__":
    inicializar_fichero()
    menu()

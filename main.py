import os 
import csv

from operaciones import (
    añadir_gasto,
    ver_gastos,
    resumen_por_etiqueta,
    eliminar_gasto,
    limpiar_gastos,
    buscar_gastos_por_palabra,
    buscar_gastos_por_etiqueta
)


FICHERO = "gastos.csv"
CAMPOS = ["fecha", "etiquetas", "monto", "comentario"]

def inicializar_fichero():
    if not os.path.exists(FICHERO):
        with open(FICHERO, mode="w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=CAMPOS)
            writer.writeheader()

def menu():
    while True:
        print("\nGestor de Gastos")
        print("1. Añadir gasto")
        print("2. Ver todos los gastos")
        print("3. Ver resumen por etiqueta")
        print("4. Buscar gastos por palabra")
        print("5. Buscar gastos por etiqueta")
        print("6. Eliminar gasto")
        print("7. Limpiar todos los gastos")
        print("8. Salir")


        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            añadir_gasto()
        elif opcion == "2":
            ver_gastos()
        elif opcion == "3":
            resumen_por_etiqueta(FICHERO)
        elif opcion == "4":
            palabra = input("Introduce una palabra a buscar: ").strip()
            buscar_gastos_por_palabra(FICHERO, palabra)
        elif opcion == "5":
            etiqueta = input("Introduce una etiqueta a buscar: ").strip()
            buscar_gastos_por_etiqueta(FICHERO, etiqueta)
        elif opcion == "6":
            eliminar_gasto(FICHERO)
        elif opcion == "7":
            limpiar_gastos(FICHERO)
        elif opcion == "8":
            break
        else:
            print("Opción no válida")

if __name__ == "__main__":
    inicializar_fichero()
    menu()

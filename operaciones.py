import csv


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
        print(f"{i + 1}. {g['fecha']} - {g['categoria']} - {g['monto']}€ - {g['comentario']}")

    try:
        indice = int(input("\nIntroduce el número del gasto a eliminar: ")) - 1
        if 0 <= indice < len(gastos):
            eliminado = gastos.pop(indice)

            with open(fichero, mode="w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["fecha", "categoria", "monto", "comentario"])
                writer.writeheader()
                writer.writerows(gastos)

            print(f"✅ Gasto eliminado: {eliminado['fecha']} - {eliminado['categoria']}")
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
        with open(fichero, mode="w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["fecha", "categoria", "monto", "comentario"])
            writer.writeheader()
        print("🧼 Todos los gastos han sido eliminados.")
    else:
        print("❎ Acción cancelada.")

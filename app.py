import tkinter as tk
import os, csv
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

from operaciones import leer_gastos, añadir_gasto, limpiar_gastos
from utils import pedir_fecha_valida, hacer_backup

FICHERO = "gastos.csv"

# --- FUNCIONES INTERMEDIAS PARA LA GUI ---

def inicializar_csv(fichero):
    if not os.path.exists(fichero):
        with open(fichero, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["fecha", "etiquetas", "monto", "comentario"])


def actualizar_tabla():
    """
    Refresca la tabla con los gastos actuales.
    """
    for fila in tabla.get_children():
        tabla.delete(fila)

    gastos = leer_gastos(FICHERO)
    for gasto in gastos:
        tabla.insert("", tk.END, values=(gasto["fecha"], gasto["etiquetas"], gasto["monto"], gasto["comentario"]))
    
    boton_ver_todo.config(state=tk.DISABLED)


def procesar_guardado():
    """
    Recoge los datos del formulario, valida y guarda el gasto.
    """
    fecha = entry_fecha.get().strip()
    if not fecha:
        fecha = datetime.today().strftime('%Y-%m-%d')

    etiquetas = entry_etiquetas.get().strip()
    monto = entry_monto.get().strip()
    comentario = entry_comentario.get().strip()

    try:
        añadir_gasto(FICHERO, fecha, etiquetas, monto, comentario)
        actualizar_tabla()
        limpiar_formulario()
        messagebox.showinfo("Éxito", "Gasto añadido correctamente.")
    except ValueError as e:
        messagebox.showerror("Error", str(e))


def limpiar_formulario():
    """
    Limpia los campos del formulario.
    """
    entry_fecha.delete(0, tk.END)
    entry_etiquetas.delete(0, tk.END)
    entry_monto.delete(0, tk.END)
    entry_comentario.delete(0, tk.END)
    entry_fecha.insert(0, datetime.today().strftime('%Y-%m-%d'))


def eliminar_gasto_seleccionado():
    seleccion = tabla.selection()
    if not seleccion:
        messagebox.showwarning("Atención", "Selecciona un gasto para eliminar.")
        return

    fila = tabla.item(seleccion[0])["values"]
    fecha, etiquetas, monto, comentario = fila

    confirmar = messagebox.askyesno("Confirmar", f"¿Eliminar el gasto de {monto}€ con etiquetas {etiquetas}?")
    if not confirmar:
        return

    # Leer todos los gastos y filtrar el que coincide exactamente
    gastos = leer_gastos(FICHERO)
    gastos_filtrados = [
        g for g in gastos
        if not (g["fecha"] == fecha and g["etiquetas"] == etiquetas and g["monto"] == str(monto) and g["comentario"] == comentario)
    ]

    # Sobrescribir archivo
    with open(FICHERO, mode="w", newline="") as f:
        import csv
        writer = csv.DictWriter(f, fieldnames=["fecha", "etiquetas", "monto", "comentario"])
        writer.writeheader()
        writer.writerows(gastos_filtrados)

    actualizar_tabla()
    messagebox.showinfo("Hecho", "Gasto eliminado correctamente.")


def eliminar_todos_los_gastos():
    confirmar = messagebox.askyesno(
        "Confirmar", 
        "¿Estás seguro de que quieres eliminar todos los gastos?\nEsta acción no se puede deshacer."
    )
    if not confirmar:
        return

    # Hacer copia de seguridad antes de limpiar (opcional)
    from utils import hacer_backup
    hacer_backup(FICHERO)

    # Borrar todo menos el encabezado
    with open(FICHERO, mode="w", newline="", encoding="utf-8") as f:
        import csv
        writer = csv.DictWriter(f, fieldnames=["fecha", "etiquetas", "monto", "comentario"])
        writer.writeheader()

    actualizar_tabla()
    messagebox.showinfo("Limpieza completada", "Todos los gastos han sido eliminados.")


def restaurar_desde_backup():
    import os
    import shutil

    backups_dir = "backups"
    archivos = sorted(os.listdir(backups_dir), reverse=True)

    if not archivos:
        messagebox.showinfo("Sin backups", "No hay copias de seguridad disponibles.")
        return

    # Crear ventana emergente
    ventana = tk.Toplevel(root)
    ventana.title("Restaurar backup")
    ventana.geometry("400x300")
    ventana.grab_set()  # Bloquea la ventana principal mientras esta esté abierta

    tk.Label(ventana, text="Selecciona un backup para restaurar:").pack(pady=10)

    lista = tk.Listbox(ventana, height=10, width=50)
    for archivo in archivos:
        lista.insert(tk.END, archivo)
    lista.pack(pady=10)

    def confirmar():
        seleccion = lista.curselection()
        if not seleccion:
            messagebox.showwarning("Atención", "Debes seleccionar un backup.")
            return

        archivo_seleccionado = archivos[seleccion[0]]
        ruta_backup = os.path.join(backups_dir, archivo_seleccionado)

        shutil.copy(ruta_backup, FICHERO)
        actualizar_tabla()
        messagebox.showinfo("Backup restaurado", f"Se restauró el backup: {archivo_seleccionado}")
        ventana.destroy()

    tk.Button(ventana, text="Restaurar", command=confirmar).pack(pady=5)
    tk.Button(ventana, text="Cancelar", command=ventana.destroy).pack()


def mostrar_grafico_mensual():
    import matplotlib.pyplot as plt
    from collections import defaultdict
    from operaciones import leer_gastos

    gastos = leer_gastos(FICHERO)

    # Agrupar montos por mes
    totales_por_mes = defaultdict(float)
    for gasto in gastos:
        try:
            fecha_obj = datetime.strptime(gasto["fecha"], "%Y-%m-%d")
            clave_mes = fecha_obj.strftime("%Y-%m")  # ej: "2025-01"
            totales_por_mes[clave_mes] += float(gasto["monto"])
        except Exception as e:
            print(f"Error procesando gasto {gasto}: {e}")

    if not totales_por_mes:
        messagebox.showinfo("Sin datos", "No hay datos suficientes para generar el gráfico.")
        return

    # Ordenar por mes
    meses_ordenados = sorted(totales_por_mes.keys())
    montos = [totales_por_mes[mes] for mes in meses_ordenados]

    # Mostrar gráfico
    plt.figure(figsize=(10, 5))
    plt.bar(meses_ordenados, montos)
    plt.xlabel("Mes")
    plt.ylabel("Total (€)")
    plt.title("Evolución del gasto mensual")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def mostrar_grafico_por_categoria():
    import matplotlib.pyplot as plt
    from collections import defaultdict
    from operaciones import leer_gastos

    gastos = leer_gastos(FICHERO)

    totales_por_categoria = defaultdict(float)

    for gasto in gastos:
        etiquetas = gasto["etiquetas"].upper().replace('"', '').split(", ")
        for etiqueta in etiquetas:
            try:
                totales_por_categoria[etiqueta] += float(gasto["monto"])
            except ValueError:
                print(f"⚠️ Error en gasto: {gasto}")

    if not totales_por_categoria:
        messagebox.showinfo("Sin datos", "No hay datos suficientes para generar el gráfico.")
        return

    categorias = list(totales_por_categoria.keys())
    montos = [totales_por_categoria[c] for c in categorias]

    # Mostrar gráfico tipo pastel
    plt.figure(figsize=(8, 8))
    plt.pie(montos, labels=categorias, autopct="%1.1f%%", startangle=90)
    plt.title("Distribución de gasto por categoría")
    plt.axis("equal")
    plt.tight_layout()
    plt.show()


def buscar_gastos():
    from operaciones import leer_gastos

    # Crear ventana de búsqueda
    ventana = tk.Toplevel(root)
    ventana.title("Buscar gastos")
    ventana.geometry("400x250")
    ventana.grab_set()

    # Campos
    tk.Label(ventana, text="Palabra clave (etiqueta o comentario):").pack(pady=5)
    entry_clave = tk.Entry(ventana)
    entry_clave.pack(fill="x", padx=10)

    tk.Label(ventana, text="Fecha (YYYY-MM-DD) [opcional]:").pack(pady=5)
    entry_fecha = tk.Entry(ventana)
    entry_fecha.pack(fill="x", padx=10)

    def realizar_busqueda():
        clave = entry_clave.get().strip().lower()
        fecha = entry_fecha.get().strip()

        resultados = []
        for gasto in leer_gastos(FICHERO):
            if clave and clave not in gasto["comentario"].lower() and clave not in gasto["etiquetas"].lower():
                continue
            if fecha and gasto["fecha"] != fecha:
                continue
            resultados.append(gasto)

        if not resultados:
            messagebox.showinfo("Sin resultados", "No se encontraron coincidencias.")
            return

        boton_ver_todo.config(state=tk.NORMAL)

        # Mostrar resultados en tabla principal
        for fila in tabla.get_children():
            tabla.delete(fila)
        for gasto in resultados:
            tabla.insert("", tk.END, values=(gasto["fecha"], gasto["etiquetas"], gasto["monto"], gasto["comentario"]))

        ventana.destroy()

    tk.Button(ventana, text="🔍 Buscar", command=realizar_busqueda).pack(pady=10)
    tk.Button(ventana, text="Cancelar", command=ventana.destroy).pack()



# Crear ventana principal
root = tk.Tk()

FUENTE_GENERAL = ("Segoe UI", 10)
root.option_add("*Font", FUENTE_GENERAL)

root.title("Gestor de gastos")
root.minsize(1000, 600)

# Estilo/color de la tabla
style = ttk.Style()
style.theme_use("clam")

style.configure("Treeview", 
    background="white", 
    foreground="black", 
    rowheight=25,
    fieldbackground="white")

style.map("Treeview", background=[("selected", "#a3d2ca")])

# Contenedor principal horizontal
frame_contenedor = tk.Frame(root)
frame_contenedor.pack(expand=True, fill=tk.BOTH)

# Zona izquierda: formulario
frame_izquierda = tk.Frame(frame_contenedor)
frame_izquierda.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

# Zona derecha: tabla y botones
frame_derecha = tk.Frame(frame_contenedor)
frame_derecha.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10, pady=10)

# Tabla (arriba en derecha)
frame_tabla = tk.Frame(frame_derecha)
frame_tabla.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

# Botones (debajo de la tabla)
frame_botones = tk.Frame(frame_derecha)
frame_botones.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

# Color de los frames
COLOR_FONDO = "#f5f5f5"   # Gris muy claro
COLOR_PANEL = "#e8e8e8"   # Panel lateral
COLOR_BOTON = "#d0e1f9"   # Azul claro para botones

root.configure(bg=COLOR_FONDO)
frame_contenedor.configure(bg=COLOR_PANEL)
frame_izquierda.configure(bg=COLOR_PANEL)
frame_derecha.configure(bg=COLOR_PANEL)
frame_tabla.configure(bg=COLOR_FONDO)
frame_botones.configure(bg=COLOR_PANEL)


# Tabla
tabla = ttk.Treeview(frame_tabla, columns=("Fecha", "Etiquetas", "Monto", "Comentario"), show="headings")
tabla.pack(expand=True, fill=tk.BOTH)

tabla.heading("Fecha", text="Fecha")
tabla.column("Fecha", width=90, anchor="w", stretch=False)

tabla.heading("Etiquetas", text="Etiquetas")
tabla.column("Etiquetas", width=200, anchor="w", stretch=True)

tabla.heading("Monto", text="Monto (€)")
tabla.column("Monto", width=80, anchor="center", stretch=False)

tabla.heading("Comentario", text="Comentario")
tabla.column("Comentario", width=100, anchor="w", stretch=True)


# Formulario
tk.Label(frame_izquierda, text="Fecha (YYYY-MM-DD):").pack(anchor="w")
entry_fecha = tk.Entry(frame_izquierda)
entry_fecha.pack(fill="x")

tk.Label(frame_izquierda, text="Etiquetas (separadas por coma):").pack(anchor="w")
entry_etiquetas = tk.Entry(frame_izquierda)
entry_etiquetas.pack(fill="x")

tk.Label(frame_izquierda, text="Monto (€):").pack(anchor="w")
entry_monto = tk.Entry(frame_izquierda)
entry_monto.pack(fill="x")

tk.Label(frame_izquierda, text="Comentario (opcional):").pack(anchor="w")
entry_comentario = tk.Entry(frame_izquierda)
entry_comentario.pack(fill="x")

tk.Button(frame_izquierda, text="➕ Añadir Gasto", command=procesar_guardado, bg=COLOR_BOTON).pack(pady=10)

tk.Button(frame_botones, text="🗑️ Eliminar Gasto", command=eliminar_gasto_seleccionado, bg=COLOR_BOTON).pack(side=tk.LEFT, padx=5)
tk.Button(frame_botones, text="🧼 Limpiar TODOS", command=eliminar_todos_los_gastos, bg=COLOR_BOTON).pack(side=tk.LEFT, padx=5)
tk.Button(frame_botones, text="♻️ Restaurar Backup", command=restaurar_desde_backup, bg=COLOR_BOTON).pack(side=tk.LEFT, padx=5)
tk.Button(frame_botones, text="📊 Gasto mensual", command=mostrar_grafico_mensual, bg=COLOR_BOTON).pack(side=tk.LEFT, padx=5)
tk.Button(frame_botones, text="📂 Gasto por categoría", command=mostrar_grafico_por_categoria, bg=COLOR_BOTON).pack(side=tk.LEFT, padx=5)
tk.Button(frame_botones, text="🔎 Buscar", command=buscar_gastos, bg=COLOR_BOTON).pack(side=tk.LEFT, padx=5)
# Botón "Ver todo" (inicialmente desactivado)
boton_ver_todo = tk.Button(frame_botones, text="🔁 Ver todo", command=actualizar_tabla, state=tk.DISABLED, bg=COLOR_BOTON)
boton_ver_todo.pack(side=tk.LEFT, padx=5)


tk.Button(frame_botones, text="Salir", command=root.destroy, bg=COLOR_BOTON).pack(side=tk.RIGHT, padx=5)


# Inicializar
    

FICHERO = "gastos.csv"
inicializar_csv(FICHERO)
actualizar_tabla()
root.mainloop()

# Gestor de Gastos Personales

Este es un pequeño programa hecho en Python que permite registrar y consultar tus gastos desde la terminal. Los datos se guardan en un archivo CSV.

## Funcionalidades

- Añadir gasto (fecha, categoría, monto, comentario)
- Ver todos los gastos registrados
- Ver resumen de gastos por categoría
- Ver resumen de gastos por mes y año
- Eliminar gasto individual seleccionando por número
- Limpiar todos los gastos tras confirmación
- Validación de montos para evitar errores
- Manejo de errores: ignora gastos inválidos antiguos sin romper el programa

## 🔧 Estructura del proyecto

    gestor-gastos/
- main.py # Control del menú principal
- operaciones.py # Funciones de cálculo, resumen y borrado
- utils.py # Funciones auxiliares como validación
- gastos.csv # Archivo de almacenamiento de datos
- README.md # Documentación del proyecto

## Cómo usar

1. Ejecuta el archivo `main.py`
2. Interactúa desde el menú
3. Los datos se almacenan en el archivo `gastos.csv`

## Requisitos

- Python 3.8 o superior
- Solo usa librerías estándar (`csv`, `datetime`, etc.)

## Próximos pasos

- Añadir funcionalidades intermedias
- Crear interfaz gráfica con Tkinter

## Autor

Imanol G. de E.



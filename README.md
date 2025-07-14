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

- Solucionar problemas
    - Los caracteres especiales (ñ, tildes, ...) no se muestran correctamente

- Añadir funcionalidades avanzadas
    - Buscar por rango de fechas
    - Presupuesto mensual con alerta
    - Separar gastos de grafica mensual por categorias
    - Editar gasto existente
    - Ordenar los gastos al clicar las columnas (monto, fecha, etiquetas...)
    - Graficos adaptables (cambiar estilo de claro a oscuro, cambiar colores...)
    - Gestión de multiples usuarios

- Mejorar interfaz gráfica 
    - Animaciones

- Futuras versiones
    - Versión móvil (Kivy)
    - Versión web (Flask o Django + HTML/CSS)

## Autor

Imanol G. de E.



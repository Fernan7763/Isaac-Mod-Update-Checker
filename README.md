
# Gestor de Mods para Steam (Tkinter + JSON)

Este proyecto es una interfaz gráfica desarrollada en **Python** con **Tkinter** para gestionar mods descargados desde Steam, permitiendo ver, editar, filtrar y organizar información de cada mod basado en su archivo `metadata.xml` y datos obtenidos de la API de Steam. Hecho específicamente para el juego, The binding of Isaac: Repentance.
El objetivo es facilitar la gestión de mods, permitiendo a los usuarios mantener un registro actualizado y organizado de sus modificaciones.

---

## 🧩 ¿Qué hace este gestor?

- Carga carpetas de mods y extrae su nombre, versión, ID y fechas desde `metadata.xml`.
- Guarda los datos en un archivo local `mods_info.json`.
- Verifica si hay una nueva versión disponible mediante la API de Steam.
- Muestra todos los mods en una interfaz con columnas ordenadas y botones de acción.
- Permite:
  - Descargar el mod directamente desde Steam.
  - Editar cualquier campo desde la interfaz.
  - Eliminar mods del registro local.
- Incluye filtros en cascada, ordenamiento por estado y nombre, y limpieza de filtros.

---

## 💡 Estructura de la interfaz

| Nombre | Versión | Nueva Versión | Fecha Publicación | Fecha Actualización | Acción | Editar | Eliminar Mod |
|--------|---------|----------------|--------------------|----------------------|--------|--------|---------------|

Cada fila representa un mod con su información básica y botones de acción.

---

## ⚙️ Requisitos

- Python 3.8 o superior
- Librerías estándar: `tkinter`, `json`, `os`, `webbrowser`
- Acceso a internet para consultar la API de Steam

---

## 📁 Archivos principales

- `Interfaz.py` → Ventana principal y estructura general.
- `Interfaz_Filtros.py` → Funciones para filtros por nombre, versión y estado.
- `Interfaz_Listas.py` → Carga y dibujado de la lista de mods con botones.
- `Interfaz_Verificar.py` → Comparación de versiones, extracción de metadatos y acceso a la API de Steam.

---

## 🚀 Uso

1. Ejecuta `Interfaz.py`.
2. Selecciona la carpeta raíz donde están los mods. (Carpeta de nombre mods)
3. Pulsa **Cargar** para leer los archivos `metadata.xml`.
4. Filtra, ordena, edita o elimina mods según tus necesidades.

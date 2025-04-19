# ---------- Importaciones ----------
from Interfaz_Verificar import comparar_versiones  # Asegúrate de que la ruta sea correcta
from tkinter import Label, Button, messagebox, simpledialog
import tkinter as tk
import webbrowser
import os
import json

# ---------- Constantes de Estilo ----------
COLOR_VERDE = "#00FF00"
COLOR_ROJO = "#FF5555"
COLOR_AZUL = "#44AAFF"
COLOR_AMARILLO = "#FFD700"
COLOR_TEXTO = "#FFFFFF"
COLOR_NO_ENCONTRADO = "#FF3333"
COLOR_FONDO = "#1e1e1e"
COLOR_BOTON = "#3a3a3a"
FUENTE_GENERAL = ("Segoe UI", 10)

ARCHIVO_JSON = "mods_info.json"


# ---------- Función Principal Externa ----------
def cargar_y_mostrar_mods(frame, filtros_activos=None):
    """
    Carga los datos del JSON, aplica filtros si hay, los ordena y los muestra.
    """
    lista = cargar_mods_json()
    if filtros_activos:
        lista = aplicar_filtros(lista, filtros_activos)
    lista = ordenar_mods(lista)
    dibujar_lista_mods(frame, lista)




# ---------- Lectura del JSON ----------
def cargar_mods_json():
    if os.path.exists(ARCHIVO_JSON):
        with open(ARCHIVO_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


# ---------- Aplicar Filtros ----------
def aplicar_filtros(lista, filtros):
    """
    Aplica los filtros proporcionados en cascada.
    Cada filtro es una función que recibe un mod y devuelve True o False.
    """
    for filtro in filtros:
        lista = list(filter(filtro, lista))
    return lista


# ---------- Dibujar Lista ----------
def dibujar_lista_mods(frame, lista_mods):
    for widget in frame.winfo_children():
        widget.destroy()

    # --- Títulos de columna ---
    titulos = ["Nombre", "Versión", "Nueva Versión", "Fecha de Publicación", "Fecha de Actualización",
               "Acción", "  Editar  ", "Eliminar"]
    
    for j, titulo in enumerate(titulos):
        Label(
            frame, text=titulo, font=(FUENTE_GENERAL[0], FUENTE_GENERAL[1], "bold"),
            fg=COLOR_TEXTO, bg=COLOR_FONDO, padx=5, pady=5
        ).grid(row=0, column=j, padx=5, pady=2)

    # --- Fila por mod ---
    for i, mod in enumerate(lista_mods):
        agregar_fila_mod(frame, mod, i + 1)  # desplazamos +1 para dejar espacio al encabezado

# ---------- Fila Individual ----------
def agregar_fila_mod(frame, mod, index):
    campos = ["nombre", "version", "nueva_version", "fecha_publicacion", "fecha_actualizacion"]

    for j, campo in enumerate(campos):
        valor = mod.get(campo, "No encontrado")
        color = obtener_color_dato(mod, campo, valor)

        Label(
            frame, text=valor, font=FUENTE_GENERAL,
            fg=color, bg=COLOR_FONDO, padx=5, pady=3
        ).grid(row=index, column=j, padx=5, pady=2)

    crear_botones(frame, mod, index)


# ---------- Determinar Color ----------
def obtener_color_dato(mod, campo, valor):
    estado = mod.get("estado", "")
    
    if campo == "version":
        if estado == "actualizable":
            return COLOR_ROJO
        elif estado == "mayor":
            return COLOR_AZUL
        elif estado == "igual":
            return COLOR_VERDE
    elif campo == "nueva_version":
        if estado == "actualizable":
            return COLOR_VERDE
        elif estado == "mayor":
            return COLOR_AZUL
        elif estado == "igual":
            return COLOR_VERDE

    return COLOR_NO_ENCONTRADO if valor == "No encontrado" else COLOR_TEXTO



# ---------- Botones ----------
def crear_botones(frame, mod, index):
    # Botón Descargar
    b_desc = Button(frame, text="Descargar", bg=COLOR_AZUL, fg="white",
                    font=FUENTE_GENERAL, activebackground="#2B8ACF", cursor="hand2",
                    command=lambda m=mod: descargar_mod(m))
    b_desc.grid(row=index, column=5)
    b_desc.bind("<ButtonPress-1>", lambda e, b=b_desc: b.config(bg="#2B8ACF"))
    b_desc.bind("<ButtonRelease-1>", lambda e, b=b_desc: b.config(bg=COLOR_AZUL))

    # Botón Modificar
    b_mod = Button(frame, text="Modificar", bg=COLOR_AMARILLO, fg="black",
                   font=FUENTE_GENERAL, activebackground="#C0A000", cursor="hand2")
    b_mod.grid(row=index, column=6)
    b_mod.bind("<ButtonPress-1>", lambda e, b=b_mod: b.config(bg="#C0A000"))
    b_mod.bind("<ButtonRelease-1>", lambda e, b=b_mod: b.config(bg=COLOR_AMARILLO))
    b_mod.config(command=lambda: mostrar_menu_modificar(frame, b_mod, mod, index, lambda idx=index: actualizar_fila(frame, mod, idx)))

    # Botón Eliminar
    b_del = Button(frame, text="Eliminar", bg="#AA3333", fg="white",
                   font=FUENTE_GENERAL, activebackground="#882222", cursor="hand2",
                   command=lambda m=mod: eliminar_mod(m, frame))
    b_del.grid(row=index, column=7)
    b_del.bind("<ButtonPress-1>", lambda e, b=b_del: b.config(bg="#882222"))
    b_del.bind("<ButtonRelease-1>", lambda e, b=b_del: b.config(bg="#AA3333"))


# ---------- Menú Modificar ----------
def mostrar_menu_modificar(frame, boton, mod, index, refrescar_fila):
    opciones = {
        "Versión actual": "version",
        "Nueva versión": "nueva_version",
        "Fecha de publicación": "fecha_publicacion",
        "Fecha de actualización": "fecha_actualizacion"
    }
    menu = tk.Menu(frame, tearoff=0, bg=COLOR_FONDO, fg=COLOR_TEXTO,
                   activebackground="#333333", activeforeground="white",
                   font=FUENTE_GENERAL)
    for texto, campo in opciones.items():
        menu.add_command(label=texto, command=lambda c=campo: modificar_dato(mod, c, index, refrescar_fila))
    x = boton.winfo_rootx()
    y = boton.winfo_rooty() + boton.winfo_height()
    menu.tk_popup(x, y)


def modificar_dato(mod, campo, index, refrescar_fila):
    nuevo_valor = simpledialog.askstring("Modificar Dato", f"Ingrese nuevo valor para '{campo}':", initialvalue=mod.get(campo, ""))
    if nuevo_valor:
        mod[campo] = nuevo_valor

        # Recalcular estado si se modificó la versión o nueva versión
        if campo in ("version", "nueva_version"):
            version = mod.get("version", "")
            nueva_version = mod.get("nueva_version", "")
            mod["estado"] = comparar_versiones(version, nueva_version)

        guardar_mods_json_actualizado(mod)
        refrescar_fila(index)


def guardar_mods_json_actualizado(mod_actualizado):
    lista = cargar_mods_json()
    for i, m in enumerate(lista):
        if m.get("id") == mod_actualizado.get("id"):
            lista[i] = mod_actualizado
            break
    with open(ARCHIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(lista, f, indent=4)



def actualizar_fila(frame, mod, index):
    for widget in frame.grid_slaves(row=index):
        widget.destroy()
    agregar_fila_mod(frame, mod, index)


# ---------- Funciones de Acción ----------
def descargar_mod(mod):
    mod_id = mod.get("id")
    if mod_id:
        url = f"https://steamcommunity.com/sharedfiles/filedetails/?id={mod_id}"
        webbrowser.open(url)
    else:
        messagebox.showwarning("ID no encontrado", f"El mod '{mod.get('nombre', 'Desconocido')}' no tiene ID válido.")


def eliminar_mod(mod, frame):
    respuesta = messagebox.askyesno("Confirmar eliminación", f"¿Eliminar '{mod['nombre']}' del registro?")
    if not respuesta:
        return

    lista = cargar_mods_json()
    nueva_lista = [m for m in lista if m.get("id") != mod.get("id")]

    with open(ARCHIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(nueva_lista, f, indent=4)

    dibujar_lista_mods(frame, nueva_lista)

# ---------- Ordenamiento ----------
def ordenar_mods(lista_mods):
    """
    Ordena los mods primero por estado (según prioridad) y luego por nombre alfabéticamente.
    """
    prioridad_estado = {
        "actualizable": 0,
        "mayor": 1,
        "igual": 2,
        "fecha": 3
    }

    def clave_orden(mod):
        estado = mod.get("estado", "").lower()
        prioridad = prioridad_estado.get(estado, 4)  # valores desconocidos van al final
        nombre = mod.get("nombre", "").lower()
        return (prioridad, nombre)

    return sorted(lista_mods, key=clave_orden)



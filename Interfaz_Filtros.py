from tkinter import Entry, Button, Label, StringVar, BooleanVar, Checkbutton
import Interfaz_Listas as IL

# ---------- Variables Globales ----------
filtros_activos = []
entrada_nombre = None
entrada_version = None
filtro_sin_act = None
filtro_ver_dif = None
frame_lista = None  # Se asignará desde Interfaz.py

# ---------- Asignar el Frame contenedor de la lista ----------
def asignar_frame_lista(frame):
    global frame_lista
    frame_lista = frame

# ---------- Inicialización de filtros ----------
def crear_interfaz_filtros(frame_filtros):
    global entrada_nombre, entrada_version, filtro_sin_act, filtro_ver_dif

    filtro_sin_act = BooleanVar()
    filtro_ver_dif = BooleanVar()

    Label(frame_filtros, text="Nombre:", fg="white", bg="#1e1e1e").grid(row=0, column=0, padx=5)
    entrada_nombre = Entry(frame_filtros)
    entrada_nombre.grid(row=0, column=1, padx=5)

    Label(frame_filtros, text="Versión actual:", fg="white", bg="#1e1e1e").grid(row=0, column=2, padx=5)
    entrada_version = Entry(frame_filtros)
    entrada_version.grid(row=0, column=3, padx=5)

    Button(frame_filtros, text="Aplicar filtros", command=aplicar_filtros,
           bg="#3a3a3a", fg="white").grid(row=0, column=4, padx=10)

    Button(frame_filtros, text="Limpiar", command=limpiar_filtros,
           bg="#444", fg="white").grid(row=0, column=5)

    Checkbutton(frame_filtros, text="Sin actualización", variable=filtro_sin_act,
                bg="#1e1e1e", fg="white", selectcolor="#1e1e1e", activebackground="#1e1e1e", activeforeground="white")\
        .grid(row=1, column=0, columnspan=2, sticky="w", padx=5)

    Checkbutton(frame_filtros, text="Versión diferente", variable=filtro_ver_dif,
                bg="#1e1e1e", fg="white", selectcolor="#1e1e1e", activebackground="#1e1e1e", activeforeground="white")\
        .grid(row=1, column=2, columnspan=2, sticky="w", padx=5)

# ---------- Filtros disponibles ----------
def filtro_por_nombre(nombre):
    return lambda mod: nombre.lower() in mod.get("nombre", "").lower()

def filtro_por_version(version):
    return lambda mod: mod.get("version", "") == version

def filtro_sin_actualizacion():
    return lambda mod: mod.get("nueva_version", "").lower() == "no encontrado"

def filtro_version_diferente():
    return lambda mod: mod.get("version", "") != mod.get("nueva_version", "")

# ---------- Aplicar filtros ----------
def aplicar_filtros():
    global filtros_activos
    filtros_activos = []

    campos = [
        (entrada_nombre, filtro_por_nombre),
        (entrada_version, filtro_por_version)
    ]

    for entrada, filtro_func in campos:
        valor = entrada.get().strip()
        if valor:
            filtros_activos.append(filtro_func(valor))

    if filtro_sin_act.get():
        filtros_activos.append(filtro_sin_actualizacion())

    if filtro_ver_dif.get():
        filtros_activos.append(filtro_version_diferente())

    IL.cargar_y_mostrar_mods(frame_lista, filtros_activos)

# ---------- Limpiar filtros ----------
def limpiar_filtros():
    entrada_nombre.delete(0, 'end')
    entrada_version.delete(0, 'end')
    filtro_sin_act.set(False)
    filtro_ver_dif.set(False)
    filtros_activos.clear()
    IL.cargar_y_mostrar_mods(frame_lista)

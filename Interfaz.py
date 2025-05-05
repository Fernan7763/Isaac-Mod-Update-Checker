# ---------- Importaciones ----------
import tkinter as tk
import os
import json


# ---------- Importaciones de otros modulos ----------
import Interfaz_Listas as IL
import Interfaz_Verificar as IV
import Interfaz_Filtros as IF


# ---------- Constantes ----------
ARCHIVO_JSON = "mods_info.json"
COLOR_FONDO = "#1e1e1e"
COLOR_TEXTO = "white"
COLOR_BOTON = "#3a3a3a"
FUENTE_GENERAL = ("Segoe UI", 10)


# ---------- Configuración Inicial ----------
ventana = tk.Tk()
ventana.title("Verificador de Mods")
ventana.configure(bg=COLOR_FONDO)
ventana.state("zoomed")


# ---------- Contenedor Principal ----------
main_frame = tk.Frame(ventana, bg=COLOR_FONDO)
main_frame.pack(expand=True, fill="both", padx=20, pady=20)


# ---------- Título ----------
titulo = tk.Label(main_frame, text="Verificador de Mods", font=("Segoe UI", 18, "bold"),
                  bg=COLOR_FONDO, fg=COLOR_TEXTO)
titulo.pack(pady=(10, 15))


# ---------- Sección Ruta de Carpeta y Botones ----------
ruta_frame = tk.Frame(main_frame, bg=COLOR_FONDO)
ruta_frame.pack(fill="x", pady=(0, 10))

tk.Label(ruta_frame, text="Ruta:", font=FUENTE_GENERAL,
         bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(side="left", padx=(0, 5))

entrada_ruta = tk.Entry(
    ruta_frame, width=60, font=FUENTE_GENERAL,
    bg=COLOR_BOTON, fg=COLOR_TEXTO,
    insertbackground=COLOR_TEXTO
)
entrada_ruta.pack(side="left", padx=5)

def seleccionar_ruta():
    IV.manejar_seleccion_ruta(entrada_ruta, boton_cargar)

boton_buscar = tk.Button(ruta_frame, text="📂", font=FUENTE_GENERAL,
                         command=seleccionar_ruta, bg=COLOR_BOTON, fg=COLOR_TEXTO)
boton_buscar.pack(side="left", padx=(5, 0))

boton_cargar = tk.Button(ruta_frame, text="Cargar Mods", font=FUENTE_GENERAL,
                         state="disabled", bg=COLOR_BOTON, fg=COLOR_TEXTO)
boton_cargar.pack(side="left", padx=(10, 0))

boton_actualizar = tk.Button(ruta_frame, text="Consultar Actualizaciones", font=FUENTE_GENERAL,
                             bg=COLOR_BOTON, fg=COLOR_TEXTO)
boton_actualizar.pack(side="left", padx=(10, 0))


# ---------- Sección de Filtros ----------
filtros_frame = tk.Frame(main_frame, bg=COLOR_FONDO)
filtros_frame.pack(fill="x", pady=(0, 10))

IF.crear_interfaz_filtros(filtros_frame)


# ---------- Lista de Mods ----------
canvas = tk.Canvas(main_frame, bg=COLOR_FONDO, highlightthickness=0)
scrollbarx = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
#scrollbary = tk.Scrollbar(main_frame, orient="horizontal", command=canvas.xview)
canvas.configure(yscrollcommand=scrollbarx.set)
#canvas.configure(yscrollcommand=scrollbary.set)

scrollbarx.pack(side="right", fill="y")
#scrollbary.pack(side="bottom", fill="x")
canvas.pack(side="left", fill="both", expand=True)

lista_frame = tk.Frame(canvas, bg=COLOR_FONDO)
canvas.create_window((0, 0), window=lista_frame, anchor="nw")

IF.asignar_frame_lista(lista_frame)

def ajustar_scroll(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

lista_frame.bind("<Configure>", ajustar_scroll)


# ---------- Estado Inferior ----------
estado_label = tk.Label(ventana, text="Listo", bg=COLOR_FONDO,
                        fg="gray", font=("Segoe UI", 9))
estado_label.pack(pady=5)


# ---------- Funciones iniciales de carga ----------
def cargar_mods():
    if not os.path.exists(ARCHIVO_JSON):
        ejemplo = [{
            "nombre": "Example Mod",
            "version": "1.0",
            "nueva_version": "1.0",
            "fecha_publicacion": "1-1-2025",
            "fecha_actualizacion": "1-1-2025",
            "tamaño": "10 MB",
            "estado": "igual",
            "id": "2575911103"
        }]
        with open(ARCHIVO_JSON, "w", encoding="utf-8") as f:
            json.dump(ejemplo, f, indent=4)

    with open(ARCHIVO_JSON, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []
    IF.limpiar_filtros()

def cargar_datos_desde_ruta():
    global mods
    def redibujar(mods_filtrados):
        global mods
        mods = mods_filtrados
        IL.dibujar_lista_mods(lista_frame, mods)

    IV.manejar_carga_mods(entrada_ruta, estado_label, cargar_mods, redibujar)
    IF.limpiar_filtros()

def consultar_actualizaciones():
    global mods
    if not mods:
        estado_label.config(text="⚠ No hay mods cargados.")
        return

    estado_label.config(text="🔍 Consultando actualizaciones en Steam...")
    ventana.update_idletasks()

    IV.actualizar_mods_desde_steam(mods, estado_label)

    mods = cargar_mods()
    IL.dibujar_lista_mods(lista_frame, mods)
    IF.limpiar_filtros()

# ---------- Asignación de Funciones ----------
boton_cargar.config(command=cargar_datos_desde_ruta)
boton_actualizar.config(command=consultar_actualizaciones)


# ---------- Cargar Datos Iniciales ----------
mods = cargar_mods()
IL.dibujar_lista_mods(lista_frame, mods)
IF.limpiar_filtros()


# ---------- Punto de Entrada ----------
if __name__ == "__main__":
    ventana.mainloop()

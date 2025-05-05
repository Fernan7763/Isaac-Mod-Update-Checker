# ---------- Importaciones ----------
import os
import json
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from tkinter import filedialog, messagebox


# ---------- Constantes ----------
ARCHIVO_JSON = "mods_info.json"
API_URL = "https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/"
MESES_ES = {
    1: "ENE", 2: "FEB", 3: "MAR", 4: "ABR", 5: "MAY", 6: "JUN",
    7: "JUL", 8: "AGO", 9: "SEP", 10: "OCT", 11: "NOV", 12: "DIC"
}

# ---------- Validar Version ----------
def es_version_valida(version):
    return all(part.isdigit() for part in version.split("."))


# ---------- Comprobar y comparar versiones ----------
def comparar_versiones(local, nueva):
    if not local or not nueva:
        return "none"

    if not es_version_valida(local) or not es_version_valida(nueva):
        return "none"

    try:
        l_parts = list(map(int, local.split(".")))
        n_parts = list(map(int, nueva.split(".")))

        # Rellenar con ceros para que ambas listas tengan la misma longitud
        max_len = max(len(l_parts), len(n_parts))
        l_parts += [0] * (max_len - len(l_parts))
        n_parts += [0] * (max_len - len(n_parts))

        if l_parts == n_parts:
            return "igual"
        elif l_parts < n_parts:
            return "actualizable"
        else:
            return "mayor"
    except:
        return "desconocido"


# ---------- Extraer Datos de Metadata ----------
def extraer_datos_metadata(path_metadata):
    try:
        tree = ET.parse(path_metadata)
        root = tree.getroot()
        nombre = root.find("name").text.strip()
        version = root.find("version").text.strip()
        mod_id = root.find("id").text.strip()
        return nombre, mod_id, version
    except Exception as e:
        print(f"Error al procesar {path_metadata}: {e}")
        return "Error de Lectura", "Error de Lectura", "Error de Lectura"


# ---------- Manejar la ruta de la carpeta de Mods ----------
def manejar_seleccion_ruta(entrada_widget, boton_cargar):
    ruta = filedialog.askdirectory(title="Selecciona la carpeta de mods")
    if not ruta:
        return

    entrada_widget.delete(0, "end")
    entrada_widget.insert(0, ruta)

    contiene_mods = False
    for carpeta in os.listdir(ruta):
        path_metadata = os.path.join(ruta, carpeta, "metadata.xml")
        if os.path.isdir(os.path.join(ruta, carpeta)) and os.path.exists(path_metadata):
            contiene_mods = True
            break

    boton_cargar.config(state="normal" if contiene_mods else "disabled")
    if not contiene_mods:
        messagebox.showwarning("Sin mods", "No se encontraron mods en la carpeta seleccionada.")
    else:
        messagebox.showinfo("Mods encontrados", "Presione Cargar Mods para cargar la información.")


# ---------- Manejar la Carga Local de Mods ----------
def cargar_mods_locales(ruta, estado_label=None):
    mods_info = []

    for carpeta in os.listdir(ruta):
        path_carpeta = os.path.join(ruta, carpeta)
        path_metadata = os.path.join(path_carpeta, "metadata.xml")

        if os.path.isdir(path_carpeta) and os.path.exists(path_metadata):
            nombre, mod_id, version = extraer_datos_metadata(path_metadata)
            if not nombre or not mod_id:
                continue

            estado = comparar_versiones(version, "No encontrado")
            info = {
                "nombre": nombre,
                "version": version,
                "nueva_version": "No Consultada",
                "fecha_publicacion": "No Consultada",
                "fecha_actualizacion": "No Consultada",
                "id": mod_id,
                "timestamp_creacion": os.path.getctime(path_carpeta),
                "estado": estado
            }

            mods_info.append(info)

    mods_info.sort(key=lambda mod: mod["timestamp_creacion"])

    for idx, mod in enumerate(mods_info, start=1):
        mod["orden_creacion"] = idx
        del mod["timestamp_creacion"]

    with open(ARCHIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(mods_info, f, indent=4, ensure_ascii=False)

    if estado_label:
        advertencia = f" ⚠️ Se detectaron más de 50 mods ({len(mods_info)})." if len(mods_info) > 50 else ""
        estado_label.config(text=f"📦 {len(mods_info)} mods locales cargados.{advertencia}")


# ---------- Manejar la Carga de Mods ----------
def manejar_carga_mods(entrada_widget, estado_label, cargar_mods_func, redibujar_callback):
    ruta = entrada_widget.get()
    if not os.path.exists(ruta):
        estado_label.config(text="❌ Ruta inválida.")
        return

    cargar_mods_locales(ruta, estado_label)
    mods = cargar_mods_func()
    redibujar_callback(mods)


# ---------- Actualizar consulta de Mods desde Steam ----------
def actualizar_mods_desde_steam(mods_actualizados, estado_label):
    if os.path.exists(ARCHIVO_JSON):
        with open(ARCHIVO_JSON, "r", encoding="utf-8") as f:
            mods_existentes = json.load(f)
    else:
        mods_existentes = []
    dic_existentes = {mod["id"]: mod for mod in mods_existentes}

    actualizados = 0
    for mod in mods_actualizados:
        info = obtener_info_steam(mod["id"])
        mod["nueva_version"] = info["nueva_version"]
        mod["fecha_actualizacion"] = info["fecha_actualizacion"]
        mod["fecha_publicacion"] = info["fecha_publicacion"]
        mod["tamaño"] = info["tamaño"]
        mod["estado"] = comparar_versiones(mod.get("version", ""), mod["nueva_version"])
        dic_existentes[mod["id"]] = mod
        actualizados += 1

    mods_final = list(dic_existentes.values())
    with open(ARCHIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(mods_final, f, indent=4, ensure_ascii=False)

    estado_label.config(text=f"✅ Información actualizada de {actualizados} mods desde Steam.")



# ---------- Realizar request a la API----------
def obtener_info_steam(mod_id):
    try:
        response = requests.post(API_URL, data={
            'itemcount': 1,
            'publishedfileids[0]': mod_id
        })
        if response.status_code != 200:
            raise Exception("API request failed")

        details = response.json()["response"]["publishedfiledetails"][0]
        print("------- ",details)
        descripcion = details.get("description", "")
        update_time = details.get("time_updated", 0)
        create_time = details.get("time_created", 0)
        size_bytes = details.get("file_size", 0)
        size_bytes = int(details.get("file_size", 0))
        size_mb = round(size_bytes / (1024 * 1024), 2)


        # Buscar versión en la descripción
        import re
        version_match = re.search(r"v?(\d+(\.\d+)+)", descripcion)
        nueva_version = version_match.group(1) if version_match else ""

        return {
            "nueva_version": nueva_version,
            "fecha_actualizacion": timestamp_a_fecha(update_time),
            "fecha_publicacion": timestamp_a_fecha(create_time),
            "tamaño": size_mb
        }

    except Exception as e:
        print(f"Error consultando Steam para ID {mod_id}: {e}")
        return {
            "nueva_version": "No encontrado",
            "fecha_actualizacion": "No encontrado",
            "fecha_publicacion": "No encontrado",
            "tamaño": "No encontrado"
        }

def timestamp_a_fecha(ts):
    if not ts:
        return "No encontrado"
    dt = datetime.utcfromtimestamp(ts)
    return f"{dt.day:02d} {MESES_ES[dt.month]} {dt.year} a las {dt.strftime('%H:%M')}"

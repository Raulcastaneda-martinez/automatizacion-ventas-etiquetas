import re
from bs4 import BeautifulSoup

# 📍 Rutas de archivos
ruta_html_ml   = r"C:\Users\PC\Videos\ML DATOS.html"
ruta_html_data = r"C:\Users\PC\Videos\DATA.html"
ruta_copy      = r"C:\Users\PC\Videos\COPY.html"
ruta_ventas    = r"C:\Users\PC\Videos\LISTA VENTAS.txt"
ruta_guardado  = r"C:\Users\PC\Videos\LISTA_VENTAS_ACTUALIZADA.txt"

# ✅ 0. Cargar COPY (mapea código de diseño / CRFND / CRTZA → NP)
#    Estructura de COPY.html (columnas por índice de <td>):
#      col[3] = NP   col[4] = DISEÑO (código)
#      col[6] = SKU ML FUNDA (CRFND...)   col[7] = SKU ML TAZA (CRTZA...)
#    El NP solo aparece en la primera fila de cada grupo y se propaga
#    hacia abajo (fill-down) para las filas siguientes.
def cargar_dict_copy(ruta):
    dict_copy = {}
    skip_values = {"DISEÑO", "NP", "COLECCIÓN", "APODO INTERNO",
                   "SKU ML FUNDA", "SKU ML TAZA", ""}

    with open(ruta, "r", encoding="utf-8") as f:
        soup_copy = BeautifulSoup(f, "html.parser")

    table_copy = soup_copy.find("table")
    if not table_copy:
        return dict_copy

    current_np = ""

    for row in table_copy.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) < 7:
            continue

        np_val      = cells[3].get_text(strip=True).upper()
        diseno_code = cells[4].get_text(strip=True).upper()
        crfnd       = cells[6].get_text(strip=True).upper()
        crtza       = cells[7].get_text(strip=True).upper() if len(cells) > 7 else ""

        if np_val.startswith("NP"):
            current_np = np_val
        if not current_np:
            continue

        if diseno_code and diseno_code not in skip_values:
            dict_copy[diseno_code] = current_np

        if crfnd.startswith("CRFND"):
            dict_copy[crfnd] = current_np

        if crtza.startswith("CRTZA"):
            dict_copy[crtza] = current_np

    return dict_copy

code_to_np_copy = cargar_dict_copy(ruta_copy)

# ✅ 1. Cargar códigos generales desde ML DATOS (para todo excepto INFINIX y REDMAGIC)
with open(ruta_html_ml, "r", encoding="utf-8") as file:
    soup_ml = BeautifulSoup(file, "html.parser")

table_ml = soup_ml.find("table")
rows_ml = table_ml.find_all("tr")

code_to_np_ml = {}

for row in rows_ml:
    cells = row.find_all("td")
    if len(cells) >= 4:
        np_value = cells[1].get_text(strip=True).upper()  # NP en columna B
        col_c = cells[2].get_text(strip=True).upper()     # Código en columna C
        if np_value.startswith("NP") and col_c:
            code_to_np_ml[col_c] = np_value
        for cell in cells[10:]:
            code = cell.get_text(strip=True).upper()
            if code:
                code_to_np_ml[code] = np_value

# ✅ 2. Cargar códigos de DATA (solo para INFINIX y REDMAGIC)
with open(ruta_html_data, "r", encoding="utf-8") as file:
    soup_data = BeautifulSoup(file, "html.parser")

table_data = soup_data.find("table")
rows_data = table_data.find_all("tr")

code_to_np_data = {}

for row in rows_data:
    cells = row.find_all("td")
    if len(cells) >= 2:
        np_value = cells[0].get_text(strip=True).upper()  # Columna A = NP
        code_value = cells[1].get_text(strip=True).upper()  # Columna B = código
        if np_value.startswith("NP") and code_value:
            code_to_np_data[code_value] = np_value

# ✅ 3. Leer la lista de ventas y aplicar la traducción correcta
with open(ruta_ventas, "r", encoding="utf-8") as file:
    ventas = file.readlines()

ventas_actualizadas = []

for linea in ventas:
    partes = linea.strip().split(" ")

    if len(partes) > 2:
        codigo = partes[1].upper()
        modelo = partes[2].upper()

        if codigo in code_to_np_copy:
            partes[1] = code_to_np_copy[codigo]
        elif modelo in ["INFINIX", "REDMAGIC"]:
            if codigo in code_to_np_data:
                partes[1] = code_to_np_data[codigo]
        else:
            if codigo in code_to_np_ml:
                partes[1] = code_to_np_ml[codigo]

    ventas_actualizadas.append(" ".join(partes))

# ✅ 4. Guardar resultados
with open(ruta_guardado, "w", encoding="utf-8") as file:
    file.write("\n".join(ventas_actualizadas))

print(f"✅ Proceso completado. Archivo guardado en: {ruta_guardado}")

import re
import quopri
from bs4 import BeautifulSoup

# ✅ Marcas, colores y modelos
marcas_validas = ["LG", "CUBOT", "OPPO", "SAMSUNG", "ZTE"]
colores_validos = ["NEGRO", "BLANCO", "ROSA"]
infinix_modelos = [
    "GT 20 PRO", "HOT 30", "HOT 30I", "HOT 40I", "HOT 50", "HOT 50 PRO",
    "HOT 50 PRO PLUS", "HOT 50I", "NOTE 30", "NOTE 30 PRO", "NOTE 40",
    "SMART 7", "SMART 7 HD", "SMART 8", "SMART 9"
]

ruta_archivo = "Ventas.mhtml"
ruta_codigos = "DATA.html"

# ✅ Leer archivo de códigos válidos desde la columna B
with open(ruta_codigos, "r", encoding="utf-8") as f:
    soup_codigos = BeautifulSoup(f, "html.parser")
    celdas_columna_b = soup_codigos.select("table.waffle td:nth-of-type(2)")
    codigos_validos = [celda.text.strip().upper() for celda in celdas_columna_b if celda.text.strip()]

def encontrar_codigo(texto):
    for codigo in codigos_validos:
        if codigo in texto:
            return codigo
    return "SIN_CODIGO"

# ✅ Helpers para leer el SKU y la cantidad reales del HTML de MercadoLibre.
# La estructura real es:
#   <span class="sc-product-data__sku">
#       <span class="sc-product-data__value">SKU: HUA2MMTRNV12IXX - CRFND000817</span>
#   </span>
#   <span class="sc-product-data__qty">
#       <span class="sc-product-data__value">1 unidad</span>
#   </span>

def obtener_sku(producto):
    sku_tag = producto.find_next("span", class_="sc-product-data__sku")
    return sku_tag.get_text(strip=True) if sku_tag else ""

def obtener_piezas_raw(producto):
    qty_tag = producto.find_next("span", class_="sc-product-data__qty")
    return qty_tag.get_text(strip=True) if qty_tag else "1 unidad"

# ✅ El SKU siempre trae el código real (CRFND/CRTZA) después del " - ".
# Buscar SIEMPRE aquí primero: es la fuente más confiable para encontrar
# el diseño o el NP más adelante.
def extraer_crfnd_crtza(texto):
    m = re.search(r'CRFND\d+|CRTZA\d+', texto.upper())
    return m.group(0) if m else ""

# ✅ Leer y procesar el archivo MHTML
with open(ruta_archivo, "rb") as file:
    raw_content = file.read()

decoded_content = quopri.decodestring(raw_content).decode('utf-8', errors='ignore')

html_match = re.search(r'<!DOCTYPE html>.*</html>', decoded_content, re.DOTALL | re.IGNORECASE)
if not html_match:
    raise ValueError("No se pudo encontrar la sección HTML en el archivo.")

html = html_match.group(0)
soup = BeautifulSoup(html, "html.parser")

productos = soup.find_all("a", class_="redirect-row")
resultados = []

for producto in productos:
    folio_tag = producto.find_previous("div", class_="left-column__pack-id")
    folio = folio_tag.text.strip().replace("#", "") if folio_tag else "SIN_FOLIO"

    label_tag = producto.find("div", class_="label")
    label_text_raw = label_tag.text.strip() if label_tag else ""
    label_text = label_text_raw.upper()

    # ✅ CASO ESPECIAL: PAQUETE
    if "PAQUETE" in label_text:
        resultados.append(f"{folio} {label_text_raw.upper()}")
        continue

    # ✅ CASO ESPECIAL: TAZA
    if "TAZA" in label_text:
        sku_texto = obtener_sku(producto)
        codigo_taza = extraer_crfnd_crtza(sku_texto) or "SIN_CODIGO"

        piezas_raw = obtener_piezas_raw(producto)
        piezas = "1 PZ." if "1" in piezas_raw else piezas_raw.upper().replace("UNIDAD", "PZ.")
        resultados.append(f"{folio} {codigo_taza} TAZA {piezas}".upper())
        continue

    # ✅ CASO ESPECIAL: REDMAGIC
    redmagic_matches = [m.start() for m in re.finditer(r'redmagic', label_text_raw.lower())]
    if len(redmagic_matches) >= 2:
        second_redmagic_pos = redmagic_matches[1]
        modelo_redmagic_raw = label_text_raw[second_redmagic_pos:].strip()
        modelo_redmagic = "REDMAGIC " + modelo_redmagic_raw[8:].strip().upper()

        sku_texto = obtener_sku(producto)
        texto_busqueda = label_text_raw.upper()
        if sku_texto:
            texto_busqueda += " " + sku_texto.upper()

        codigo = extraer_crfnd_crtza(sku_texto) or encontrar_codigo(texto_busqueda)

        piezas_raw = obtener_piezas_raw(producto)
        piezas = "1 PZ." if "1" in piezas_raw else piezas_raw.upper().replace("UNIDAD", "PZ.")

        resultados.append(f"{folio} {codigo} {modelo_redmagic} 2MM {piezas}".upper())
        continue

    # ✅ CASO ESPECIAL: INFINIX
    modelo_infinix = None
    for m in infinix_modelos:
        if m in label_text:
            modelo_infinix = f"INFINIX {m}"
            break

    if modelo_infinix:
        sku_texto = obtener_sku(producto)
        texto_busqueda = label_text_raw.upper()
        if sku_texto:
            texto_busqueda += " " + sku_texto.upper()

        codigo = extraer_crfnd_crtza(sku_texto) or encontrar_codigo(texto_busqueda)

        piezas_raw = obtener_piezas_raw(producto)
        piezas = "1 PZ." if "1" in piezas_raw else piezas_raw.upper().replace("UNIDAD", "PZ.")

        resultados.append(f"{folio} {codigo} {modelo_infinix} 2MM {piezas}".upper())
        continue

    # ✅ FLUJO GENERAL
    sku_texto = obtener_sku(producto)
    codigo_crfnd = extraer_crfnd_crtza(sku_texto)

    if codigo_crfnd:
        diseño = codigo_crfnd
    else:
        href = producto.get("href", "")
        diseño_match = re.search(r'MLM-(\d+)-', href)
        diseño = diseño_match.group(1) if diseño_match else "SIN_DISEÑO"

    descripcion = producto.find("div", class_="row-description")
    desc_text = descripcion.text.strip() if descripcion else ""

    modelo = "SIN_MODELO"
    marca = ""

    modelo_match = re.search(r'Nombre del diseño:\s*(.+?)(?:\||$)', desc_text, re.IGNORECASE)
    if modelo_match:
        modelo = modelo_match.group(1).strip()
        if modelo.lower().startswith("para "):
            modelo = modelo[5:].strip()

    if "GALAXY" in label_text:
        if modelo != "SIN_MODELO":
            modelo = f"GALAXY {modelo.upper()}"
    elif "IPHONE" in desc_text.upper() and modelo != "SIN_MODELO":
        pass

    marca_match = re.search(r'Funda Para\s+(\w+)', label_text, re.IGNORECASE)
    if marca_match:
        posible_marca = marca_match.group(1).upper()
        if posible_marca in marcas_validas:
            marca = posible_marca
        elif posible_marca == "XIAOMI" and re.match(r'^\d', modelo):
            marca = "XIAOMI"

    if marca:
        modelo = f"{marca} {modelo}"

    color = ""
    color_match = re.search(r'Color:\s*([^\|<\n\r]+)', desc_text)
    if color_match:
        color_text = color_match.group(1).strip().upper()
        primera_palabra = re.split(r'[ /,-]', color_text)[0]
        if primera_palabra in colores_validos:
            color = primera_palabra

    material = "ELITE" if color else "2MM"
    extra = "MAGSAFE" if "MAGSAFE" in label_text else ""

    piezas_raw = obtener_piezas_raw(producto)
    piezas = "1 PZ." if "1" in piezas_raw else piezas_raw.upper().replace("UNIDAD", "PZ.")

    componentes = [folio, diseño, modelo]
    if material:
        componentes.append(material)
    if extra:
        componentes.append(extra)
    if color:
        componentes.append(color)
    componentes.append(piezas)

    linea = ' '.join(componentes).upper()
    resultados.append(re.sub(r'\s+', ' ', linea))

# ✅ Guardar resultados
with open("LISTA VENTAS.txt", "w", encoding="utf-8") as f:
    for linea in resultados:
        f.write(linea + "\n")

print("Extracción finalizada correctamente.")

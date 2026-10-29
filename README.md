# 📦 Automatización de ventas y guías de envío

Este proyecto contiene scripts de Python diseñados para automatizar el procesamiento de las ventas, identificar los códigos correspondientes a cada producto y preparar las guías de envío membretadas, listas para imprimir.

El sistema se divide en dos procesos principales:

- **Extracción y organización de ventas:** los scripts `ET.py` y `NP.py` trabajan en conjunto para obtener la información de las ventas y relacionar los códigos de los productos con sus respectivos números NP.
- **Preparación de guías para impresión:** el script `PDF.py` procesa los archivos PDF de las guías y agrega un texto identificador en el margen izquierdo.

## 📂 Scripts del proyecto

### 1. `ET.py` — Extracción de información de ventas

Lee el archivo `Ventas.mhtml`, que contiene la información de las ventas de Mercado Libre, y extrae los datos relevantes de los productos.

Entre sus funciones se encuentran:

- Obtener el folio de cada venta.
- Identificar los códigos de los productos mediante sus SKU.
- Reconocer modelos, marcas, colores y características de los productos.
- Identificar cantidades de piezas.
- Aplicar reglas especiales para productos como tazas, paquetes, fundas Infinix y equipos RedMagic.
- Generar el archivo `LISTA VENTAS.txt` con la información organizada de las ventas.

Este archivo de texto sirve como entrada para el siguiente proceso.

### 2. `NP.py` — Asignación de códigos NP

Procesa la lista de ventas generada por `ET.py` y utiliza archivos HTML con información de productos y diseños para identificar el número NP correspondiente a cada código.

Consulta las siguientes fuentes:

- `ML DATOS.html`: información general de códigos y números NP.
- `DATA.html`: códigos utilizados específicamente para modelos Infinix y RedMagic.
- `COPY.html`: relación entre diseños, números NP y códigos de fundas o tazas.

El script utiliza estas correspondencias para reemplazar los códigos identificados en las ventas por su número NP correspondiente, cuando existe una coincidencia.

Como resultado, genera el archivo:

`LISTA_VENTAS_ACTUALIZADA.txt`

Este documento contiene la información de las ventas después del proceso de asignación de NP.

### 3. `EJECUTAR PROCESOS.py` — Ejecución automática

Este script permite ejecutar los dos procesos anteriores de forma consecutiva, sin tener que iniciar cada uno manualmente.

El orden de ejecución es:

1. Ejecutar `ET.py` para extraer y organizar la información de las ventas.
2. Ejecutar `NP.py` para relacionar los códigos con sus respectivos números NP.

Si alguno de los scripts presenta un error, el proceso se detiene para evitar continuar con la siguiente etapa.

**Importante:** ambos scripts deben estar correctamente configurados y contar con sus archivos de entrada. Los nombres de los scripts deben coincidir con los indicados en el archivo ejecutor.

### 4. `PDF.py` — Preparación de guías membretadas

Procesa los archivos PDF de una carpeta de entrada y genera versiones preparadas para impresión.

Sus funciones principales son:

- Abrir cada archivo PDF encontrado en la carpeta configurada.
- Agregar un texto identificador en orientación vertical, sobre el margen izquierdo de la primera página.
- Utilizar el nombre original del archivo, sin la extensión `.pdf`, como texto identificador.
- Guardar el resultado en una carpeta de salida destinada a las guías listas para imprimir.
- Eliminar el archivo temporal utilizado para generar el texto.

El resultado son archivos PDF con el identificador de la guía incorporado.

**Nota:** el script actual procesa únicamente la primera página de cada PDF y utiliza rutas de carpetas configuradas directamente en el código.

## 🔄 Flujo de trabajo

El funcionamiento general del proyecto es el siguiente:

1. Se obtiene la información de las ventas y se guarda en `Ventas.mhtml`.
2. Se ejecuta `EJECUTAR PROCESOS.py`.
3. `ET.py` extrae los datos y genera `LISTA VENTAS.txt`.
4. `NP.py` utiliza esa información y genera `LISTA_VENTAS_ACTUALIZADA.txt`.
5. Se utiliza la información obtenida para identificar las ventas y organizar las etiquetas correspondientes.
6. `PDF.py` prepara las guías membretadas para su impresión.

## 🏷️ Nota importante sobre el renombrado de etiquetas

Al descargar una etiqueta, esta se renombra con la información correspondiente a la venta de la que se obtuvo mediante el proceso automatizado.

La referencia para identificar cada venta es el archivo TXT generado por `EJECUTAR PROCESOS.py`, que ejecuta los scripts de extracción y asignación de códigos.

Esto permite relacionar las etiquetas descargadas con la información organizada de cada venta y facilita su identificación durante la preparación de los pedidos.

El renombrado de las etiquetas forma parte del flujo de trabajo descrito; no debe confundirse con la función de `PDF.py`, cuyo código actual se encarga de agregar el identificador al PDF y guardarlo en la carpeta de salida.

## 🛠️ Requisitos

- Python 3.
- Beautiful Soup 4 (`beautifulsoup4`).
- PyPDF2.
- ReportLab.

Para instalar las dependencias, ejecuta:

```bash
pip install beautifulsoup4 PyPDF2 reportlab
```

## ⚙️ Configuración

Antes de ejecutar los scripts, verifica lo siguiente:

- Las rutas de los archivos HTML, MHTML y TXT corresponden a su ubicación real.
- Los archivos de datos contienen la información actualizada de los productos.
- Las carpetas de entrada y salida de los PDF están configuradas correctamente.
- Los scripts se encuentran en las ubicaciones esperadas por el ejecutor.

Actualmente, algunas rutas están definidas directamente en el código, por lo que puede ser necesario adaptarlas al equipo donde se ejecute el proyecto.

## 🎯 Objetivo del proyecto

Reducir el trabajo manual en la organización de ventas, la identificación de productos mediante códigos NP y la preparación de etiquetas de envío, manteniendo la información organizada y facilitando la impresión de las guías.


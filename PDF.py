import os
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def agregar_pie_pagina(pdf_input, pdf_output, texto_footer):
    # Crear un PDF temporal con el texto del footer
    footer_pdf = "footer_temp.pdf"
    c = canvas.Canvas(footer_pdf, pagesize=letter)
    
    # Agregar texto vertical al costado izquierdo
    c.saveState()
    c.translate(10, 10)  # Ajusta la posición inicial del texto
    c.rotate(90)          # Gira el texto 90 grados para que sea vertical
    c.setFont("Helvetica", 11)  # Cambia el tamaño de letra (segundo valor)
    c.drawString(0, 0, texto_footer)  # Dibuja el texto
    c.restoreState()
    
    c.save()

    # Leer el PDF original y el footer
    reader = PdfReader(pdf_input)
    writer = PdfWriter()
    footer_page = PdfReader(footer_pdf).pages[0]

    # Procesar solo la primera página del PDF
    first_page = reader.pages[0]
    first_page.merge_page(footer_page)
    writer.add_page(first_page)

    # Guardar el nuevo PDF con el pie de página
    with open(pdf_output, "wb") as output_pdf:
        writer.write(output_pdf)

    # Eliminar archivo temporal
    os.remove(footer_pdf)

# Carpeta de entrada y salida
carpeta_entrada = r"C:\Users\PC\Videos\guias tios O"
carpeta_salida = r"C:\Users\PC\Videos\IMPRIMIR.GUIAS"
os.makedirs(carpeta_salida, exist_ok=True)

# Procesar cada archivo PDF en la carpeta
for archivo_pdf in os.listdir(carpeta_entrada):
    if archivo_pdf.endswith(".pdf"):
        ruta_entrada = os.path.join(carpeta_entrada, archivo_pdf)
        ruta_salida = os.path.join(carpeta_salida, f"primera_pagina_{archivo_pdf}")
        texto_footer = archivo_pdf.replace(".pdf", "")  # Nombre del archivo sin extensión
        agregar_pie_pagina(ruta_entrada, ruta_salida, texto_footer)

print("listo vasti hermosa, revisa en tu carpeta de imprimir, postdata te amo : D.")

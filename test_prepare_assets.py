import os
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.graphics.shapes import Drawing, Rect, Circle, Line, String
from PIL import Image as PILImage, ImageDraw

# =============================================================================
# 0. PREPARAR IMÁGENES ANOTADAS
# =============================================================================
def prepare_annotated_body():
    bg_path = "src/assets/images/bg_men.png"
    out_path = "src/assets/images/bg_men_annotated.png"
    if not os.path.exists(bg_path):
        return None
    
    im = PILImage.open(bg_path).convert("RGBA")
    draw = ImageDraw.Draw(im)

    # Vista posterior (espalda) - Cabeza centrada en x=1310, y=180
    cx, cy = 1310, 180
    
    # Círculo diana rojo en el occipital
    draw.ellipse((cx-45, cy-45, cx+45, cy+45), outline="#dc2626", width=10)
    draw.ellipse((cx-18, cy-18, cx+18, cy+18), fill="#dc2626")
    
    # Línea indicadora
    draw.line((cx+45, cy, cx+220, cy-70), fill="#dc2626", width=8)
    
    # Cuadro informativo
    draw.rectangle((cx+220, cy-140, cx+560, cy+20), fill=(255, 255, 255, 245), outline="#dc2626", width=6)
    
    # Texto en el cuadro (si PIL default font funciona)
    draw.text((cx+235, cy-125), "LESIÓN OCCIPITAL (18:30 H)", fill="#991b1b")
    draw.text((cx+235, cy-90), "Brecha craneal profunda", fill="#1f2937")
    draw.text((cx+235, cy-60), "Impacto seco por caída", fill="#1f2937")
    draw.text((cx+235, cy-30), "Base craneal fracturada", fill="#1f2937")

    # Etiquetas de vista inferior
    draw.text((380, 1880), "VISTA ANTERIOR (FRENTE)", fill="#4b5563")
    draw.text((1180, 1880), "VISTA POSTERIOR (ESPALDA)", fill="#4b5563")

    im.save(out_path)
    return out_path

prepare_annotated_body()
print("Imagen anotada generada.")

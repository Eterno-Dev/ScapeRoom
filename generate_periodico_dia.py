import os
import pymupdf
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage, ImageDraw

# Registrar fuentes periodísticas auténticas de rotativa
try:
    pdfmetrics.registerFont(TTFont('Georgia', 'C:/Windows/Fonts/georgia.ttf'))
    pdfmetrics.registerFont(TTFont('Georgia-Bold', 'C:/Windows/Fonts/georgiab.ttf'))
    pdfmetrics.registerFont(TTFont('Georgia-Italic', 'C:/Windows/Fonts/georgiai.ttf'))
    FONT_HEADLINE = 'Georgia-Bold'
    FONT_BODY = 'Georgia'
    FONT_ITALIC = 'Georgia-Italic'
except Exception as e:
    print("Warning: Georgia not found, using Times:", e)
    FONT_HEADLINE = 'Times-Bold'
    FONT_BODY = 'Times-Roman'
    FONT_ITALIC = 'Times-Italic'

def create_photo_placeholder(filename, width_px, height_px, label, sublabel=""):
    im = PILImage.new('RGBA', (width_px, height_px), (245, 246, 248, 255))
    draw = ImageDraw.Draw(im)
    draw.rectangle((0, 0, width_px - 1, height_px - 1), outline="#9ca3af", width=2)
    cx, cy = width_px // 2, height_px // 2 - 10
    draw.rectangle((cx - 22, cy - 15, cx + 22, cy + 15), outline="#4b5563", width=2)
    draw.ellipse((cx - 9, cy - 9, cx + 9, cy + 9), outline="#4b5563", width=2)
    draw.ellipse((cx + 11, cy - 11, cx + 16, cy - 6), fill="#4b5563")
    draw.text((cx - len(label)*3.5, cy + 22), label, fill="#1f2937")
    if sublabel:
        draw.text((cx - len(sublabel)*3, cy + 35), sublabel, fill="#4b5563")
    im.save(filename)
    return filename

def build_periodico_dia_pdf(output_filename="5_periodico_dia.pdf"):
    os.makedirs("src/assets/images/periodico_dia", exist_ok=True)
    create_photo_placeholder("src/assets/images/periodico_dia/foto_kronos.png", 520, 220, "[ FOTO 1: SEDE CENTRAL KRONOS S.A. ]", "Recapitalizacion de emergencia")
    create_photo_placeholder("src/assets/images/periodico_dia/foto_caballo.png", 320, 180, "[ FOTO 2: NUEVO PURASANGRE ]", "Circuito de carreras Apex")
    create_photo_placeholder("src/assets/images/periodico_dia/foto_israel.png", 320, 180, "[ FOTO 3: FOTOGRAFIA DE INTELIGENCIA ]", "Enlace militar en Tel Aviv")

    # A4 = 595.27 x 841.89 pt
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=A4,
        leftMargin=24,
        rightMargin=24,
        topMargin=15,
        bottomMargin=15
    )

    styles = getSampleStyleSheet()

    # Tipografía de periódico auténtica (estilo EL PAÍS / New York Times)
    masthead_style = ParagraphStyle(
        'Masthead',
        parent=styles['Normal'],
        fontName=FONT_HEADLINE,
        fontSize=48,
        leading=50,
        alignment=1,
        textColor=colors.HexColor('#111827'),
        spaceBefore=1,
        spaceAfter=1
    )

    meta_bar = ParagraphStyle(
        'MetaBar',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor('#1F2937')
    )

    # TITULAR 1: Punchy, espectacular, periodístico
    hero_title = ParagraphStyle(
        'HeroTitle',
        parent=styles['Heading1'],
        fontName=FONT_HEADLINE,
        fontSize=24,
        leading=27,
        alignment=0,
        textColor=colors.HexColor('#991B1B'),
        spaceBefore=2,
        spaceAfter=3
    )

    hero_subtitle = ParagraphStyle(
        'HeroSub',
        parent=styles['Normal'],
        fontName=FONT_ITALIC,
        fontSize=10,
        leading=13.5,
        textColor=colors.HexColor('#374151'),
        spaceAfter=7
    )

    # TITULARES SECUNDARIOS
    sec_title = ParagraphStyle(
        'SecTitle',
        parent=styles['Heading2'],
        fontName=FONT_HEADLINE,
        fontSize=14,
        leading=17,
        textColor=colors.HexColor('#111827'),
        spaceBefore=1,
        spaceAfter=2
    )

    sec_subtitle = ParagraphStyle(
        'SecSub',
        parent=styles['Normal'],
        fontName=FONT_ITALIC,
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#4B5563'),
        spaceAfter=4
    )

    body_news = ParagraphStyle(
        'BodyNews',
        parent=styles['Normal'],
        fontName=FONT_BODY,
        fontSize=8.5,
        leading=12,
        alignment=4, # TA_JUSTIFY
        textColor=colors.HexColor('#1F2937')
    )

    caption_style = ParagraphStyle(
        'Caption',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7,
        leading=9,
        textColor=colors.HexColor('#4B5563')
    )

    story = []

    # =========================================================================
    # 1. CABECERA: EL DIARIO DEL DÍA (Estilo EL PAÍS)
    # =========================================================================
    story.append(Paragraph("EL DIARIO DEL DÍA", masthead_style))
    story.append(Paragraph("EL PERIÓDICO GLOBAL DE INFORMACIÓN GENERAL Y FINANZAS", ParagraphStyle('SubM', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8, leading=10, alignment=1, textColor=colors.HexColor('#4B5563'))))
    story.append(Spacer(1, 3))

    # Barra de fecha entre dos líneas finas auténticas de rotativa
    top_meta = [
        [
            Paragraph("SÁBADO 31 DE OCTUBRE DE 2026", meta_bar),
            Paragraph("AÑO XXVIII • NÚMERO 10.412", ParagraphStyle('MB1', parent=meta_bar, alignment=1)),
            Paragraph("EDICIÓN NACIONAL", ParagraphStyle('MB2', parent=meta_bar, alignment=1)),
            Paragraph("PRECIO: 2,00 $", ParagraphStyle('MB3', parent=meta_bar, alignment=2))
        ]
    ]
    t_top = Table(top_meta, colWidths=[160, 130, 140, 117])
    t_top.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,-1), 1, colors.HexColor('#000000')),
        ('LINEBELOW', (0,0), (-1,-1), 1, colors.HexColor('#000000')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_top)
    story.append(Spacer(1, 6))

    # =========================================================================
    # 2. NOTICIA PRINCIPAL: TITULAR ESPECTACULAR Y SUBTÍTULO DEFINITORIO
    # =========================================================================
    story.append(Paragraph("Kronos repunta un 120% en 12 horas", hero_title))
    story.append(Paragraph("Una inyección nocturna de 12 millones de dólares de su accionista mayoritario salva a la compañía del embargo judicial y reactiva sus operaciones.", hero_subtitle))

    kronos_col1 = (
        "<b>NUEVA YORK. —</b> En una de las jornadas más insólitas jamás presenciadas en Wall Street, el grupo "
        "<b>Kronos & Logística S.A.</b> protagonizó de madrugada un rebote vertical del <b>120%</b> tras haber tocado fondo bursátil la tarde anterior.<br/><br/>"
        "La Comisión de Mercados certificó una transferencia extraordinaria irrevocable de <b>12 millones de dólares</b> emitida por su socio de referencia, "
        "desactivando la orden de embargo cautelar dictada por el tribunal mercantil."
    )

    kronos_col2 = (
        "La repentina aparición de las garantías patrimoniales necesarias ha desatado intensas especulaciones en los círculos financieros sobre el origen de los avales familiares.<br/><br/>"
        "La dirección de Kronos aseguró en un escueto comunicado que la liquidez está garantizada y que la sociedad afrontará de inmediato todos sus compromisos pendientes."
    )

    kronos_text_table = Table([[
        Paragraph(kronos_col1, body_news),
        Paragraph(kronos_col2, body_news)
    ]], colWidths=[140, 145])
    kronos_text_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))

    kronos_photo_col = [
        Image("src/assets/images/periodico_dia/foto_kronos.png", width=250, height=95),
        Spacer(1, 2),
        Paragraph("Fachada de la sede central de Kronos en el distrito financiero tras suspenderse el preconcurso de acreedores. / REUTERS", caption_style)
    ]

    hero_layout = Table([[kronos_text_table, kronos_photo_col]], colWidths=[290, 257])
    hero_layout.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LINEBEFORE', (1,0), (1,0), 0.5, colors.HexColor('#D1D5DB')),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (0,0), 8),
        ('LEFTPADDING', (1,0), (1,0), 8),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(hero_layout)
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#000000'), spaceAfter=6))

    # =========================================================================
    # 3. SECCIÓN MEDIA: DOS COLUMNAS PERIODÍSTICAS CON FOTOS
    # =========================================================================

    # Columna Izquierda: Hípica / Apuestas
    col_horse = [
        Paragraph("<font color='#991B1B'><b>HÍPICA Y APUESTAS</b></font>", ParagraphStyle('TagH', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.5, leading=9, textColor=colors.HexColor('#991B1B'))),
        Paragraph("Nuevo caballo en las carreras clandestinas", sec_title),
        Paragraph("El sindicato de apuestas adquiere a 'Sombra Veloz' tras la muerte por sobredosis del animal titular.", sec_subtitle),
        Image("src/assets/images/periodico_dia/foto_caballo.png", width=255, height=95),
        Spacer(1, 2),
        Paragraph("El ejemplar purasangre adquirido de madrugada en una subasta privada. / AP", caption_style),
        Spacer(1, 4),
        Paragraph(
            "<b>LOUISVILLE. —</b> Apenas unas horas después del fulminante colapso en los boxes del cotizado caballo de carreras <i>'Tormenta Negra'</i> —cuya necropsia reveló una <b>dosis masiva de estimulantes no autorizados</b>—, "
            "el consorcio de apuestas clandestinas vinculado a Apex formalizó de urgencia la compraventa de un nuevo purasangre.<br/><br/>"
            "La operación, saldada íntegramente en efectivo por jóvenes operadores del circuito nocturno, confirma la presión apremiante por mantener abiertos los calendarios de apuestas amañadas.",
            body_news
        )
    ]

    # Columna Derecha: Internacional / Enlace militar
    col_israel = [
        Paragraph("<font color='#1E3A8A'><b>SEGURIDAD INTERNACIONAL</b></font>", ParagraphStyle('TagI', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.5, leading=9, textColor=colors.HexColor('#1E3A8A'))),
        Paragraph("Captan en Israel a un traficante de armas", sec_title),
        Paragraph("Fotografiado en Oriente Próximo a las 16:30 horas, a miles de kilómetros de suelo americano.", sec_subtitle),
        Image("src/assets/images/periodico_dia/foto_israel.png", width=255, height=95),
        Spacer(1, 2),
        Paragraph("Imagen satelital y de campo filtrada por los servicios de inteligencia militar cerca de Tel Aviv. / AFP", caption_style),
        Spacer(1, 4),
        Paragraph(
            "<b>TEL AVIV. —</b> Informes de inteligencia militar desclasificados esta mañana sitúan a un conocido intermediario de suministros bélicos cerrando un pacto clandestino de armamento en un enclave táctico de Oriente Próximo.<br/><br/>"
            "El registro gráfico fue captado <b>el día 30 a las 16:30 horas locales (apenas dos horas antes del anochecer en América)</b>, constatando que el enlace militar se encontraba a miles de kilómetros de distancia del continente americano.",
            body_news
        )
    ]

    mid_table = Table([[col_horse, col_israel]], colWidths=[267, 280])
    mid_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LINEBEFORE', (1,0), (1,0), 0.8, colors.HexColor('#000000')),
        ('LEFTPADDING', (0,0), (0,0), 0),
        ('RIGHTPADDING', (0,0), (0,0), 8),
        ('LEFTPADDING', (1,0), (1,0), 8),
        ('RIGHTPADDING', (1,0), (1,0), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(mid_table)
    story.append(Spacer(1, 6))

    # =========================================================================
    # 4. MÓDULO INFERIOR DE IMPACTO (Estilo módulo de portada de EL PAÍS)
    # =========================================================================
    alert_box = [
        [
            Paragraph(
                "<font color='#991B1B'><b>SOCIEDAD & SALUD</b></font><br/>"
                "<font size=10 color='#111827'><b>El tráfico de drogas sube un 20% en cinco años</b></font>",
                ParagraphStyle('ABoxL', parent=styles['Normal'], fontName=FONT_HEADLINE, fontSize=9, leading=12)
            ),
            Paragraph(
                "Un informe de las agencias de seguridad alerta de un incremento sostenido del 20% en la circulación de estupefacientes y psicofármacos sintéticos. "
                "Los investigadores vinculan este auge al blanqueo de capitales procedente de deudas de juego clandestino y extorsiones a familias acaudaladas.",
                ParagraphStyle('ABoxR', parent=styles['Normal'], fontName=FONT_BODY, fontSize=8, leading=10.5, textColor=colors.HexColor('#1F2937'))
            )
        ]
    ]
    t_alert = Table(alert_box, colWidths=[180, 367])
    t_alert.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#000000')),
        ('LINEBEFORE', (1,0), (1,0), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_alert)

    doc.build(story)
    print("5_periodico_dia.pdf generado con éxito:", output_filename)

if __name__ == '__main__':
    build_periodico_dia_pdf()

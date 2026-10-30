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
    create_photo_placeholder("src/assets/images/periodico_dia/foto_kronos.png", 520, 200, "[ FOTO 1: SEDE KRONOS S.A. ]", "Recapitalizacion de emergencia")
    create_photo_placeholder("src/assets/images/periodico_dia/foto_caballo.png", 320, 160, "[ FOTO 2: NUEVO PURASANGRE ]", "Circuito clandestino Apex")
    create_photo_placeholder("src/assets/images/periodico_dia/foto_israel.png", 320, 160, "[ FOTO 3: FOTOGRAFIA DE INTELIGENCIA ]", "Enlace militar en Tel Aviv")

    # A4 = 595.27 x 841.89 pt
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=A4,
        leftMargin=24,
        rightMargin=24,
        topMargin=14,
        bottomMargin=14
    )

    styles = getSampleStyleSheet()

    masthead_style = ParagraphStyle(
        'Masthead',
        parent=styles['Normal'],
        fontName=FONT_HEADLINE,
        fontSize=44,
        leading=46,
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
        leading=10,
        textColor=colors.HexColor('#1F2937')
    )

    # TITULAR DE APERTURA: MUERTE DEL MAGNATE
    breaking_tag = ParagraphStyle(
        'BTag',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9,
        textColor=colors.HexColor('#DC2626')
    )

    magnate_title = ParagraphStyle(
        'MagTitle',
        parent=styles['Heading1'],
        fontName=FONT_HEADLINE,
        fontSize=20,
        leading=23,
        textColor=colors.HexColor('#991B1B'),
        spaceBefore=1,
        spaceAfter=2
    )

    magnate_sub = ParagraphStyle(
        'MagSub',
        parent=styles['Normal'],
        fontName=FONT_ITALIC,
        fontSize=9.5,
        leading=12.5,
        textColor=colors.HexColor('#374151'),
        spaceAfter=4
    )

    # TITULAR KRONOS
    kronos_title = ParagraphStyle(
        'KronosTitle',
        parent=styles['Heading2'],
        fontName=FONT_HEADLINE,
        fontSize=15,
        leading=18,
        textColor=colors.HexColor('#111827'),
        spaceBefore=1,
        spaceAfter=2
    )

    kronos_sub = ParagraphStyle(
        'KronosSub',
        parent=styles['Normal'],
        fontName=FONT_ITALIC,
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#4B5563'),
        spaceAfter=4
    )

    # TITULARES SECUNDARIOS (HÍPICA E ISRAEL)
    sec_title = ParagraphStyle(
        'SecTitle',
        parent=styles['Heading2'],
        fontName=FONT_HEADLINE,
        fontSize=12.5,
        leading=15,
        textColor=colors.HexColor('#111827'),
        spaceBefore=1,
        spaceAfter=2
    )

    sec_subtitle = ParagraphStyle(
        'SecSub',
        parent=styles['Normal'],
        fontName=FONT_ITALIC,
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor('#4B5563'),
        spaceAfter=3
    )

    body_news = ParagraphStyle(
        'BodyNews',
        parent=styles['Normal'],
        fontName=FONT_BODY,
        fontSize=8,
        leading=11,
        alignment=4, # TA_JUSTIFY
        textColor=colors.HexColor('#1F2937')
    )

    caption_style = ParagraphStyle(
        'Caption',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.5,
        leading=8.5,
        textColor=colors.HexColor('#4B5563')
    )

    story = []

    # =========================================================================
    # 1. CABECERA: EL DIARIO DEL DÍA (Estilo EL PAÍS)
    # =========================================================================
    story.append(Paragraph("EL DIARIO DEL DÍA", masthead_style))
    story.append(Paragraph("EL PERIÓDICO GLOBAL DE INFORMACIÓN GENERAL Y FINANZAS", ParagraphStyle('SubM', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.5, leading=9, alignment=1, textColor=colors.HexColor('#4B5563'))))
    story.append(Spacer(1, 2))

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
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_top)
    story.append(Spacer(1, 4))

    # =========================================================================
    # 2. NOTICIA DE APERTURA: MUERTE SOSPECHOSA DEL MAGNATE VALPARAÍSO
    # =========================================================================
    story.append(Paragraph("<b>ÚLTIMA HORA • INVESTIGACIÓN JUDICIAL EN CURSO</b>", breaking_tag))
    story.append(Paragraph("Muere el magnate Valparaíso de forma sospechosa en su villa de 10 millones", magnate_title))
    story.append(Paragraph("La policía detiene temporalmente la investigación sobre el terreno tras la intervención formal de su equipo de abogados.", magnate_sub))

    magnate_col1 = (
        "<b>VALPARAÍSO ESTATE. —</b> El multimillonario y veterano patriarca <b>Ricardo Valparaíso</b> "
        "fue hallado sin vida anoche en el interior de su exclusiva mansión señorial, valorada en más de <b>10 millones de dólares</b>, "
        "en circunstancias que los primeros peritos catalogaron de <i>'altamente sospechosas'</i>.<br/><br/>"
        "Sin embargo, el operativo forense de la policía judicial se ha visto sorprendentemente <b>detenido de forma temporal</b> "
        "a primera hora de esta madrugada por orden judicial, a petición formal presentada por el despacho de abogados del difunto."
    )

    magnate_col2 = (
        "El equipo jurídico de la familia esgrimió estrictas cláusulas de confidencialidad y la inmediata apertura de la pieza "
        "testamentaria para paralizar temporalmente las pesquisas e interrogatorios en la vivienda.<br/><br/>"
        "La repentina muerte del magnate, rodeado únicamente por un selecto círculo de allegados convocados a una velada privada, "
        "ha disparado las especulaciones sobre la disputa de su millonaria herencia y acuerdos mercantiles pendientes."
    )

    t_magnate = Table([[
        Paragraph(magnate_col1, body_news),
        Paragraph(magnate_col2, body_news)
    ]], colWidths=[270, 275])
    t_magnate.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (0,0), 0),
        ('RIGHTPADDING', (0,0), (0,0), 8),
        ('LINEBEFORE', (1,0), (1,0), 0.5, colors.HexColor('#D1D5DB')),
        ('LEFTPADDING', (1,0), (1,0), 8),
        ('RIGHTPADDING', (1,0), (1,0), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_magnate)
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#000000'), spaceAfter=5))

    # =========================================================================
    # 3. NOTICIA ECONÓMICA: KRONOS REPUNTA UN 120% TRAS INYECCIÓN DE 12M$
    # =========================================================================
    kronos_left = [
        Paragraph("<font color='#047857'><b>MERCADOS FINANCIEROS</b></font>", ParagraphStyle('TagK', parent=breaking_tag, textColor=colors.HexColor('#047857'))),
        Paragraph("Kronos repunta un 120% en 12 horas", kronos_title),
        Paragraph("Una inyección nocturna de 12 millones de dólares de su accionista mayoritario salva a la corporación del embargo judicial.", kronos_sub),
        Paragraph(
            "<b>NUEVA YORK. —</b> En una de las jornadas más insólitas jamás presenciadas en Wall Street, el grupo "
            "<b>Kronos & Logística S.A.</b> protagonizó de madrugada un rebote vertical del <b>120%</b> tras haber tocado fondo bursátil la tarde anterior.<br/><br/>"
            "La Comisión de Mercados certificó una transferencia extraordinaria irrevocable de <b>12 millones de dólares</b> emitida por su socio de referencia, "
            "desactivando la orden de embargo cautelar dictada por el juzgado mercantil. La repentina aparición de los avales necesarios "
            "ha desatado intensas especulaciones sobre el origen de los fondos familiares.",
            body_news
        )
    ]

    kronos_photo_col = [
        Image("src/assets/images/periodico_dia/foto_kronos.png", width=245, height=88),
        Spacer(1, 2),
        Paragraph("Fachada de la sede central de Kronos en el distrito financiero tras suspenderse el preconcurso. / REUTERS", caption_style)
    ]

    hero_layout = Table([[kronos_left, kronos_photo_col]], colWidths=[295, 250])
    hero_layout.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LINEBEFORE', (1,0), (1,0), 0.5, colors.HexColor('#D1D5DB')),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (0,0), 8),
        ('LEFTPADDING', (1,0), (1,0), 8),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(hero_layout)
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#000000'), spaceAfter=5))

    # =========================================================================
    # 4. SECCIÓN MEDIA: DOS COLUMNAS (HÍPICA E INTERNACIONAL)
    # =========================================================================
    col_horse = [
        Paragraph("<font color='#991B1B'><b>HÍPICA Y APUESTAS</b></font>", ParagraphStyle('TagH', parent=breaking_tag)),
        Paragraph("Nuevo caballo en carreras clandestinas", sec_title),
        Paragraph("Adquieren a 'Sombra Veloz' tras la muerte por sobredosis del animal titular.", sec_subtitle),
        Image("src/assets/images/periodico_dia/foto_caballo.png", width=255, height=85),
        Spacer(1, 2),
        Paragraph("El ejemplar purasangre adquirido de madrugada en una subasta privada. / AP", caption_style),
        Spacer(1, 3),
        Paragraph(
            "<b>LOUISVILLE. —</b> Apenas unas horas después del fulminante colapso en boxes del caballo de carreras <i>'Tormenta Negra'</i> —cuya necropsia reveló una <b>dosis masiva de estimulantes no autorizados</b>—, "
            "el consorcio de apuestas clandestinas vinculado a Apex formalizó de urgencia la compraventa de un nuevo purasangre.<br/><br/>"
            "La operación, saldada íntegramente en metálico por jóvenes operadores nocturnos, confirma la presión apremiante por mantener abiertos los calendarios de apuestas amañadas.",
            body_news
        )
    ]

    col_israel = [
        Paragraph("<font color='#1E3A8A'><b>SEGURIDAD INTERNACIONAL</b></font>", ParagraphStyle('TagI', parent=breaking_tag, textColor=colors.HexColor('#1E3A8A'))),
        Paragraph("Captan en Israel a un traficante de armas", sec_title),
        Paragraph("Fotografiado en Oriente Próximo dos horas antes del anochecer.", sec_subtitle),
        Image("src/assets/images/periodico_dia/foto_israel.png", width=255, height=85),
        Spacer(1, 2),
        Paragraph("Registro gráfico filtrado por inteligencia militar cerca de Tel Aviv. / AFP", caption_style),
        Spacer(1, 3),
        Paragraph(
            "<b>TEL AVIV. —</b> Informes de inteligencia militar desclasificados esta mañana sitúan a un conocido intermediario de suministros bélicos cerrando un pacto clandestino de fusiles y munición en un enclave táctico de Oriente Próximo.<br/><br/>"
            "El registro gráfico fue captado <b>el día 30 a las 16:30 horas locales (apenas dos horas antes del anochecer en América)</b>, constatando que el enlace militar se encontraba a miles de kilómetros de suelo americano.",
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
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(mid_table)
    story.append(Spacer(1, 5))

    # =========================================================================
    # 5. MÓDULO INFERIOR: ALERTA SOCIAL DE DROGAS (+20%)
    # =========================================================================
    alert_box = [
        [
            Paragraph(
                "<font color='#991B1B'><b>SOCIEDAD & SALUD</b></font><br/>"
                "<font size=9.5 color='#111827'><b>El tráfico de drogas sube un 20% en cinco años</b></font>",
                ParagraphStyle('ABoxL', parent=styles['Normal'], fontName=FONT_HEADLINE, fontSize=9, leading=11.5)
            ),
            Paragraph(
                "Un informe de las agencias de seguridad alerta de un incremento sostenido del 20% en la circulación de estupefacientes y psicofármacos sintéticos. "
                "Los investigadores vinculan este auge al blanqueo de capitales procedente de deudas de juego clandestino y extorsiones a familias acaudaladas.",
                ParagraphStyle('ABoxR', parent=styles['Normal'], fontName=FONT_BODY, fontSize=7.5, leading=10, textColor=colors.HexColor('#1F2937'))
            )
        ]
    ]
    t_alert = Table(alert_box, colWidths=[180, 367])
    t_alert.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#000000')),
        ('LINEBEFORE', (1,0), (1,0), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_alert)

    doc.build(story)
    print("5_periodico_dia.pdf generado con éxito:", output_filename)

if __name__ == '__main__':
    build_periodico_dia_pdf()

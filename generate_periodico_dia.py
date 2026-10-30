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

# Registrar fuentes periodísticas auténticas
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
    im = PILImage.new('RGBA', (width_px, height_px), (242, 243, 245, 255))
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
    create_photo_placeholder("src/assets/images/periodico_dia/foto_kronos.png", 520, 220, "[ FOTO 1: SEDE KRONOS S.A. ]", "Recapitalizacion en Wall Street")
    create_photo_placeholder("src/assets/images/periodico_dia/foto_villa.png", 360, 210, "[ FOTO: VILLA VALPARAÍSO ]", "Cordon policial en la mansion")
    create_photo_placeholder("src/assets/images/periodico_dia/foto_caballo.png", 320, 160, "[ FOTO 2: NUEVO PURASANGRE ]", "Circuito clandestino Apex")
    create_photo_placeholder("src/assets/images/periodico_dia/foto_israel.png", 320, 160, "[ FOTO 3: FOTOGRAFIA DE INTELIGENCIA ]", "Enlace militar en Tel Aviv")

    # A4 = 595.27 x 841.89 pt. Usable width = 595.27 - 48 = 547.27 pt.
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=A4,
        leftMargin=24,
        rightMargin=24,
        topMargin=15,
        bottomMargin=15
    )

    styles = getSampleStyleSheet()

    # MASTHEAD PERIODÍSTICO (ESTILO EL PAÍS)
    masthead_style = ParagraphStyle(
        'Masthead',
        parent=styles['Normal'],
        fontName=FONT_HEADLINE,
        fontSize=48,
        leading=50,
        alignment=1,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=0,
        spaceAfter=0
    )

    meta_bar = ParagraphStyle(
        'MetaBar',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.2,
        leading=9.2,
        textColor=colors.HexColor('#1F2937')
    )

    section_tag = ParagraphStyle(
        'SecTag',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9,
        textColor=colors.HexColor('#991B1B')
    )

    # 1. KRONOS (NOTICIA PRINCIPAL / HERO)
    hero_title = ParagraphStyle(
        'HeroTitle',
        parent=styles['Heading1'],
        fontName=FONT_HEADLINE,
        fontSize=20.5,
        leading=23.5,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=1,
        spaceAfter=2
    )

    hero_subtitle = ParagraphStyle(
        'HeroSub',
        parent=styles['Normal'],
        fontName=FONT_ITALIC,
        fontSize=9.5,
        leading=12.5,
        textColor=colors.HexColor('#374151'),
        spaceAfter=3
    )

    # 2. MUERTE DEL MAGNATE (SEGUNDA NOTICIA - CON FOTO A LA IZQUIERDA)
    mag_title = ParagraphStyle(
        'MagTitle',
        parent=styles['Heading2'],
        fontName=FONT_HEADLINE,
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=1,
        spaceAfter=2
    )

    mag_subtitle = ParagraphStyle(
        'MagSub',
        parent=styles['Normal'],
        fontName=FONT_ITALIC,
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#4B5563'),
        spaceAfter=3
    )

    # 3. TITULARES SECUNDARIOS (HÍPICA E ISRAEL)
    sec_title = ParagraphStyle(
        'SecTitle',
        parent=styles['Heading2'],
        fontName=FONT_HEADLINE,
        fontSize=11.5,
        leading=14,
        textColor=colors.HexColor('#0f172a'),
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
        spaceAfter=2
    )

    body_news = ParagraphStyle(
        'BodyNews',
        parent=styles['Normal'],
        fontName=FONT_BODY,
        fontSize=7.8,
        leading=10.5,
        alignment=4, # Justified
        textColor=colors.HexColor('#1F2937')
    )

    caption_style = ParagraphStyle(
        'Caption',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.2,
        leading=8,
        textColor=colors.HexColor('#4B5563')
    )

    story = []

    # =========================================================================
    # 1. CABECERA: EL DIARIO DEL DÍA (ESTILO EL PAÍS)
    # =========================================================================
    top_bar = Table([[
        Paragraph("<font size=7 color='#4B5563'>www.eldiariodeldia.com</font>", ParagraphStyle('TL', parent=styles['Normal'])),
        Paragraph("<font size=7 color='#4B5563'>EL PERIÓDICO GLOBAL DE INFORMACIÓN GENERAL Y FINANZAS</font>", ParagraphStyle('TR', parent=styles['Normal'], alignment=2))
    ]], colWidths=[200, 347])
    top_bar.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
    ]))
    story.append(top_bar)

    story.append(Paragraph("EL DIARIO DEL DÍA", masthead_style))
    story.append(Spacer(1, 1))

    top_meta = [
        [
            Paragraph("SÁBADO 31 DE OCTUBRE DE 2026", meta_bar),
            Paragraph("AÑO XXVIII • NÚMERO 10.412", ParagraphStyle('MB1', parent=meta_bar, alignment=1)),
            Paragraph("EDICIÓN NACIONAL", ParagraphStyle('MB2', parent=meta_bar, alignment=1)),
            Paragraph("PRECIO: 2,00 $", ParagraphStyle('MB3', parent=meta_bar, alignment=2))
        ]
    ]
    t_top = Table(top_meta, colWidths=[155, 135, 140, 117])
    t_top.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,-1), 0.8, colors.HexColor('#000000')),
        ('LINEBELOW', (0,0), (-1,-1), 0.8, colors.HexColor('#000000')),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_top)
    story.append(Spacer(1, 3))

    # =========================================================================
    # 2. NOTICIA PRINCIPAL (HERO): KRONOS REPUNTA UN 120% EN 12 HORAS
    # =========================================================================
    story.append(Paragraph("<b>MERCADOS FINANCIEROS • WALL STREET</b>", section_tag))
    story.append(Paragraph("Kronos repunta un 120% en 12 horas", hero_title))
    story.append(Paragraph("Una inyección nocturna de 12 millones de dólares de su accionista mayoritario salva a la compañía del embargo judicial y reactiva sus operaciones.", hero_subtitle))

    kronos_col1 = (
        "<b>NUEVA YORK. —</b> En una de las jornadas más insólitas jamás presenciadas en Wall Street, el grupo "
        "<b>Kronos & Logística S.A.</b> protagonizó de madrugada un rebote vertical del <b>120%</b> tras haber tocado fondo bursátil la tarde previa.<br/><br/>"
        "La Comisión de Mercados certificó una transferencia extraordinaria irrevocable de <b>12 millones de dólares</b> emitida por su socio de referencia, "
        "desactivando la orden de embargo cautelar dictada por el juzgado mercantil. La repentina aparición de los avales necesarios "
        "ha desatado intensas especulaciones sobre el origen de los fondos aportados in extremis.<br/>"
        "<font size=6.5 color='#6B7280'>Pasa a la página 14 / Finanzas</font>"
    )

    kronos_col2 = (
        "La quiebra técnica amenazaba con arrastrar a una red de proveedores estratégicos y paralizar divisiones clave del sector logístico.<br/><br/>"
        "La dirección de Kronos aseguró en un escueto comunicado que la liquidez está garantizada y que la corporación afrontará de inmediato todas sus obligaciones financieras pendientes.<br/><br/>"
        "Analistas del sector califican el rescate de maniobra de manual de última hora, coordinada en vísperas del cierre trimestral de cuentas bancarias."
    )

    kronos_text_table = Table([[
        Paragraph(kronos_col1, body_news),
        Paragraph(kronos_col2, body_news)
    ]], colWidths=[144, 146])
    kronos_text_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (0,0), 6),
        ('LINEBEFORE', (1,0), (1,0), 0.5, colors.HexColor('#D1D5DB')),
        ('LEFTPADDING', (1,0), (1,0), 6),
        ('RIGHTPADDING', (1,0), (1,0), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))

    kronos_photo_col = [
        Image("src/assets/images/periodico_dia/foto_kronos.png", width=248, height=90),
        Spacer(1, 2),
        Paragraph("Fachada de la sede central de Kronos en el distrito financiero tras suspenderse el preconcurso de acreedores. / REUTERS", caption_style)
    ]

    hero_layout = Table([[kronos_text_table, kronos_photo_col]], colWidths=[297, 250])
    hero_layout.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LINEBEFORE', (1,0), (1,0), 0.5, colors.HexColor('#D1D5DB')),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (0,0), 8),
        ('LEFTPADDING', (1,0), (1,0), 8),
        ('RIGHTPADDING', (1,0), (1,0), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(hero_layout)
    story.append(Spacer(1, 3))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor('#000000'), spaceBefore=1, spaceAfter=3))

    # =========================================================================
    # 3. SEGUNDA NOTICIA: MUERTE SOSPECHOSA DEL MAGNATE (CON FOTO A LA IZQUIERDA)
    # =========================================================================
    story.append(Paragraph("<b>SUCESOS • DILIGENCIAS JUDICIALES</b>", ParagraphStyle('TagS', parent=section_tag, textColor=colors.HexColor('#1E3A8A'))))
    story.append(Paragraph("Muere de forma sospechosa el magnate Valparaíso en su villa", mag_title))
    story.append(Paragraph("La policía detiene temporalmente la investigación sobre el terreno por petición formal de sus abogados.", mag_subtitle))

    mag_photo_col = [
        Image("src/assets/images/periodico_dia/foto_villa.png", width=168, height=78),
        Spacer(1, 2),
        Paragraph("Patrullas y precinto policial en la entrada de la villa Valparaíso esta madrugada. / EFE", caption_style)
    ]

    mag_text1 = (
        "<b>VALPARAÍSO ESTATE. —</b> El multimillonario <b>Ricardo Valparaíso</b> fue hallado sin vida anoche en su mansión señorial de <b>10 millones de dólares</b>, "
        "en circunstancias que los primeros peritos forenses catalogaron de altamente sospechosas.<br/><br/>"
        "La policía judicial detuvo la inspección ocular a primera hora tras un formal requerimiento del equipo jurídico de la familia."
    )

    mag_text2 = (
        "El despacho legal alegó la apertura inmediata del protocolo testamentario y cláusulas de confidencialidad para precintar las dependencias privadas.<br/><br/>"
        "<i>«La defensa jurídica exige custodiar el archivo privado y suspender declaraciones de testigos hasta conocer el testamento.»</i><br/>"
        "<font size=6.5 color='#6B7280'>Pasa a la pág. 8 / Sucesos</font>"
    )

    t_magnate = Table([[
        mag_photo_col,
        Paragraph(mag_text1, body_news),
        Paragraph(mag_text2, body_news)
    ]], colWidths=[175, 185, 187])
    t_magnate.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (0,0), 6),
        ('LINEBEFORE', (1,0), (1,0), 0.5, colors.HexColor('#D1D5DB')),
        ('LEFTPADDING', (1,0), (1,0), 6),
        ('RIGHTPADDING', (1,0), (1,0), 6),
        ('LINEBEFORE', (2,0), (2,0), 0.5, colors.HexColor('#D1D5DB')),
        ('LEFTPADDING', (2,0), (2,0), 6),
        ('RIGHTPADDING', (2,0), (2,0), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_magnate)
    story.append(Spacer(1, 3))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor('#000000'), spaceBefore=1, spaceAfter=3))

    # =========================================================================
    # 4. SECCIÓN MEDIA: DOS COLUMNAS PERIODÍSTICAS CON FOTOS (HÍPICA E ISRAEL)
    # =========================================================================
    col_horse = [
        Paragraph("<b>HÍPICA Y APUESTAS</b>", section_tag),
        Paragraph("Nuevo caballo en carreras clandestinas", sec_title),
        Paragraph("Adquieren a 'Sombra Veloz' tras la sobredosis del animal titular.", sec_subtitle),
        Image("src/assets/images/periodico_dia/foto_caballo.png", width=254, height=80),
        Spacer(1, 2),
        Paragraph("Purasangre adquirido de madrugada en subasta privada. / AP", caption_style),
        Spacer(1, 2),
        Paragraph(
            "<b>LOUISVILLE. —</b> Apenas horas después del colapso del purasangre <i>'Tormenta Negra'</i> —cuya necropsia reveló una <b>dosis masiva de estimulantes no autorizados</b>—, "
            "el consorcio de apuestas clandestinas formalizó de urgencia la compraventa de un sustituto.<br/><br/>"
            "La operación en metálico confirma la presión por sostener el circuito ilegal de juego.",
            body_news
        )
    ]

    col_israel = [
        Paragraph("<b>SEGURIDAD INTERNACIONAL</b>", ParagraphStyle('TagI', parent=section_tag, textColor=colors.HexColor('#1E3A8A'))),
        Paragraph("Captan en Israel a un traficante de armas", sec_title),
        Paragraph("Fotografiado en Tel Aviv a las 16:30 horas (dos antes del anochecer).", sec_subtitle),
        Image("src/assets/images/periodico_dia/foto_israel.png", width=254, height=80),
        Spacer(1, 2),
        Paragraph("Registro de inteligencia militar en Oriente Próximo. / AFP", caption_style),
        Spacer(1, 2),
        Paragraph(
            "<b>TEL AVIV. —</b> Informes militares sitúan a un conocido intermediario de suministros bélicos cerrando un pacto en un enclave táctico de Oriente Próximo.<br/><br/>"
            "El registro fue captado el día 30 a las <b>16:30 h locales (dos horas antes de oscurecer en América)</b>, constatando que el enlace estaba a miles de kilómetros.",
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
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(mid_table)
    story.append(Spacer(1, 3))

    # =========================================================================
    # 5. MÓDULO INFERIOR DE IMPACTO SOCIAL (ESTILO CAJA EL PAÍS)
    # =========================================================================
    alert_box = [
        [
            Paragraph(
                "<font color='#991B1B'><b>SOCIEDAD & SALUD</b></font><br/>"
                "<font size=9 color='#0f172a'><b>El tráfico de drogas sube un 20% en cinco años</b></font>",
                ParagraphStyle('ABoxL', parent=styles['Normal'], fontName=FONT_HEADLINE, fontSize=8.5, leading=11)
            ),
            Paragraph(
                "Un informe de las agencias de seguridad alerta del alza del 20% en la circulación de psicofármacos sintéticos y estimulantes. "
                "Los investigadores vinculan este incremento al blanqueo de capitales procedente de apuestas clandestinas y extorsiones patrimoniales.",
                ParagraphStyle('ABoxR', parent=styles['Normal'], fontName=FONT_BODY, fontSize=7.5, leading=9.8, textColor=colors.HexColor('#1F2937'))
            )
        ]
    ]
    t_alert = Table(alert_box, colWidths=[175, 372])
    t_alert.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#000000')),
        ('LINEBEFORE', (1,0), (1,0), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_alert)

    doc.build(story)
    print("5_periodico_dia.pdf generado con éxito:", output_filename)

if __name__ == '__main__':
    build_periodico_dia_pdf()

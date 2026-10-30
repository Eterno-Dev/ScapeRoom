import os
import pymupdf
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.graphics.shapes import Drawing, Rect, String, Line
from PIL import Image as PILImage, ImageDraw

def create_photo_placeholder(filename, width_px, height_px, label, sublabel=""):
    im = PILImage.new('RGBA', (width_px, height_px), (243, 244, 246, 255))
    draw = ImageDraw.Draw(im)
    # Border
    draw.rectangle((0, 0, width_px - 1, height_px - 1), outline="#9ca3af", width=2)
    # Diagonal subtle camera / placeholder graphic
    cx, cy = width_px // 2, height_px // 2 - 12
    draw.rectangle((cx - 24, cy - 16, cx + 24, cy + 16), outline="#6b7280", width=2)
    draw.ellipse((cx - 10, cy - 10, cx + 10, cy + 10), outline="#6b7280", width=2)
    draw.ellipse((cx + 12, cy - 12, cx + 18, cy - 6), fill="#6b7280")
    
    # Text
    draw.text((cx - len(label)*3.5, cy + 24), label, fill="#374151")
    if sublabel:
        draw.text((cx - len(sublabel)*3, cy + 38), sublabel, fill="#6b7280")
    im.save(filename)
    return filename

def build_periodico_dia_pdf(output_filename="5_periodico_dia.pdf"):
    # Create 3 placeholder images
    os.makedirs("src/assets/images/periodico_dia", exist_ok=True)
    p1 = create_photo_placeholder("src/assets/images/periodico_dia/foto_kronos.png", 520, 260, "[ FOTO 1: SEDE CENTRAL KRONOS S.A. ]", "Recapitalización de emergencia")
    p2 = create_photo_placeholder("src/assets/images/periodico_dia/foto_caballo.png", 320, 200, "[ FOTO 2: NUEVO PURASANGRE ]", "Circuito de carreras")
    p3 = create_photo_placeholder("src/assets/images/periodico_dia/foto_israel.png", 320, 200, "[ FOTO 3: INTELIGENCIA MILITAR ]", "Enlace en Oriente Próximo")

    # Document setup: A4 = 595.27 x 841.89 pt.
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=A4,
        leftMargin=25,
        rightMargin=25,
        topMargin=14,
        bottomMargin=14
    )

    styles = getSampleStyleSheet()

    # Tipografías estilo prensa clásica
    masthead_style = ParagraphStyle(
        'Masthead',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=44,
        leading=46,
        alignment=1,
        textColor=colors.HexColor('#000000'),
        spaceBefore=2,
        spaceAfter=2
    )

    dateline_style = ParagraphStyle(
        'Dateline',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#1F2937')
    )

    hero_head = ParagraphStyle(
        'HeroHead',
        parent=styles['Heading1'],
        fontName='Times-Bold',
        fontSize=18,
        leading=21,
        alignment=1,
        textColor=colors.HexColor('#991B1B'),
        spaceBefore=2,
        spaceAfter=2
    )

    hero_sub = ParagraphStyle(
        'HeroSub',
        parent=styles['Normal'],
        fontName='Times-Italic',
        fontSize=9.5,
        leading=12,
        alignment=1,
        textColor=colors.HexColor('#374151'),
        spaceAfter=5
    )

    sec_head = ParagraphStyle(
        'SecHead',
        parent=styles['Heading2'],
        fontName='Times-Bold',
        fontSize=11.5,
        leading=14,
        textColor=colors.HexColor('#111827'),
        spaceBefore=2,
        spaceAfter=2
    )

    sec_sub = ParagraphStyle(
        'SecSub',
        parent=styles['Normal'],
        fontName='Times-Italic',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor('#4B5563'),
        spaceAfter=3
    )

    body_news = ParagraphStyle(
        'BodyNews',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=8.5,
        leading=11.5,
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

    alert_head = ParagraphStyle(
        'AlertHead',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#991B1B')
    )

    alert_body = ParagraphStyle(
        'AlertBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor('#1F2937')
    )

    story = []

    # =========================================================================
    # 1. CABECERA MASTHEAD "EL DIARIO DEL DÍA" (Estilo periódico nacional)
    # =========================================================================
    top_meta = [
        [
            Paragraph("<b>EDICIÓN MATINAL NACIONAL • INFORMACIÓN GENERAL Y FINANZAS</b>", dateline_style),
            Paragraph("<b>SÁBADO, 31 DE OCTUBRE DE 2026 • PRECIO: 2,50 $ • AÑO XXXIV • Nº 12.049</b>", ParagraphStyle('TopMetaR', parent=dateline_style, alignment=2))
        ]
    ]
    t_top_meta = Table(top_meta, colWidths=[335, 210])
    t_top_meta.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 1.2, colors.HexColor('#000000')),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_top_meta)

    # Masthead principal
    story.append(Paragraph("EL DIARIO DEL DÍA", masthead_style))
    story.append(Paragraph("EL GRAN PERIÓDICO INDEPENDIENTE DE LA MAÑANA — NOTICIAS, MERCADOS Y ACTUALIDAD", ParagraphStyle('SubM', parent=styles['Normal'], fontName='Times-Italic', fontSize=8.5, leading=10.5, alignment=1, textColor=colors.HexColor('#4B5563'))))
    story.append(Spacer(1, 3))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#000000'), spaceAfter=6))

    # =========================================================================
    # 2. NOTICIA PRINCIPAL (HERO): REBOTE DEL 120% DE KRONOS TRAS INYECCIÓN DE 12M$
    # =========================================================================
    story.append(Paragraph("KRONOS S.A. PROTAGONIZA UN REBOTE HISTÓRICO DEL 120% EN BOLSA EN 12 HORAS TRAS UNA INYECCIÓN DE 12 MILLONES DE DÓLARES", hero_head))
    story.append(Paragraph("El rescate patrimonial aportado a última hora por el accionista mayoritario suspende el embargo judicial y salva a la entidad de la quiebra técnica.", hero_sub))

    kronos_text_left = (
        "<b>NUEVA YORK / WALL STREET.</b> En un giro tan vertiginoso como inesperado, el conglomerado empresarial <b>Grupo Kronos & Logística S.A.</b> "
        "ha remontado su desplome del día anterior con un repunte histórico del <b>120% en apenas doce horas de negociación</b> en los parqués internacionales.<br/><br/>"
        "La Comisión de Supervisión de Mercados ha confirmado que la operación de salvamento fue formalizada en la medianoche mediante la entrada irrevocable de "
        "<b>12 millones de dólares en fondos de capital privado</b> aportados por su socio y avalista financiero de referencia. "
        "Con este aporte extraordinario de liquidez, el Juzgado Mercantil ha dejado en suspenso la orden de intervención forzosa de activos."
    )

    kronos_text_mid = (
        "Fuentes de la junta directiva han evitado detallar el origen inmediato de las garantías patrimoniales que permitieron desbloquear el rescate, "
        "si bien confirman que la deuda corporativa vencida queda provisionalmente saldada.<br/><br/>"
        "Analistas del sector logístico califican la maniobra de <i>'salvamento in extremis de manual'</i>, coincidiendo con las febriles reuniones celebradas "
        "la tarde previa en residencias privadas de la alta sociedad."
    )

    kronos_left_col = [
        Paragraph(kronos_text_left, body_news),
        Spacer(1, 4),
        Paragraph(kronos_text_mid, body_news)
    ]

    kronos_right_col = [
        Image("src/assets/images/periodico_dia/foto_kronos.png", width=245, height=95),
        Spacer(1, 2),
        Paragraph("<b>Fotografía 1:</b> Sede central de Kronos S.A. en el distrito financiero tras el levantamiento judicial.", caption_style)
    ]

    t_hero = Table([[kronos_left_col, kronos_right_col]], colWidths=[290, 255])
    t_hero.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LINEBEFORE', (1,0), (1,0), 0.5, colors.HexColor('#D1D5DB')),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (0,0), 8),
        ('LEFTPADDING', (1,0), (1,0), 8),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_hero)
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#000000'), spaceAfter=5))

    # =========================================================================
    # 3. MITAD INFERIOR DIVIDIDA EN DOS GRANDES REPORTAJES + RECUADRO DE DROGAS
    # =========================================================================

    # SECCIÓN CABALLOS / APUESTAS AMAÑADAS (NIETO)
    caballo_content = [
        Paragraph("<b>HÍPICA Y APUESTAS CLANDESTINAS</b>", ParagraphStyle('Tag1', parent=dateline_style, fontSize=7.5, textColor=colors.HexColor('#991B1B'))),
        Paragraph("UN NUEVO PURASANGRE SE UNE AL EQUIPO DE CARRERAS TRAS LA MUERTE SOSPECHOSA DEL CAMPEÓN ANTERIOR", sec_head),
        Paragraph("El sindicato de apuestas adquiere a 'Sombra Veloz' tras el colapso por sobredosis de estimulantes del animal titular.", sec_sub),
        Image("src/assets/images/periodico_dia/foto_caballo.png", width=255, height=95),
        Spacer(1, 2),
        Paragraph("<b>Fotografía 2:</b> Nuevo purasangre adquirido para el circuito clandestino de carreras.", caption_style),
        Spacer(1, 3),
        Paragraph(
            "<b>KENTUCKY / REDACCIÓN.</b> Apenas horas después del misterioso deceso en los establos del cotizado caballo <i>'Tormenta Negra'</i>, "
            "cuyos primeros análisis toxicológicos apuntan a una <b>sobredosis letal de sustancias dopantes</b> suministradas para forzar su rendimiento, "
            "el consorcio privado de apuestas vinculado a Apex ha presentado formalmente a su nuevo purasangre titular.<br/><br/>"
            "La vertiginosa compraventa en metálico, orquestada de madrugada por jóvenes operadores del entorno de apuestas, "
            "ha levantado las sospechas de fraudes continuados en carreras amañadas.",
            body_news
        )
    ]

    # SECCIÓN VENDEDOR DE ARMAS EN ISRAEL (GENERAL)
    israel_content = [
        Paragraph("<b>EXCLUSIVA INTERNACIONAL • SEGURIDAD MILITAR</b>", ParagraphStyle('Tag2', parent=dateline_style, fontSize=7.5, textColor=colors.HexColor('#1E3A8A'))),
        Paragraph("CAPTAN A UN VENDEDOR DE ARMAS ANÓNIMO CERRANDO UN PACTO CON MANDOS EN ISRAEL HORAS ANTES DE LA REUNIÓN", sec_head),
        Paragraph("Imágenes de inteligencia confirman la presencia del enlace en Oriente Próximo el día 30, a miles de kilómetros.", sec_sub),
        Image("src/assets/images/periodico_dia/foto_israel.png", width=255, height=95),
        Spacer(1, 2),
        Paragraph("<b>Fotografía 3:</b> Registro gráfico captado por agencias de seguridad cerca de Tel Aviv.", caption_style),
        Spacer(1, 3),
        Paragraph(
            "<b>JERUSALÉN / TEL AVIV.</b> Informes confidenciales de inteligencia militar han filtrado una fotografía donde se identifica a un "
            "vendedor y mediador de armamento negociando un suministro táctico de fusiles y munición con mandos del frente regional.<br/><br/>"
            "El encuentro tuvo lugar <b>el día 30 a las 16:30 horas locales (dos horas antes del anochecer en América)</b>, lo que constata "
            "su estancia física en Oriente Próximo en dicha jornada. Las agencias rastrean el origen militar de los pertrechos.",
            body_news
        )
    ]

    bottom_split = Table([[caballo_content, israel_content]], colWidths=[265, 275])
    bottom_split.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LINEBEFORE', (1,0), (1,0), 0.8, colors.HexColor('#000000')),
        ('LEFTPADDING', (0,0), (0,0), 0),
        ('RIGHTPADDING', (0,0), (0,0), 8),
        ('LEFTPADDING', (1,0), (1,0), 8),
        ('RIGHTPADDING', (1,0), (1,0), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(bottom_split)
    story.append(Spacer(1, 6))

    # =========================================================================
    # 4. RECUADRO INFERIOR DE IMPACTO SOCIAL: AUMENTO DE DROGAS (+20%)
    # =========================================================================
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#991B1B'), spaceAfter=4))
    
    alert_box_data = [
        [
            Paragraph("<b>ALERTA SOCIAL & SALUD PÚBLICA:</b>", alert_head),
            Paragraph(
                "<b>EL CONSUMO Y TRÁFICO ILEGAL DE ESTUPEFACIENTES SE INCREMENTA UN 20% EN LA SOCIEDAD EN EL ÚLTIMO QUINQUENIO</b> — "
                "Informes del departamento antidroga revelan una correlación alarmante entre las redes de tráfico de pastillas estimulantes no reguladas, "
                "las deudas de juego clandestino juvenil y operaciones encubiertas de extorsión patrimonial en las grandes urbes.",
                alert_body
            )
        ]
    ]
    t_alert = Table(alert_box_data, colWidths=[150, 395])
    t_alert.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FEF2F2')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#DC2626')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_alert)

    doc.build(story)
    print("Periódico del Día generado con éxito:", output_filename)

if __name__ == '__main__':
    build_periodico_dia_pdf()

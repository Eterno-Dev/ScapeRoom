import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from PIL import Image as PILImage, ImageDraw

# =============================================================================
# 0. PREPARAR IMAGEN ANOTADA DE LA AUTOPSIA
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
    draw.ellipse((cx-45, cy-45, cx+45, cy+45), outline="#dc2626", width=12)
    draw.ellipse((cx-16, cy-16, cx+16, cy+16), fill="#dc2626")
    
    # Línea indicadora
    draw.line((cx+45, cy, cx+220, cy-60), fill="#dc2626", width=8)
    
    # Cuadro informativo estilizado
    draw.rectangle((cx+220, cy-130, cx+580, cy+30), fill=(255, 255, 255, 250), outline="#dc2626", width=6)
    
    draw.text((cx+235, cy-115), "BRECHA OCCIPITAL (18:30 H)", fill="#991b1b")
    draw.text((cx+235, cy-80), "Traumatismo contuso severo", fill="#1f2937")
    draw.text((cx+235, cy-50), "Impacto seco por caida libre", fill="#1f2937")
    draw.text((cx+235, cy-20), "Fractura deprimida en base", fill="#1f2937")

    # Etiquetas de vista inferior
    draw.text((380, 1880), "VISTA ANTERIOR (FRENTE)", fill="#4b5563")
    draw.text((1180, 1880), "VISTA POSTERIOR (ESPALDA)", fill="#4b5563")

    im.save(out_path)
    return out_path

prepare_annotated_body()

styles = getSampleStyleSheet()

# Tipografías base
form_label = ParagraphStyle(
    'FormLabel',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=7.5,
    leading=9.5,
    textColor=colors.HexColor('#1F2937')
)

form_val_typewriter = ParagraphStyle(
    'FormValTypewriter',
    parent=styles['Normal'],
    fontName='Courier-Bold',
    fontSize=8.5,
    leading=10.5,
    textColor=colors.HexColor('#0F172A')
)

form_desc_typewriter = ParagraphStyle(
    'FormDescTypewriter',
    parent=styles['Normal'],
    fontName='Courier',
    fontSize=7.5,
    leading=10,
    textColor=colors.HexColor('#1E293B')
)

# =============================================================================
# 1. GENERAR DOCUMENTO 1: AUTOPSIA FORENSE (1 PÁGINA)
# =============================================================================
def generate_autopsia_pdf(output_filename="1_autopsia_forense.pdf"):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=A4,
        leftMargin=30,
        rightMargin=30,
        topMargin=26,
        bottomMargin=26
    )

    story = []

    # Cabecera Estilo Medical Examiner (Captura 2)
    header_style1 = ParagraphStyle(
        'Head1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=12,
        alignment=1,
        textColor=colors.HexColor('#111827')
    )
    header_style2 = ParagraphStyle(
        'Head2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=15,
        alignment=1,
        textColor=colors.HexColor('#000000')
    )
    header_style3 = ParagraphStyle(
        'Head3',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        alignment=1,
        textColor=colors.HexColor('#4B5563')
    )

    story.append(Paragraph("DEPARTAMENTO DE POLICÍA JUDICIAL — DIVISIÓN DE MEDICINA LEGAL", header_style1))
    story.append(Paragraph("INFORME DE INVESTIGACIÓN MÉDICO FORENSE PRELIMINAR", header_style2))
    story.append(Paragraph("REPORT OF INVESTIGATION BY COUNTY MEDICAL EXAMINER — REF: 2026-F892", header_style3))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#000000'), spaceAfter=5))

    # Formulario Fila 1: Datos Personales
    r1 = [
        [
            Paragraph("<b>FALLECIDO:</b> <font name='Courier-Bold'>Ricardo Valparaíso</font>", form_label),
            Paragraph("<b>RAZA:</b> <font name='Courier-Bold'>Caucásica</font>", form_label),
            Paragraph("<b>SEXO:</b> <font name='Courier-Bold'>M</font>", form_label),
            Paragraph("<b>EDAD:</b> <font name='Courier-Bold'>72</font>", form_label)
        ]
    ]
    t1 = Table(r1, colWidths=[240, 110, 85, 100])
    t1.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 0.8, colors.HexColor('#000000')),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t1)

    # Formulario Fila 2: Hora y Lugar
    r2 = [
        [
            Paragraph("<b>HORA DE LA MUERTE:</b> <font name='Courier-Bold' color='#991B1B'><b>18:30 HORAS</b></font>", form_label),
            Paragraph("<b>LUGAR DEL HALLAZGO:</b> <font name='Courier-Bold'>Finca Señorial Valparaíso</font>", form_label)
        ]
    ]
    t2 = Table(r2, colWidths=[240, 295])
    t2.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 0.8, colors.HexColor('#000000')),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t2)

    # Formulario Fila 3: Tipo de Muerte (Checkboxes como captura 2)
    cb_text = (
        "<b>TIPO DE MUERTE:</b>&nbsp;&nbsp;&nbsp;&nbsp;"
        "TRAUMÁTICA [ ]&nbsp;&nbsp;&nbsp;&nbsp;"
        "SUICIDIO [ ]&nbsp;&nbsp;&nbsp;&nbsp;"
        "SÚBITA [ ]&nbsp;&nbsp;&nbsp;&nbsp;"
        "HALLAZGO [ ]&nbsp;&nbsp;&nbsp;&nbsp;"
        "<b>SOSPECHOSA [<font name='Courier-Bold' color='#991B1B'>X</font>]</b>&nbsp;&nbsp;&nbsp;&nbsp;"
        "<b>NO NATURAL [<font name='Courier-Bold' color='#991B1B'>X</font>]</b>"
    )
    r3 = [[Paragraph(cb_text, form_label)]]
    t3 = Table(r3, colWidths=[535])
    t3.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 1.2, colors.HexColor('#000000')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t3)
    story.append(Spacer(1, 4))

    # Formulario Fila 4: Descripción del Cuerpo
    r4 = [
        [
            Paragraph("<b>ALTURA:</b> <font name='Courier-Bold'>1.76 m</font>", form_label),
            Paragraph("<b>PESO:</b> <font name='Courier-Bold'>78 kg</font>", form_label),
            Paragraph("<b>PELO:</b> <font name='Courier-Bold'>Cano</font>", form_label),
            Paragraph("<b>OJOS:</b> <font name='Courier-Bold'>Marrones</font>", form_label)
        ],
        [
            Paragraph("<b>VESTIMENTA:</b> <font name='Courier-Bold'>Traje formal oscuro de etiqueta</font>", form_label),
            Paragraph("<b>ACCESORIOS:</b> <font name='Courier-Bold'>Sin reloj de bolsillo ni sortija</font>", form_label),
            Paragraph("", form_label),
            Paragraph("", form_label)
        ]
    ]
    t4 = Table(r4, colWidths=[135, 120, 140, 140])
    t4.setStyle(TableStyle([
        ('SPAN', (1,1), (3,1)),
        ('LINEBELOW', (0,1), (-1,1), 0.8, colors.HexColor('#000000')),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t4)
    story.append(Spacer(1, 5))

    # CUERPO PRINCIPAL: COLUMNA IZQUIERDA (HERIDAS Y TOXICOLOGÍA) + COLUMNA DERECHA (IMAGEN ANOTADA)
    left_flowables = [
        Paragraph("<b>MARCAS Y HERIDAS TRAUMÁTICAS (MARKS AND WOUNDS):</b>", form_label),
        Spacer(1, 2),
        Paragraph("• <font name='Courier-Bold'>LESIÓN CRANEAL:</font> Brecha contusa profunda de 5.2 cm en región occipital izquierda. Fractura conminuta en base de cráneo con hemorragia subaracnoidea inmediata. Consistente con impacto violento contra plano rígido tras caída de espaldas.", form_desc_typewriter),
        Spacer(1, 3),
        Paragraph("• <font name='Courier-Bold'>DESCARTE BALÍSTICO:</font> CERO orificios de entrada o salida de proyectil en piel o vísceras. Ausencia total de metralla o pólvora incrustada.", form_desc_typewriter),
        Spacer(1, 3),
        Paragraph("• <font name='Courier-Bold'>DESCARTE DE ARMA BLANCA:</font> No se aprecian incisiones punzantes, heridas por estilete, tijeras ni herramientas.", form_desc_typewriter),
        Spacer(1, 6),
        HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#9CA3AF'), spaceAfter=4),
        Paragraph("<b>RESULTADOS TOXICOLÓGICOS (TOXICOLOGY RESULTS):</b>", form_label),
        Spacer(1, 2),
        Paragraph("• <font name='Courier-Bold'>SUSTANCIA DETECTADA:</font> Compuesto activo en torrente sanguíneo cuantificado en <font color='#991B1B'><b>42.5 mg/L</b></font>.", form_desc_typewriter),
        Spacer(1, 3),
        Paragraph("• <font name='Courier-Bold'>IDENTIFICACIÓN QUÍMICA:</font> No catalogada en cribado preliminar. El laboratorio forense no ha aislado el principio activo.", form_desc_typewriter),
        Spacer(1, 3),
        Paragraph("• <font name='Courier-Bold'>NOTA FACULTATIVA:</font> Un profesional médico debe cotejar esta concentración (42.5 mg/L) con la farmacopea para dictaminar si la dosis administrada era letal o insuficiente.", form_desc_typewriter),
    ]

    img_annotated_path = "src/assets/images/bg_men_annotated.png"
    right_flowables = [
        Paragraph("<b>MAPA CORPORAL DE LESIONES (ESQUEMA OFICIAL)</b>", ParagraphStyle('DiagH', parent=form_label, alignment=1)),
        Spacer(1, 2),
        Image(img_annotated_path, width=225, height=248)
    ]

    split_data = [[left_flowables, right_flowables]]
    split_table = Table(split_data, colWidths=[295, 240])
    split_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#000000')),
        ('INNERGRID', (0,0), (-1,-1), 0.8, colors.HexColor('#000000')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(split_table)
    story.append(Spacer(1, 5))

    # CONCLUSIONES INFERIORES: CAUSA PROBABLE Y ACCIONES (Como Captura 2)
    bottom_boxes = [
        [
            Paragraph("<b>CAUSA PROBABLE DE LA MUERTE (PROBABLE CAUSE OF DEATH):</b>", form_label),
            Paragraph("<b>ACCIONES COMPLEMENTARIAS (FURTHER ACTION):</b>", form_label)
        ],
        [
            Paragraph("<font name='Courier-Bold'>TRAUMATISMO CRANEOENCEFÁLICO SEVERO (18:30 H).<br/>Shock irreversible producido por fractura occipital consecutiva a colapso y caída violenta hacia atrás.<br/>Intoxicación por compuesto químico sin determinar.</font>", form_desc_typewriter),
            Paragraph("<font name='Courier-Bold'>1. Peritaje toxicológico urgente por especialista.<br/>2. Cotejo de la medicación incautada en la vivienda.<br/>3. Custodia de casquillos y evidencias perimetrales.</font>", form_desc_typewriter)
        ]
    ]
    t_bottom = Table(bottom_boxes, colWidths=[310, 225])
    t_bottom.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#000000')),
        ('INNERGRID', (0,0), (-1,-1), 0.8, colors.HexColor('#000000')),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F3F4F6')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_bottom)
    story.append(Spacer(1, 5))

    # Declaración jurada y firmas
    decl = (
        "DECLARO BAJO JURAMENTO QUE HE ASUMIDO EL EXAMEN FORENSE DEL CADÁVER CONFORME A LA LEY Y QUE "
        "LOS DATOS Y DESCRIPCIONES REFLEJAN LA TOTALIDAD DE LOS HALLAZGOS FÍSICOS Y TOXICOLÓGICOS OBSERVADOS."
    )
    story.append(Paragraph(f"<font size=6.5 color='#374151'>{decl}</font>", styles['Normal']))
    story.append(Spacer(1, 4))

    sig_row = [
        [
            Paragraph("<b>FECHA:</b> <font name='Courier-Bold'>30 de Octubre de 2026</font>", form_label),
            Paragraph("<b>LUGAR:</b> <font name='Courier-Bold'>Juzgado de Instrucción Especial</font>", form_label),
            Paragraph("<b>FIRMA PERITO FORENSE:</b> <font name='Courier-Bold'><i>Dra. Isabel Ortega / Dr. Alfonso Rivas</i></font>", form_label)
        ]
    ]
    t_sig = Table(sig_row, colWidths=[150, 185, 200])
    t_sig.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,-1), 0.8, colors.HexColor('#000000')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_sig)

    doc.build(story)
    print("Documento 1 generado:", output_filename)

# =============================================================================
# 2. GENERAR DOCUMENTO 2: PERIÓDICO "WARBES" + EXTRACTO BANCARIO (1 PÁGINA)
# =============================================================================
def generate_warbes_pdf(output_filename="2_periodico_warbes.pdf"):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=A4,
        leftMargin=30,
        rightMargin=30,
        topMargin=26,
        bottomMargin=26
    )

    story = []

    # CABECERA ESTILO FORBES / DAILY TIMES: "WARBES"
    meta_top = [
        [
            Paragraph("<b>OCTUBRE 2026 • EDICIÓN ESPECIAL FINANCIERA</b>", ParagraphStyle('WTopL', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor('#374151'))),
            Paragraph("<b>PRECIO: 4,50 € • VOL. XLII</b>", ParagraphStyle('WTopR', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8, alignment=2, textColor=colors.HexColor('#374151')))
        ]
    ]
    t_meta = Table(meta_top, colWidths=[265, 270])
    t_meta.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 1, colors.HexColor('#000000')),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_meta)

    # TITULAR GIGANTE "WARBES"
    warbes_title = ParagraphStyle(
        'WarbesMasthead',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=38,
        leading=40,
        alignment=1,
        textColor=colors.HexColor('#000000'),
        spaceBefore=2,
        spaceAfter=2
    )
    story.append(Paragraph("WARBES", warbes_title))

    warbes_sub = ParagraphStyle(
        'WarbesSub',
        parent=styles['Normal'],
        fontName='Times-Italic',
        fontSize=8.5,
        leading=10.5,
        alignment=1,
        textColor=colors.HexColor('#4B5563'),
        spaceAfter=5
    )
    story.append(Paragraph("THE GLOBAL FINANCIAL & WEALTH CHRONICLE — CRÓNICA DE MERCADOS Y PATRIMONIOS", warbes_sub))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#000000'), spaceAfter=8))

    # TITULAR PRINCIPAL EN ROJO Y NEGRO
    headline_style = ParagraphStyle(
        'WarbesHead',
        parent=styles['Heading1'],
        fontName='Times-Bold',
        fontSize=15,
        leading=18,
        alignment=0,
        textColor=colors.HexColor('#991B1B'),
        spaceAfter=6
    )
    story.append(Paragraph("¡HISTÓRICO COLAPSO! EL GRUPO MERCANTIL DÁVILA ENTRA EN QUIEBRA TÉCNICA TRAS DESPLOMARSE SUS ACCIONES", headline_style))

    # CUERPO DEL PERIÓDICO (COLUMNA NOTICIA + GRÁFICA REAL)
    grafica_path = "src/assets/images/grafica.png"
    news_text = (
        "<b>MADRID / ZÚRICH.</b> La sociedad mercantil de inversiones familiares <i>Dávila Corp</i>, "
        "administrada por el entorno directo de la familia, ha protagonizado este mediodía una de las caídas más "
        "abruptas registradas en los mercados de valores este año, perdiendo más del <b>82% de su capitalización bursátil</b>.<br/><br/>"
        "Los tribunales mercantiles han advertido que iniciarán el <b>procedimiento concursal de liquidación y embargo forzoso</b> "
        "de bienes si la dirección de la entidad no aporta una inyección inmediata y desesperada de al menos dos millones de euros antes del fin de mes. "
        "Fuentes próximas al caso confirman que la dirección mercantil intentó desesperadamente recabar fondos personales de la familia para frenar el embargo inminente."
    )

    art_style = ParagraphStyle(
        'ArtStyle',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#1F2937')
    )

    left_article = [
        Paragraph(news_text, art_style),
        Spacer(1, 6),
        Paragraph("<b>CRECEN LAS SANCIONES POR PLATAFORMAS CLANDESTINAS DE APUESTAS (APEX BETS)</b>", ParagraphStyle('SideHead', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor('#111827'))),
        Paragraph("<font size=7.5 color='#4B5563'>Las autoridades de supervisión financiera investigan plataformas telemáticas internacionales empleadas para saldar deudas de juego bajo intimidación física.</font>", styles['Normal'])
    ]

    right_chart = [
        Image(grafica_path, width=240, height=128),
        Spacer(1, 2),
        Paragraph("<font size=7 color='#6B7280'><b>Gráfica 1:</b> Evolución vertical de la cotización de acciones de Dávila Corp (desplome total en 72 h).</font>", styles['Normal'])
    ]

    news_layout = Table([[left_article, right_chart]], colWidths=[285, 250])
    news_layout.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(news_layout)
    story.append(Spacer(1, 10))

    # SEGUNDA MITAD: EXTRACTO BANCARIO OFICIAL
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#000000'), spaceAfter=6))
    story.append(Paragraph("BANCO CENTRAL PRIVADO — EXTRACTO OFICIAL DE MOVIMIENTOS BANCARIOS", ParagraphStyle('BankTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor('#111827'))))
    story.append(Paragraph("<b>TITULAR:</b> D. Ricardo Valparaíso | <b>CUENTA MATRIZ:</b> ES33 0049 1800 5511 2233 4455 | <b>FECHA:</b> 30 de Octubre de 2026", styles['Normal']))
    story.append(Spacer(1, 6))

    bank_rows = [
        [
            Paragraph("<b>HORA REGISTRO</b>", form_label),
            Paragraph("<b>OPERACIÓN / CONCEPTO</b>", form_label),
            Paragraph("<b>CUENTA / CANAL DESTINO</b>", form_label),
            Paragraph("<b>IMPORTE</b>", form_label)
        ],
        [
            Paragraph("<font name='Courier-Bold'>17:45:10</font>", form_desc_typewriter),
            Paragraph("TRANSFERENCIA EXTRAORDINARIA URGENTE<br/><font size=7 color='#6B7280'>Ref: Rescate societario / Inyección de capital Dávila Corp</font>", form_desc_typewriter),
            Paragraph("ES84 2100 0418 9012 3456 7890<br/><font size=7 color='#6B7280'>Oficina Central Mercantil</font>", form_desc_typewriter),
            Paragraph("<font name='Courier-Bold' color='#991B1B'><b>- 1.850.000,00 €</b></font>", form_desc_typewriter)
        ],
        [
            Paragraph("<font name='Courier-Bold' color='#991B1B'><b>18:28:44</b></font><br/><font size=6.5 color='#991B1B'><b>(Minutos antes)</b></font>", form_desc_typewriter),
            Paragraph("TRANSFERENCIA TELEMÁTICA INMEDIATA IP-REMOTA<br/><font size=7 color='#6B7280'>Ref: Liquidación saldo cuenta #9942 - Apex Bets</font>", form_desc_typewriter),
            Paragraph("ES12 0049 1823 4498 7654 3210<br/><font size=7 color='#6B7280'>Terminal de Banca Móvil Remota</font>", form_desc_typewriter),
            Paragraph("<font name='Courier-Bold' color='#991B1B'><b>- 14.250,00 €</b></font>", form_desc_typewriter)
        ]
    ]

    t_bank = Table(bank_rows, colWidths=[95, 205, 145, 90])
    t_bank.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F3F4F6')),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#FFFFFF')),
        ('BACKGROUND', (0,2), (-1,2), colors.HexColor('#FEF2F2')), # Alerta sutil en la de las 18:28
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#000000')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D1D5DB')),
        ('ALIGN', (3,0), (3,-1), 'RIGHT'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_bank)
    story.append(Spacer(1, 8))

    bank_audit_note = (
        "<b>AUDITORÍA DE SEGURIDAD TELEMÁTICA:</b> La transferencia de <b>-14.250,00 € emitida a las 18:28:44 horas</b> "
        "(escasos minutos antes del fallecimiento fijado a las 18:30) fue confirmada mediante verificación biométrica en un terminal "
        "móvil enlazado a servidores externos. <b>El titular que ejecutó esta orden se encontraba fuera de la escena a esa hora exacta.</b>"
    )
    story.append(Paragraph(bank_audit_note, form_desc_typewriter))

    doc.build(story)
    print("Documento 2 generado:", output_filename)

# =============================================================================
# 3. GENERAR DOCUMENTO 3: PERFILES DE LOS 7 PERSONAJES (1 PÁGINA)
# =============================================================================
def generate_perfiles_pdf(output_filename="3_perfiles_personajes.pdf"):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=A4,
        leftMargin=30,
        rightMargin=30,
        topMargin=26,
        bottomMargin=26
    )

    story = []

    # Cabecera Estilo Character Profile (Captura 3)
    p_main_title = ParagraphStyle(
        'ProfMainTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=21,
        alignment=1,
        textColor=colors.HexColor('#0284C7'),
        spaceAfter=2
    )
    story.append(Paragraph("CHARACTER PROFILES — REGISTRO DE SOSPECHOSOS", p_main_title))
    story.append(Paragraph("<font size=8 color='#4B5563'>DESPACHO NOTARIAL Y DE ABOGACÍA — ANTECEDENTES Y RELACIÓN CON EL FINADO</font>", ParagraphStyle('SubSub', parent=styles['Normal'], alignment=1)))
    story.append(Spacer(1, 5))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0284C7'), spaceAfter=8))

    # EXACTAMENTE 7 CUADRÍCULAS (UNA POR PERSONAJE)
    # Estilo Banner azul claro en cada cabecera como en la captura 3
    # Letras ocultas en negrita: C - A - J - O - N - S - E - C - R - E - T - O
    suspects = [
        {
            "role": "1. PERFIL CINEGÉTICO (EL CAZADOR / LA CAZADORA)",
            "subtitle": "GUARDERÍA DE TERRENOS & FAUNA",
            "text": "<b>C</b>onservó labores técnicas en el Museo de Historia Natural de la capital hasta su repentino despido por irregularidades en el catálogo de especímenes protegidos.",
            "suspicion": "Vínculo con armas cinegéticas y piezas disecadas en el pabellón de caza."
        },
        {
            "role": "2. PERFIL MUSICAL (EL CANTANTE / LA CANTANTE)",
            "subtitle": "SOLISTA & FIGURA ESCÉNICA — GRUPO S.V.X.",
            "text": "Fundador y voz de referencia del afamado con<b>J</b>unto musical <b>S.V.X.</b> (Sinfonía Vocal X). Mantendría contactos reservados para silenciar exclusivas de prensa sobre incidentes privados.",
            "suspicion": "Reunión secreta con el anfitrión poco antes de apagarse las luces."
        },
        {
            "role": "3. PERFIL SANITARIO (EL MÉDICO / LA MÉDICA)",
            "subtitle": "FACULTATIVO PRIVADO DE CONFIANZA",
            "text": "F<b>A</b>cultativo con consulta privada de acreditada trayectoria. Asumía en exclusiva la custodia, administración y dispensación de la medicación diaria del finado.",
            "suspicion": "Acceso libre al botiquín personal y conocimiento de las dosis farmacológicas."
        },
        {
            "role": "4. PERFIL ESTRATÉGICO (EL GENERAL)",
            "subtitle": "MANDO MILITAR DEL ESTADO MAYOR",
            "text": "Mando de alta graduaci<b>Ó</b>n condecorado en servicios logísticos. Mantenía correspondencia confidencial e intercambios periódicos sobre expedientes reservados con la víctima.",
            "suspicion": "Presencia continuada en el despacho notarial y biblioteca revisando actas."
        },
        {
            "role": "5. PERFIL HEREDERO JOVEN (EL NIETO / LA NIETA)",
            "subtitle": "RAMA DESCENDIENTE DIRECTA",
            "text": "Aspirante a la fortu<b>N</b>a familiar vinculado a locales de ocio nocturno y plataformas virtuales de apuestas clandestinas. Frecuentes disputas familiares por adelantos patrimoniales.",
            "suspicion": "Presión apremiante de deudas telemáticas reclamadas por cobradores."
        },
        {
            "role": "6. PERFIL BOTÁNICO (EL JARDINERO / LA JARDINERA)",
            "subtitle": "CUSTODIA DE EXTERIORES Y CANCELAS",
            "text": "Re<b>S</b>ponsable del mantenimiento perimetral, arbolado y accesos secundarios. Incorporación reciente en nómina con documentación acreditativa procedente de otra comunidad.",
            "suspicion": "Disputa verbal directa con la víctima horas antes en los terrenos exteriores."
        },
        {
            "role": "7. PERFIL FRATERNO (EL HERMANO / LA HERMANA)",
            "subtitle": "GESTOR CORPORATIVO & SOCIEDADES",
            "text": "G<b>E</b>stor de entidades mercantiles familiares. Solicitó reuniones de urgencia con el anfitrión pidiendo avales millonarios inmediatos para evitar el colapso judicial y quiebra de sus empresas.",
            "suspicion": "Móvil económico de rescate patrimonial urgente ante la intervención bancaria."
        }
    ]

    card_header_style = ParagraphStyle(
        'CardHead',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=10.5,
        textColor=colors.HexColor('#0369A1')
    )
    
    card_sub_style = ParagraphStyle(
        'CardSub',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7,
        leading=8.5,
        alignment=2,
        textColor=colors.HexColor('#0C4A6E')
    )

    card_body_style = ParagraphStyle(
        'CardBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor('#1E293B')
    )

    # Construir las 7 cuadrículas (altura controlada para encajar en 1 página A4)
    for s in suspects:
        card_content = [
            [
                Paragraph(s["role"], card_header_style),
                Paragraph(s["subtitle"], card_sub_style)
            ],
            [
                Paragraph(f"<b>ANTECEDENTES:</b> {s['text']}<br/><b>INDICIOS:</b> {s['suspicion']}", card_body_style),
                ""
            ]
        ]
        t_card = Table(card_content, colWidths=[360, 175])
        t_card.setStyle(TableStyle([
            ('SPAN', (0,1), (1,1)),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E0F2FE')), # Fondo azul claro como captura 3
            ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#F8FAFC')),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#0284C7')),
            ('LINEBELOW', (0,0), (-1,0), 0.8, colors.HexColor('#38BDF8')),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(t_card)
        story.append(Spacer(1, 4))

    # Nota final al pie del albacea
    footer_text = (
        "<b>NOTA DE SEGURIDAD DEL ALBACEA:</b> Este legajo notarial recopila datos públicos y testimonios de la velada. "
        "Las anotaciones manuscritas del testador contienen caracteres singulares resaltados para el cotejo pericial."
    )
    story.append(Spacer(1, 2))
    story.append(Paragraph(f"<font size=7 color='#4B5563'>{footer_text}</font>", styles['Normal']))

    doc.build(story)
    print("Documento 3 generado:", output_filename)

# =============================================================================
# 4. GENERAR DOCUMENTO CONSOLIDADO (3 PÁGINAS)
# =============================================================================
def generate_consolidated_pdf(output_filename="documentos_investigacion.pdf"):
    import pypdf
    merger = pypdf.PdfWriter()
    for f in ["1_autopsia_forense.pdf", "2_periodico_warbes.pdf", "3_perfiles_personajes.pdf"]:
        reader = pypdf.PdfReader(f)
        for page in reader.pages:
            merger.add_page(page)
    with open(output_filename, "wb") as out:
        merger.write(out)
    print("PDF consolidado generado con éxito:", output_filename)

if __name__ == '__main__':
    generate_autopsia_pdf()
    generate_warbes_pdf()
    generate_perfiles_pdf()
    generate_consolidated_pdf()

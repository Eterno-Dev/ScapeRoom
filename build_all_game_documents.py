import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from PIL import Image as PILImage, ImageDraw

# =============================================================================
# 0. PREPARAR ASSETS: SILUETA ANOTADA Y FIRMA FORENSE
# =============================================================================
def prepare_assets():
    # 1. Silueta con brecha occipital
    bg_path = "src/assets/images/bg_men.png"
    out_annotated = "src/assets/images/bg_men_annotated.png"
    if os.path.exists(bg_path):
        im = PILImage.open(bg_path).convert("RGBA")
        draw = ImageDraw.Draw(im)
        cx, cy = 1310, 180 # Espalda - Cabeza
        draw.ellipse((cx-45, cy-45, cx+45, cy+45), outline="#dc2626", width=12)
        draw.ellipse((cx-16, cy-16, cx+16, cy+16), fill="#dc2626")
        draw.line((cx+45, cy, cx+220, cy-60), fill="#dc2626", width=8)
        draw.rectangle((cx+220, cy-130, cx+580, cy+30), fill=(255, 255, 255, 250), outline="#dc2626", width=6)
        draw.text((cx+235, cy-115), "BRECHA OCCIPITAL (18:30 H)", fill="#991b1b")
        draw.text((cx+235, cy-80), "Traumatismo contuso severo", fill="#1f2937")
        draw.text((cx+235, cy-50), "Impacto seco por caida libre", fill="#1f2937")
        draw.text((cx+235, cy-20), "Fractura deprimida en base", fill="#1f2937")
        draw.text((380, 1880), "VISTA ANTERIOR (FRENTE)", fill="#4b5563")
        draw.text((1180, 1880), "VISTA POSTERIOR (ESPALDA)", fill="#4b5563")
        im.save(out_annotated)

    # 2. Firma realista de médico forense independiente
    sig_path = "src/assets/images/signature_forense.png"
    w, h = 600, 160
    im_sig = PILImage.new('RGBA', (w, h), (255, 255, 255, 0))
    d_sig = ImageDraw.Draw(im_sig)
    ink = (15, 43, 92, 240)
    coords = [
        (30, 100), (45, 40), (60, 110), (75, 45), (90, 95), (105, 100),
        (130, 90), (145, 30), (160, 110), (175, 35), (195, 100),
        (215, 80), (225, 95), (235, 75), (245, 95),
        (265, 35), (275, 100), (285, 85),
        (315, 70), (330, 40), (345, 105), (360, 45), (375, 95),
        (390, 80), (405, 95), (420, 75), (435, 95), (455, 40), (470, 100)
    ]
    for i in range(len(coords)-1):
        d_sig.line([coords[i], coords[i+1]], fill=ink, width=4)
    flourish = [(50, 120), (120, 145), (250, 150), (400, 135), (520, 110), (550, 90), (520, 95), (460, 115), (550, 105)]
    for i in range(len(flourish)-1):
        d_sig.line([flourish[i], flourish[i+1]], fill=ink, width=4)
    im_sig_smooth = im_sig.resize((300, 80), PILImage.Resampling.LANCZOS)
    im_sig_smooth.save(sig_path)

prepare_assets()

styles = getSampleStyleSheet()

form_label = ParagraphStyle(
    'FormLabel', parent=styles['Normal'],
    fontName='Helvetica-Bold', fontSize=7.5, leading=9.5, textColor=colors.HexColor('#1F2937')
)

form_desc_typewriter = ParagraphStyle(
    'FormDescTypewriter', parent=styles['Normal'],
    fontName='Courier', fontSize=7.5, leading=10, textColor=colors.HexColor('#1E293B')
)

# =============================================================================
# 1. GENERAR DOCUMENTO 1: AUTOPSIA FORENSE (MÉDICO INDEPENDIENTE + FIRMA REAL)
# =============================================================================
def generate_autopsia_pdf(output_filename="1_autopsia_forense.pdf"):
    doc = SimpleDocTemplate(
        output_filename, pagesize=A4,
        leftMargin=30, rightMargin=30, topMargin=24, bottomMargin=24
    )

    story = []

    # Cabecera Medical Examiner
    story.append(Paragraph("INSTITUTO DE MEDICINA LEGAL Y CIENCIAS FORENSES", ParagraphStyle('H1', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9.5, leading=12, alignment=1, textColor=colors.HexColor('#111827'))))
    story.append(Paragraph("INFORME DE INVESTIGACIÓN MÉDICO FORENSE PRELIMINAR", ParagraphStyle('H2', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=13, leading=15, alignment=1, textColor=colors.HexColor('#000000'))))
    story.append(Paragraph("JUZGADO DE GUARDIA DE PRIMERA INSTANCIA — REF. EXPEDIENTE: 2026-F892", ParagraphStyle('H3', parent=styles['Normal'], fontName='Helvetica', fontSize=7.5, leading=9.5, alignment=1, textColor=colors.HexColor('#4B5563'))))
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

    # Formulario Fila 3: Tipo de Muerte
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
            Paragraph("<b>ACCESORIOS:</b> <font name='Courier-Bold'>Sin reloj de bolsillo ni cartera</font>", form_label),
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

    # CUERPO PRINCIPAL: HERIDAS + SILUETA REAL
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
        Paragraph("• <font name='Courier-Bold'>IDENTIFICACIÓN QUÍMICA:</font> No catalogada en cribado preliminar. El laboratorio no ha emitido informe definitivo sobre el principio activo.", form_desc_typewriter),
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

    # CONCLUSIONES INFERIORES: CAUSA PROBABLE Y ACCIONES
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
    story.append(Spacer(1, 4))

    # Declaración jurada y firma realista (Médico independiente: Dr. Mateo Valbuena)
    sig_img_path = "src/assets/images/signature_forense.png"
    sig_content = [
        [
            Paragraph("<b>FECHA:</b> <font name='Courier-Bold'>30/10/2026</font><br/><b>JUZGADO:</b> <font name='Courier-Bold'>Instrucción Nº 4</font>", form_label),
            Paragraph("<b>MÉDICO FORENSE OFICIAL ADSCRITO:</b><br/><font name='Courier-Bold'>Dr. Mateo Valbuena (Col. 28/44102)</font>", form_label),
            Image(sig_img_path, width=130, height=35)
        ]
    ]
    t_sig = Table(sig_content, colWidths=[140, 245, 150])
    t_sig.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,-1), 0.8, colors.HexColor('#000000')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
    ]))
    story.append(t_sig)

    doc.build(story)
    print("Documento 1 generado:", output_filename)

# =============================================================================
# 2. GENERAR DOCUMENTO 2: PERIÓDICO "WARBES" + SLIP RECORTABLE BANCARIO
# =============================================================================
def generate_warbes_pdf(output_filename="2_periodico_warbes.pdf"):
    doc = SimpleDocTemplate(
        output_filename, pagesize=A4,
        leftMargin=30, rightMargin=30, topMargin=22, bottomMargin=22
    )

    story = []

    # 1. BANNER METADATOS DE PRENSA
    meta_top = [
        [
            Paragraph("<b>VIERNES 30 DE OCTUBRE DE 2026 • EDICIÓN VESPERTINA ESPECIAL</b>", ParagraphStyle('WTopL', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor('#1F2937'))),
            Paragraph("<b>NÚMERO 14.892 • PRECIO: 2,80 €</b>", ParagraphStyle('WTopR', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8, alignment=2, textColor=colors.HexColor('#1F2937')))
        ]
    ]
    t_meta = Table(meta_top, colWidths=[365, 170])
    t_meta.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 1.2, colors.HexColor('#000000')),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_meta)

    # 2. MASTHEAD ENORME "WARBES" (Estilo Forbes / El País)
    story.append(Paragraph("WARBES", ParagraphStyle(
        'WarbesMasthead', parent=styles['Normal'],
        fontName='Times-Bold', fontSize=42, leading=44, alignment=1, textColor=colors.HexColor('#000000'), spaceBefore=2, spaceAfter=1
    )))
    story.append(Paragraph("EL DIARIO GLOBAL DE FINANZAS, MERCADOS Y GRANDES FORTUNAS", ParagraphStyle(
        'WarbesSub', parent=styles['Normal'],
        fontName='Times-Italic', fontSize=8.5, leading=10.5, alignment=1, textColor=colors.HexColor('#4B5563'), spaceAfter=4
    )))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#000000'), spaceAfter=6))

    # 3. TITULAR PRINCIPAL ENORME (EMPRESA NEUTRA: GRUPO KRONOS & LOGÍSTICA)
    story.append(Paragraph(
        "<b>¡BANCARROTA HISTÓRICA! EL GIGANTE EMPRESARIAL KRONOS SE DESPLOMA UN 82% EN BOLSA Y ENTRA EN PRECONCURSO DE ACREEDORES</b>",
        ParagraphStyle('MainHead', parent=styles['Heading1'], fontName='Times-Bold', fontSize=14.5, leading=17, textColor=colors.HexColor('#991B1B'), spaceAfter=5)
    ))

    # 4. CUERPO DEL PERIÓDICO DIVIDIDO EN SECCIONES BIEN DEFINIDAS (ESTILO EL PAÍS)
    grafica_path = "src/assets/images/grafica.png"

    # Columna 1: Crónica de la quiebra
    col1_text = (
        "<b>REDACCIÓN / MADRID.</b> El conglomerado multisectorial <b>Grupo Kronos & Logística S.A.</b>, "
        "uno de los mayores imperios mercantiles de la región, ha vivido hoy una jornada fatídica en el parquet bursátil "
        "con una caída en picado del <b>82% en sus títulos</b> tras vencer el plazo límite para atender sus deudas bancarias.<br/><br/>"
        "Fuentes judiciales han confirmado que el Juzgado de lo Mercantil procederá al <b>embargo preventivo de todas las cuentas "
        "patrimoniales</b> salvo que la dirección presente antes de 48 horas una inyección irrevocable de al menos dos millones de euros de liquidez inmediata."
    )
    col1 = [
        Paragraph(col1_text, ParagraphStyle('Col1P', parent=styles['Normal'], fontName='Times-Roman', fontSize=8.5, leading=11.5, textColor=colors.HexColor('#1F2937')))
    ]

    # Columna 2: Gráfica con margen y respiro (sin texto pegado)
    col2 = [
        Image(grafica_path, width=200, height=95),
        Spacer(1, 3),
        Paragraph("<font size=7 color='#4B5563'><b>Figura 1:</b> Desplome vertical de la cotización bursátil de Kronos S.A. en las últimas 72 h.</font>", styles['Normal'])
    ]

    # Columna 3: Noticia secundaria bien diferenciada
    col3_text = (
        "<b>INVESTIGACIÓN JUDICIAL</b><br/>"
        "<b>CRECEN LAS SANCIONES POR REDES ILEGALES DE APUESTAS Y COBROS VIOLENTOS</b><br/><br/>"
        "Operativos policiales alertan de transferencias y retiradas en metálico forzadas para saldar deudas de plataformas no reguladas (Apex Bets)."
    )
    col3 = [
        Paragraph(col3_text, ParagraphStyle('Col3P', parent=styles['Normal'], fontName='Times-Roman', fontSize=8, leading=10.5, textColor=colors.HexColor('#1F2937')))
    ]

    news_grid = Table([[col1, col2, col3]], colWidths=[195, 210, 130])
    news_grid.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LINEBEFORE', (1,0), (1,0), 0.5, colors.HexColor('#D1D5DB')),
        ('LINEBEFORE', (2,0), (2,0), 0.5, colors.HexColor('#D1D5DB')),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(news_grid)
    story.append(Spacer(1, 6))

    # 5. RECUADRO INFERIOR RECORTABLE: EXTRACTO BANCARIO (TIJERA + BORDE DISCONTINUO)
    story.append(Paragraph(
        "<font size=7 color='#6B7280'>✂ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ✂</font>",
        ParagraphStyle('ScissorLine', parent=styles['Normal'], alignment=1, spaceAfter=4)
    ))

    # Título y datos del extracto bancario
    bank_title = ParagraphStyle('BTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor('#111827'))
    story.append(Paragraph("BANCO CENTRAL PRIVADO — EXTRACTO OFICIAL DE CUENTA CORRIENTE", bank_title))
    story.append(Paragraph("<b>TITULAR:</b> D. Ricardo Valparaíso | <b>IBAN MATRIZ:</b> ES33 0049 1800 5511 2233 4455 | <b>PERÍODO:</b> 28 a 30 de Octubre de 2026", styles['Normal']))
    story.append(Spacer(1, 4))

    # Movimientos bancarios:
    # 1) Dos días antes (28/10) a la corporación en quiebra (Grupo Kronos).
    # 2) El día de la muerte (30/10 a las 18:28:44 h): Extracción PRESENCIAL EN VENTANILLA DE EFECTIVO en Sucursal Centro.
    bank_rows = [
        [
            Paragraph("<b>FECHA / HORA</b>", form_label),
            Paragraph("<b>OPERACIÓN / CONCEPTO OFICIAL</b>", form_label),
            Paragraph("<b>CANAL / TERMINAL</b>", form_label),
            Paragraph("<b>IMPORTE</b>", form_label)
        ],
        [
            Paragraph("<font name='Courier-Bold'>28/10/2026<br/>11:20:14 h</font>", form_desc_typewriter),
            Paragraph("TRANSFERENCIA ORDINARIA URGENTE<br/><font size=7 color='#6B7280'>Ref: Inyección auxilio financiero / Grupo Kronos & Logística S.A.</font>", form_desc_typewriter),
            Paragraph("Cuenta Bancaria Destino:<br/>ES84 2100 0418 9012 3456 7890", form_desc_typewriter),
            Paragraph("<font name='Courier-Bold' color='#991B1B'><b>- 1.850.000,00 €</b></font>", form_desc_typewriter)
        ],
        [
            Paragraph("<font name='Courier-Bold' color='#991B1B'><b>30/10/2026<br/>18:28:44 h</b></font><br/><font size=6.5 color='#991B1B'><b>(Minutos antes)</b></font>", form_desc_typewriter),
            Paragraph("<b>EXTRACCIÓN PRESENCIAL EN EFECTIVO (VENTANILLA)</b><br/><font size=7 color='#6B7280'>Ref: Retirada de efectivo en metálico con DNI y firma manuscrita</font>", form_desc_typewriter),
            Paragraph("<b>Ventanilla 3 — Sucursal Central</b><br/><font size=7 color='#6B7280'>Calle Mayor, 12 (Sede Urbana)</font>", form_desc_typewriter),
            Paragraph("<font name='Courier-Bold' color='#991B1B'><b>- 15.000,00 €</b></font>", form_desc_typewriter)
        ]
    ]

    t_bank = Table(bank_rows, colWidths=[95, 205, 145, 90])
    t_bank.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E5E7EB')),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#FFFFFF')),
        ('BACKGROUND', (0,2), (-1,2), colors.HexColor('#FEF2F2')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#000000')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D1D5DB')),
        ('ALIGN', (3,0), (3,-1), 'RIGHT'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_bank)
    story.append(Spacer(1, 5))

    bank_audit_note = (
        "<b>CONSTANCIA NOTARIAL DE PRESENCIA FÍSICA:</b> La retirada de <b>-15.000,00 € en dinero en efectivo fue efectuada "
        "de manera estrictamente presencial en la ventanilla de la Sucursal Centro a las 18:28:44 horas</b>, "
        "mediante acreditación de DNI y firma en el mostrador. <b>Dicho registro certifica documentalmente que la persona que retiró "
        "el efectivo se encontraba físicamente en la sucursal bancaria en el instante del crimen (18:30 h).</b>"
    )
    story.append(Paragraph(bank_audit_note, form_desc_typewriter))

    doc.build(story)
    print("Documento 2 generado:", output_filename)

# =============================================================================
# 3. GENERAR DOCUMENTO 3: PERFILES DE LOS 7 PERSONAJES (OCUPA LA PÁGINA ENTERA)
# =============================================================================
def generate_perfiles_pdf(output_filename="3_perfiles_personajes.pdf"):
    doc = SimpleDocTemplate(
        output_filename, pagesize=A4,
        leftMargin=30, rightMargin=30, topMargin=22, bottomMargin=22
    )

    story = []

    # Cabecera Notarial
    p_main_title = ParagraphStyle(
        'ProfMainTitle', parent=styles['Heading1'],
        fontName='Helvetica-Bold', fontSize=16, leading=19, alignment=1, textColor=colors.HexColor('#0284C7'), spaceAfter=2
    )
    story.append(Paragraph("REGISTRO NOTARIAL DE ASISTENTES A LA VELADA", p_main_title))
    story.append(Paragraph("<font size=8 color='#4B5563'>DESPACHO JURÍDICO & ALBACEAZGO — DOSSIER CONFIDENCIAL DE LOS 7 SOSPECHOSOS</font>", ParagraphStyle('SubSub', parent=styles['Normal'], alignment=1)))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0284C7'), spaceAfter=6))

    # EXACTAMENTE 7 CUADRÍCULAS GRANDES (OCUPANDO TODA LA PÁGINA A4)
    # Altura de cada caja generosa (~90pt) con padding espacioso
    suspects = [
        {
            "role": "1. PERFIL CINEGÉTICO (EL CAZADOR / LA CAZADORA)",
            "subtitle": "GUARDERÍA CINEGÉTICA & FAUNA",
            "text": "<b>C</b>onservó labores técnicas en el Museo de Historia Natural de la capital hasta su repentino despido disciplinario tras descubrirse irregularidades graves en el catálogo de especímenes protegidos.",
            "suspicion": "Vínculo con armas de caza y piezas disecadas en el pabellón de la finca."
        },
        {
            "role": "2. PERFIL MUSICAL (EL CANTANTE / LA CANTANTE)",
            "subtitle": "VOCALISTA SOLISTA — GRUPO S.V.X.",
            "text": "Fundador y voz de referencia del afamado con<b>J</b>unto musical <b>S.V.X.</b> (Sinfonía Vocal X). Mantendría contactos reservados para silenciar exclusivas de prensa sobre incidentes privados.",
            "suspicion": "Reunión secreta con el anfitrión poco antes de apagarse las luces."
        },
        {
            "role": "3. PERFIL SANITARIO (EL MÉDICO / LA MÉDICA)",
            "subtitle": "FACULTATIVO PRIVADO DE CONFIANZA",
            "text": "F<b>A</b>cultativo con consulta médica privada de acreditada trayectoria. Asumía en exclusiva la custodia, administración y dispensación de la medicación diaria del finado.",
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
        'CardHead', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=9, leading=11, textColor=colors.HexColor('#0369A1')
    )
    
    card_sub_style = ParagraphStyle(
        'CardSub', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=7.5, leading=9.5, alignment=2, textColor=colors.HexColor('#0C4A6E')
    )

    card_body_style = ParagraphStyle(
        'CardBody', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.5, leading=11.5, textColor=colors.HexColor('#1E293B')
    )

    for s in suspects:
        card_content = [
            [
                Paragraph(s["role"], card_header_style),
                Paragraph(s["subtitle"], card_sub_style)
            ],
            [
                Paragraph(f"<b>ANTECEDENTES:</b> {s['text']}<br/><b>INDICIOS EN LA VELADA:</b> {s['suspicion']}", card_body_style),
                ""
            ]
        ]
        t_card = Table(card_content, colWidths=[365, 170])
        t_card.setStyle(TableStyle([
            ('SPAN', (0,1), (1,1)),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E0F2FE')),
            ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#F8FAFC')),
            ('BOX', (0,0), (-1,-1), 1.2, colors.HexColor('#0284C7')),
            ('LINEBELOW', (0,0), (-1,0), 0.8, colors.HexColor('#38BDF8')),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(t_card)
        story.append(Spacer(1, 5))

    footer_text = (
        "<b>NOTA DE SEGURIDAD DEL ALBACEA:</b> Este legajo notarial recopila datos públicos y testimonios de la velada. "
        "Las anotaciones manuscritas del testador contienen caracteres singulares resaltados para el cotejo pericial."
    )
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

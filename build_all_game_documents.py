import os
import pymupdf
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from PIL import Image as PILImage, ImageDraw

# =============================================================================
# 0. PREPARAR ASSETS IMÁGENES
# =============================================================================
def prepare_assets():
    # 1. Silueta: SOLO el punto circular / diana roja en la nuca (occipital)
    bg_path = "src/assets/images/bg_men.png"
    out_annotated = "src/assets/images/bg_men_annotated.png"
    if os.path.exists(bg_path):
        im = PILImage.open(bg_path).convert("RGBA")
        draw = ImageDraw.Draw(im)
        cx, cy = 1310, 180 # Espalda - Nuca / Occipital
        draw.ellipse((cx-42, cy-42, cx+42, cy+42), outline="#dc2626", width=14)
        draw.ellipse((cx-16, cy-16, cx+16, cy+16), fill="#dc2626")
        draw.text((380, 1880), "VISTA ANTERIOR (FRENTE)", fill="#4b5563")
        draw.text((1180, 1880), "VISTA POSTERIOR (ESPALDA)", fill="#4b5563")
        im.save(out_annotated)

    # 2. Firma oficial médico forense (Dr. Mateo Valbuena) desde firma.png
    sig_raw_path = "C:/Users/paucr/Downloads/firma.png"
    sig_dest_path = "src/assets/images/signature_forense.png"
    if os.path.exists(sig_raw_path):
        im_f = PILImage.open(sig_raw_path).convert("RGBA")
        datas = im_f.getdata()
        new_data = []
        for item in datas:
            if item[0] > 230 and item[1] > 230 and item[2] > 230:
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)
        im_f.putdata(new_data)
        im_f.save(sig_dest_path)

    # 3. Pasaporte falso con doble círculo rojo en Alaska (SIN cajas rojas ni rótulos feos)
    pass_path = "src/assets/images/fake_passport.jpg"
    out_pass = "src/assets/images/fake_passport_clean.png"
    if os.path.exists(pass_path):
        im_p = PILImage.open(pass_path).convert("RGBA")
        d_p = ImageDraw.Draw(im_p)
        # Posición exacta de Alaska en el mapa superior (x=555, y=115)
        cx_a, cy_a = 555, 115
        d_p.ellipse((cx_a-14, cy_a-14, cx_a+14, cy_a+14), outline="#dc2626", width=3)
        d_p.ellipse((cx_a-5, cy_a-5, cx_a+5, cy_a+5), fill="#dc2626")

        # Texto alineado con los campos
        tx = 690
        d_p.text((tx, 395), "HERRERA", fill="#0f172a")
        d_p.text((tx, 435), "LUCIA", fill="#0f172a")
        d_p.text((tx, 475), "UNITED STATES OF AMERICA", fill="#1e293b")
        d_p.text((tx, 515), "03 NOV 1991", fill="#991b1b") # FAKE DATE
        d_p.text((820, 515), "F", fill="#1e293b")
        d_p.text((tx, 550), "ANCHORAGE, ALASKA, U.S.A.", fill="#991b1b") # FAKE PLACE

        # MRZ inferior
        d_p.text((490, 592), "P<USAHERRERA<<LUCIA<<<<<<<<<<<<<<<<<<<<<<<<<<", fill="#1e293b")
        d_p.text((490, 608), "5492018428USA9111032F3111038<<<<<<<<<<<<<<<02", fill="#1e293b")
        im_p.save(out_pass)

prepare_assets()

# Registrar fuentes periodísticas auténticas de rotativa
try:
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
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

styles = getSampleStyleSheet()

# =============================================================================
# 1. DOCUMENTO 1: AUTOPSIA FORENSE (100% LLENO DE MARGEN A MARGEN)
# =============================================================================
def generate_autopsia_pdf(output_filename="1_autopsia_forense.pdf"):
    doc = SimpleDocTemplate(
        output_filename, pagesize=A4,
        leftMargin=25, rightMargin=25, topMargin=16, bottomMargin=16
    )

    story = []

    # Cabecera
    story.append(Paragraph("INSTITUTO DE MEDICINA LEGAL Y CIENCIAS FORENSES", ParagraphStyle('H1', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10.5, leading=13, alignment=1, textColor=colors.HexColor('#111827'))))
    story.append(Paragraph("INFORME DE INVESTIGACIÓN MÉDICO FORENSE PRELIMINAR", ParagraphStyle('H2', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=15, leading=18, alignment=1, textColor=colors.HexColor('#000000'))))
    story.append(Paragraph("JUZGADO DE GUARDIA DE PRIMERA INSTANCIA — EXPEDIENTE FORENSE: 2026-F892", ParagraphStyle('H3', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=11, alignment=1, textColor=colors.HexColor('#4B5563'))))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#000000'), spaceAfter=8))

    f_label = ParagraphStyle('FLab', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, leading=11.5, textColor=colors.HexColor('#1F2937'))
    f_tw = ParagraphStyle('FTw', parent=styles['Normal'], fontName='Courier', fontSize=9, leading=12.5, textColor=colors.HexColor('#1E293B'))

    # Fila 1: Datos Personales
    r1 = [
        [
            Paragraph("<b>FALLECIDO:</b> <font name='Courier-Bold'>Ricardo Valparaíso</font>", f_label),
            Paragraph("<b>RAZA:</b> <font name='Courier-Bold'>Caucásica</font>", f_label),
            Paragraph("<b>SEXO:</b> <font name='Courier-Bold'>M</font>", f_label),
            Paragraph("<b>EDAD:</b> <font name='Courier-Bold'>72</font>", f_label)
        ]
    ]
    t1 = Table(r1, colWidths=[245, 115, 85, 100])
    t1.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 0.8, colors.HexColor('#000000')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t1)

    # Fila 2: Hora y Lugar
    r2 = [
        [
            Paragraph("<b>HORA DE LA MUERTE:</b> <font name='Courier-Bold' color='#991B1B'><b>18:30 HORAS</b></font>", f_label),
            Paragraph("<b>LUGAR DEL HALLAZGO:</b> <font name='Courier-Bold'>Finca Señorial Valparaíso (EE.UU.)</font>", f_label)
        ]
    ]
    t2 = Table(r2, colWidths=[245, 300])
    t2.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 0.8, colors.HexColor('#000000')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t2)

    # Fila 3: Tipo de Muerte
    cb_text = (
        "<b>TIPO DE MUERTE:</b>&nbsp;&nbsp;&nbsp;&nbsp;"
        "TRAUMÁTICA [ ]&nbsp;&nbsp;&nbsp;&nbsp;"
        "SUICIDIO [ ]&nbsp;&nbsp;&nbsp;&nbsp;"
        "SÚBITA [ ]&nbsp;&nbsp;&nbsp;&nbsp;"
        "HALLAZGO [ ]&nbsp;&nbsp;&nbsp;&nbsp;"
        "<b>SOSPECHOSA [<font name='Courier-Bold' color='#991B1B'>X</font>]</b>&nbsp;&nbsp;&nbsp;&nbsp;"
        "<b>NO NATURAL [<font name='Courier-Bold' color='#991B1B'>X</font>]</b>"
    )
    t3 = Table([[Paragraph(cb_text, f_label)]], colWidths=[545])
    t3.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 1.2, colors.HexColor('#000000')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t3)

    # Fila 4: Descripción del Cuerpo
    r4 = [
        [
            Paragraph("<b>ALTURA:</b> <font name='Courier-Bold'>1.76 m</font>", f_label),
            Paragraph("<b>PESO:</b> <font name='Courier-Bold'>78 kg</font>", f_label),
            Paragraph("<b>PELO:</b> <font name='Courier-Bold'>Cano</font>", f_label),
            Paragraph("<b>OJOS:</b> <font name='Courier-Bold'>Marrones</font>", f_label)
        ],
        [
            Paragraph("<b>VESTIMENTA:</b> <font name='Courier-Bold'>Traje formal oscuro de etiqueta</font>", f_label),
            Paragraph("<b>ACCESORIOS:</b> <font name='Courier-Bold'>Sin reloj de bolsillo ni cartera personal</font>", f_label),
            Paragraph("", f_label),
            Paragraph("", f_label)
        ]
    ]
    t4 = Table(r4, colWidths=[140, 125, 140, 140])
    t4.setStyle(TableStyle([
        ('SPAN', (1,1), (3,1)),
        ('LINEBELOW', (0,1), (-1,1), 0.8, colors.HexColor('#000000')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t4)
    story.append(Spacer(1, 12))

    # CUERPO PRINCIPAL: HERIDAS + SILUETA AMPLIADA
    left_flowables = [
        Paragraph("<b>MARCAS Y HERIDAS TRAUMÁTICAS (MARKS AND WOUNDS):</b>", f_label),
        Spacer(1, 5),
        Paragraph("• <font name='Courier-Bold'>LESIÓN CRANEAL:</font> Brecha contusa profunda de 5.2 cm en región occipital izquierda. Fractura conminuta en base craneal con hemorragia subaracnoidea inmediata. Consistente con impacto violento contra plano rígido tras caída súbita de espaldas.", f_tw),
        Spacer(1, 8),
        Paragraph("• <font name='Courier-Bold'>DESCARTE BALÍSTICO:</font> CERO orificios de entrada o salida de proyectil en piel o vísceras. Ausencia total de metralla o pólvora incrustada.", f_tw),
        Spacer(1, 8),
        Paragraph("• <font name='Courier-Bold'>DESCARTE DE ARMA BLANCA:</font> No se aprecian incisiones punzantes, heridas por estilete, tijeras ni herramientas.", f_tw),
        Spacer(1, 14),
        HRFlowable(width="100%", thickness=0.8, color=colors.HexColor('#9CA3AF'), spaceAfter=8),
        Paragraph("<b>RESULTADOS TOXICOLÓGICOS (TOXICOLOGY RESULTS):</b>", f_label),
        Spacer(1, 5),
        Paragraph("• <font name='Courier-Bold'>SUSTANCIA DETECTADA:</font> Compuesto activo en torrente sanguíneo cuantificado en <font color='#991B1B'><b>42.5 mg/L</b></font>.", f_tw),
        Spacer(1, 8),
        Paragraph("• <font name='Courier-Bold'>IDENTIFICACIÓN QUÍMICA:</font> No catalogada en cribado preliminar. El laboratorio no ha emitido informe definitivo sobre el principio activo.", f_tw),
        Spacer(1, 8),
        Paragraph("• <font name='Courier-Bold'>NOTA FACULTATIVA:</font> Un profesional médico debe cotejar esta concentración (42.5 mg/L) con la farmacopea para dictaminar si la dosis administrada era letal o insuficiente.", f_tw),
    ]

    img_annotated_path = "src/assets/images/bg_men_annotated.png"
    right_flowables = [
        Paragraph("<b>MAPA CORPORAL DE LESIONES (ESQUEMA OFICIAL)</b>", ParagraphStyle('DiagH', parent=f_label, alignment=1)),
        Spacer(1, 8),
        Image(img_annotated_path, width=240, height=295) # Silueta ampliada
    ]

    split_table = Table([[left_flowables, right_flowables]], colWidths=[305, 240])
    split_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1.2, colors.HexColor('#000000')),
        ('INNERGRID', (0,0), (-1,-1), 0.8, colors.HexColor('#000000')),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(split_table)
    story.append(Spacer(1, 14))

    # CONCLUSIONES INFERIORES: CAUSA PROBABLE Y ACCIONES
    bottom_boxes = [
        [
            Paragraph("<b>CAUSA PROBABLE DE LA MUERTE (PROBABLE CAUSE OF DEATH):</b>", f_label),
            Paragraph("<b>ACCIONES COMPLEMENTARIAS (FURTHER ACTION):</b>", f_label)
        ],
        [
            Paragraph("<font name='Courier-Bold'>TRAUMATISMO CRANEOENCEFÁLICO SEVERO (18:30 H).<br/>Shock irreversible producido por fractura occipital consecutiva a colapso y caída violenta hacia atrás.<br/>Intoxicación por compuesto químico sin determinar.</font>", f_tw),
            Paragraph("<font name='Courier-Bold'>1. Peritaje toxicológico urgente por especialista.<br/>2. Cotejo de la medicación incautada en la vivienda.<br/>3. Custodia de casquillos y evidencias perimetrales.</font>", f_tw)
        ]
    ]
    t_bottom = Table(bottom_boxes, colWidths=[315, 230])
    t_bottom.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1.2, colors.HexColor('#000000')),
        ('INNERGRID', (0,0), (-1,-1), 0.8, colors.HexColor('#000000')),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F3F4F6')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_bottom)
    story.append(Spacer(1, 14))

    # Declaración jurada y firma
    sig_img_path = "src/assets/images/signature_forense.png"
    sig_content = [
        [
            Paragraph("<b>FECHA:</b> <font name='Courier-Bold'>30/10/2026</font><br/><b>JUZGADO:</b> <font name='Courier-Bold'>Instrucción Nº 4</font>", f_label),
            Paragraph("<b>MÉDICO FORENSE OFICIAL ADSCRITO:</b><br/><font name='Courier-Bold'>Dr. Mateo Valbuena (Col. 28/44102)</font>", f_label),
            Image(sig_img_path, width=125, height=64)
        ]
    ]
    t_sig = Table(sig_content, colWidths=[145, 250, 150])
    t_sig.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,-1), 1, colors.HexColor('#000000')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_sig)

    doc.build(story)
    print("Documento 1 generado:", output_filename)

# =============================================================================
# 2. DOCUMENTO 2: PERIÓDICO "WARBES" (60%) + EXTRACTO BANCARIO (40%) DE MARGEN A MARGEN
# =============================================================================
def generate_warbes_pdf(output_filename="2_periodico_warbes.pdf"):
    doc = SimpleDocTemplate(
        output_filename, pagesize=A4,
        leftMargin=25, rightMargin=25, topMargin=15, bottomMargin=15
    )

    story = []

    # BANNER METADATOS
    meta_top = [
        [
            Paragraph("<b>VIERNES 30 DE OCTUBRE DE 2026 • EDICIÓN VESPERTINA ESPECIAL</b>", ParagraphStyle('WTopL', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor('#1F2937'))),
            Paragraph("<b>NÚMERO 14.892 • PRECIO: 2,80 $</b>", ParagraphStyle('WTopR', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, alignment=2, textColor=colors.HexColor('#1F2937')))
        ]
    ]
    t_meta = Table(meta_top, colWidths=[375, 170])
    t_meta.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 1.2, colors.HexColor('#000000')),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_meta)

    # MASTHEAD "WARBES" ENORME
    story.append(Paragraph("WARBES", ParagraphStyle(
        'WarbesMasthead', parent=styles['Normal'],
        fontName=FONT_HEADLINE, fontSize=52, leading=54, alignment=1, textColor=colors.HexColor('#000000'), spaceBefore=2, spaceAfter=2
    )))
    story.append(Paragraph("EL DIARIO GLOBAL DE FINANZAS, MERCADOS Y GRANDES FORTUNAS", ParagraphStyle(
        'WarbesSub', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=8, leading=10, alignment=1, textColor=colors.HexColor('#4B5563'), spaceAfter=5
    )))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#000000'), spaceAfter=7))

    # TITULAR PRINCIPAL: PUNCHY, IMPACTANTE Y PERIODÍSTICO
    story.append(Paragraph(
        "Kronos se desploma un 82% en Bolsa",
        ParagraphStyle('MainHead', parent=styles['Heading1'], fontName=FONT_HEADLINE, fontSize=24, leading=27, textColor=colors.HexColor('#991B1B'), spaceAfter=3)
    ))
    story.append(Paragraph(
        "La corporación entra en preconcurso de acreedores tras vencer sus pagarés corporativos. El juzgado amenaza con el embargo total si no aporta dos millones de dólares de urgencia.",
        ParagraphStyle('MainSub', parent=styles['Normal'], fontName=FONT_ITALIC, fontSize=10, leading=13.5, textColor=colors.HexColor('#374151'), spaceAfter=8)
    ))

    # CUERPO DEL PERIÓDICO (SECCIONES ESTILO EL PAÍS CON TEXTO JUSTIFICADO)
    grafica_path = "src/assets/images/grafica.png"

    col1_text = (
        "<b>NUEVA YORK. —</b> El conglomerado multisectorial <b>Grupo Kronos & Logística S.A.</b> "
        "vivió hoy una jornada de pánico bursátil con una caída vertical del <b>82% en sus títulos</b> "
        "tras vencer el plazo límite para atender pagarés financieros corporativos.<br/><br/>"
        "Fuentes judiciales han confirmado que el Juzgado de lo Mercantil procederá al <b>embargo preventivo de todas las cuentas "
        "patrimoniales</b> salvo que la dirección presente antes de 48 horas una inyección irrevocable de al menos dos millones de dólares de liquidez inmediata.<br/><br/>"
        "La quiebra arrastra a proveedores estratégicos y sitúa a los accionistas al borde de la insolvencia penal definitiva."
    )
    col1 = [
        Paragraph(col1_text, ParagraphStyle('Col1P', parent=styles['Normal'], fontName=FONT_BODY, fontSize=9.5, leading=13.5, alignment=4, textColor=colors.HexColor('#1F2937')))
    ]

    col2 = [
        Image(grafica_path, width=220, height=105),
        Spacer(1, 3),
        Paragraph("Desplome vertical de la cotización bursátil de Kronos S.A. en las últimas 72 h. / BLOOMBERG", ParagraphStyle('FNote', parent=styles['Normal'], fontName='Helvetica', fontSize=7, leading=9, textColor=colors.HexColor('#4B5563'))),
        Spacer(1, 6),
        Paragraph("<b>CRISIS DE LIQUIDEZ:</b> La caída de Kronos deja sin cobertura avales bancarios cruzados entre sociedades familiares.", ParagraphStyle('FigNote', parent=styles['Normal'], fontName=FONT_ITALIC, fontSize=8.5, leading=11.5, textColor=colors.HexColor('#4B5563')))
    ]

    col3_text = (
        "<b>INVESTIGACIÓN</b><br/>"
        "<font size=10 color='#111827'><b>Alerta por redes de apuestas ilegales</b></font><br/>"
        "<i>Operativos policiales investigan retiradas forzosas de efectivo vinculadas a la plataforma 'Apex Bets'.</i><br/><br/>"
        "Las autoridades alertan de movimientos bancarios telemáticos e intimidación física para saldar deudas clandestinas en grandes urbes."
    )
    col3 = [
        Paragraph(col3_text, ParagraphStyle('Col3P', parent=styles['Normal'], fontName=FONT_BODY, fontSize=8.5, leading=11.5, textColor=colors.HexColor('#1F2937')))
    ]

    news_grid = Table([[col1, col2, col3]], colWidths=[205, 225, 115])
    news_grid.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LINEBEFORE', (1,0), (1,0), 0.5, colors.HexColor('#D1D5DB')),
        ('LINEBEFORE', (2,0), (2,0), 0.5, colors.HexColor('#D1D5DB')),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(news_grid)
    story.append(Spacer(1, 14))

    # SLIP INFERIOR RECORTABLE DEL BANCO CENTRAL (40% RESTANTE, HASTA EL BORDE INFERIOR)
    story.append(Paragraph(
        "<font size=7 color='#6B7280'>✂ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ✂</font>",
        ParagraphStyle('ScissorLine', parent=styles['Normal'], alignment=1, spaceAfter=6)
    ))

    bank_title = ParagraphStyle('BTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=11.5, leading=14, textColor=colors.HexColor('#111827'))
    story.append(Paragraph("BANCO CENTRAL PRIVADO — EXTRACTO OFICIAL DE CUENTA CORRIENTE", bank_title))
    story.append(Paragraph("<b>TITULAR:</b> D. Ricardo Valparaíso | <b>IBAN MATRIZ:</b> US44 0049 1800 5511 2233 4455 | <b>PERÍODO:</b> 28 a 30 de Octubre de 2026", styles['Normal']))
    story.append(Spacer(1, 8))

    f_lab_b = ParagraphStyle('FLabB', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, leading=11, textColor=colors.HexColor('#1F2937'))
    f_tw_b = ParagraphStyle('FTwB', parent=styles['Normal'], fontName='Courier', fontSize=9, leading=12, textColor=colors.HexColor('#1E293B'))

    bank_rows = [
        [
            Paragraph("<b>FECHA / HORA</b>", f_lab_b),
            Paragraph("<b>OPERACIÓN / CONCEPTO OFICIAL</b>", f_lab_b),
            Paragraph("<b>CANAL / TERMINAL</b>", f_lab_b),
            Paragraph("<b>IMPORTE</b>", f_lab_b)
        ],
        [
            Paragraph("<font name='Courier-Bold'>28/10/2026<br/>11:20:14 h</font>", f_tw_b),
            Paragraph("TRANSFERENCIA ORDINARIA URGENTE<br/><font size=8 color='#6B7280'>Ref: Inyección auxilio financiero / Grupo Kronos & Logística S.A.</font>", f_tw_b),
            Paragraph("Cuenta Bancaria Destino:<br/>US84 2100 0418 9012 3456 7890", f_tw_b),
            Paragraph("<font name='Courier-Bold' color='#991B1B'><b>- 1.850.000,00 $</b></font>", f_tw_b)
        ],
        [
            Paragraph("<font name='Courier-Bold' color='#991B1B'><b>30/10/2026<br/>18:28:44 h</b></font><br/><font size=7.5 color='#991B1B'><b>(Minutos antes)</b></font>", f_tw_b),
            Paragraph("<b>EXTRACCIÓN PRESENCIAL EN EFECTIVO (VENTANILLA)</b><br/><font size=8 color='#6B7280'>Ref: Retirada de efectivo en metálico con DNI/ID y firma manuscrita</font>", f_tw_b),
            Paragraph("<b>Ventanilla 3 — Sucursal Central</b><br/><font size=8 color='#6B7280'>Main Street, 120 (Sede Urbana)</font>", f_tw_b),
            Paragraph("<font name='Courier-Bold' color='#991B1B'><b>- 15.000,00 $</b></font>", f_tw_b)
        ]
    ]

    t_bank = Table(bank_rows, colWidths=[100, 215, 140, 90])
    t_bank.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E5E7EB')),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#FFFFFF')),
        ('BACKGROUND', (0,2), (-1,2), colors.HexColor('#FEF2F2')),
        ('BOX', (0,0), (-1,-1), 1.2, colors.HexColor('#000000')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D1D5DB')),
        ('ALIGN', (3,0), (3,-1), 'RIGHT'),
        ('TOPPADDING', (0,0), (-1,-1), 9),
        ('BOTTOMPADDING', (0,0), (-1,-1), 9),
    ]))
    story.append(t_bank)
    story.append(Spacer(1, 10))

    bank_audit_note = (
        "<b>CONSTANCIA NOTARIAL DE PRESENCIA FÍSICA:</b> La retirada de <b>-15.000,00 $ en dinero en efectivo fue efectuada "
        "de manera estrictamente presencial en la ventanilla de la Sucursal Centro a las 18:28:44 horas</b>, "
        "mediante acreditación de documento de identidad y firma manuscrita in situ. <b>Dicho registro certifica documentalmente "
        "que la persona que retiró el efectivo se encontraba físicamente en la sucursal bancaria urbana en el instante del crimen (18:30 h).</b>"
    )
    story.append(Paragraph(bank_audit_note, f_tw_b))

    doc.build(story)
    print("Documento 2 generado:", output_filename)

# =============================================================================
# 3. DOCUMENTO 3: REGISTRO DE PERSONAS CERCANAS AL FALLECIDO (100% LLENO)
# =============================================================================
def generate_perfiles_pdf(output_filename="3_perfiles_personajes.pdf"):
    doc = SimpleDocTemplate(
        output_filename, pagesize=A4,
        leftMargin=25, rightMargin=25, topMargin=16, bottomMargin=16
    )

    story = []

    # Cabecera Oficial
    p_main_title = ParagraphStyle(
        'ProfMainTitle', parent=styles['Heading1'],
        fontName='Helvetica-Bold', fontSize=15.5, leading=18.5, alignment=1, textColor=colors.HexColor('#0284C7'), spaceAfter=2
    )
    story.append(Paragraph("REGISTRO DE PERSONAS CERCANAS AL FALLECIDO", p_main_title))
    story.append(Paragraph("<font size=8.5 color='#4B5563'>EXPEDIENTE DE IDENTIFICACIÓN — CÍRCULO SOCIAL Y FAMILIAR CONVOCADO A LA VELADA</font>", ParagraphStyle('SubSub', parent=styles['Normal'], alignment=1)))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0284C7'), spaceAfter=8))

    # EXACTAMENTE 7 CUADRÍCULAS DE MEDIDAS IDÉNTICAS Y NOMBRES DE ROL AJUSTADOS AL USUARIO
    # Lugares de nacimiento TODOS ESTADOUNIDENSES (Hermano y Nieto del mismo lugar: Boston, Massachusetts)
    # Jardinero/a: Queens, Nueva York (EE.UU.) — 14 de mayo de 1994
    suspects = [
        {
            "role": "1. CAZADOR DE LA FINCA",
            "subtitle": "GUARDERÍA CINEGÉTICA & MEDIO RURAL",
            "bio": "Guarda forestal y especialista cinegético. Administraba los cotos y senderos naturales de la finca desde hacía ocho años por encargo directo del anfitrión.",
            "birthplace": "Helena, Montana (EE.UU.)",
            "birthdate": "22 de marzo de 1982"
        },
        {
            "role": "2. MÚSICO",
            "subtitle": "VOCALISTA PROFESIONAL — GRUPO S.V.X.",
            "bio": "Vocalista y director artístico del afamado conjunto musical S.V.X. (Sinfonía Vocal X). Amenizaba las recepciones exclusivas y veladas de gala en el salón principal.",
            "birthplace": "Nueva Orleans, Luisiana (EE.UU.)",
            "birthdate": "17 de agosto de 1989"
        },
        {
            "role": "3. RESPONSABLE SANITARIO",
            "subtitle": "MEDICINA INTERNA & CONSULTA PRIVADA",
            "bio": "Facultativo de cabecera privado con amplia reputación. Responsable del seguimiento médico diario, revisión de analíticas y custodia de la medicación del difunto.",
            "birthplace": "Filadelfia, Pensilvania (EE.UU.)",
            "birthdate": "05 de noviembre de 1976"
        },
        {
            "role": "4. GENERAL MILITAR",
            "subtitle": "OFICIAL SUPERIOR (EN RESERVA)",
            "bio": "Oficial de alta graduación en la reserva del Ejército. Amigo de juventud del anfitrión y consultor histórico en asuntos de patrimonio y archivo militar.",
            "birthplace": "San Antonio, Texas (EE.UU.)",
            "birthdate": "11 de enero de 1965"
        },
        {
            "role": "5. DESCENDIENTE LEJANO",
            "subtitle": "RAMA DESCENDIENTE DIRECTA (NIETO/A)",
            "bio": "Graduado en comercio exterior y gestor de actividades de ocio. Nieto del finado y aspirante natural en la línea de sucesión de los bienes familiares.",
            "birthplace": "Boston, Massachusetts (EE.UU.)", # MISMO LUGAR QUE EL HERMANO
            "birthdate": "29 de septiembre de 2001"
        },
        {
            "role": "6. JARDINERO DE LA FINCA",
            "subtitle": "BOTÁNICA ORNAMENTAL & EXTERIORES",
            "bio": "Especialista en botánica ornamental y cancelas exteriores. Incorporación reciente en la finca para la conservación del mirador vegetal y accesos perimetrales.",
            "birthplace": "Queens, Nueva York (EE.UU.)", # <--- DISCREPANCIA CLAVE CON PASAPORTE FALSO
            "birthdate": "14 de mayo de 1994"           # <--- DISCREPANCIA CLAVE (1994 vs 1991)
        },
        {
            "role": "7. HERMANO DE LA VÍCTIMA",
            "subtitle": "ADMINISTRACIÓN MERCANTIL",
            "bio": "Director mercantil y gestor de sociedades de inversión familiar. Hermano menor del fallecido y copropietario de activos patrimoniales comunes.",
            "birthplace": "Boston, Massachusetts (EE.UU.)", # MISMO LUGAR QUE EL NIETO
            "birthdate": "19 de julio de 1960"
        }
    ]

    card_header_style = ParagraphStyle(
        'CardHead', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=9.5, leading=12, textColor=colors.HexColor('#0369A1')
    )
    
    card_sub_style = ParagraphStyle(
        'CardSub', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=8, leading=10, alignment=2, textColor=colors.HexColor('#0C4A6E')
    )

    card_body_style = ParagraphStyle(
        'CardBody', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9, leading=12.5, textColor=colors.HexColor('#1E293B')
    )

    card_meta_style = ParagraphStyle(
        'CardMeta', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.5, leading=11, textColor=colors.HexColor('#0F172A')
    )

    # Cada tabla con relleno generoso y altura perfectamente repartida
    for s in suspects:
        card_content = [
            [
                Paragraph(s["role"], card_header_style),
                Paragraph(s["subtitle"], card_sub_style)
            ],
            [
                Paragraph(f"<b>OCUPACIÓN Y RELACIÓN:</b> {s['bio']}", card_body_style),
                ""
            ],
            [
                Paragraph(f"<b>LUGAR DE NACIMIENTO:</b> {s['birthplace']}", card_meta_style),
                Paragraph(f"<b>FECHA DE NACIMIENTO:</b> {s['birthdate']}", card_meta_style)
            ]
        ]
        t_card = Table(card_content, colWidths=[375, 170])
        t_card.setStyle(TableStyle([
            ('SPAN', (0,1), (1,1)),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E0F2FE')),
            ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#F8FAFC')),
            ('BACKGROUND', (0,2), (-1,2), colors.HexColor('#F1F5F9')),
            ('BOX', (0,0), (-1,-1), 1.2, colors.HexColor('#0284C7')),
            ('LINEBELOW', (0,0), (-1,0), 0.8, colors.HexColor('#38BDF8')),
            ('LINEBELOW', (0,1), (-1,1), 0.6, colors.HexColor('#CBD5E1')),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5.5),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(t_card)
        story.append(Spacer(1, 5))

    doc.build(story)
    print("Documento 3 generado:", output_filename)

# =============================================================================
# 4. DOCUMENTO 4: PASAPORTE FALSO RECORTABLE (AMBOS GÉNEROS EN 1 PÁGINA)
# =============================================================================
def generate_pasaporte_pdf(output_filename="4_pasaporte_falso.pdf"):
    doc = SimpleDocTemplate(
        output_filename, pagesize=A4,
        leftMargin=25, rightMargin=25, topMargin=12, bottomMargin=12
    )

    story = []

    pass_female = "src/assets/images/fake_passport_female.jpg"
    pass_male = "src/assets/images/fake_passport_male.jpg"
    pw = 510
    ph = 347 # Aspect ratio 932x634 -> 1.47

    story.append(Paragraph("<font size=7 color='#6B7280'><b>OPCIÓN A: EVIDENCIA PASAPORTE FEMENINO</b></font>", ParagraphStyle('HPassF', parent=styles['Normal'], alignment=1, spaceAfter=2)))
    story.append(Image(pass_female, width=pw, height=ph))
    story.append(Spacer(1, 4))

    # Línea de recorte exactamente a mitad de página
    story.append(Paragraph(
        "<font size=7 color='#6B7280'>✂ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ✂</font>",
        ParagraphStyle('ScissorLinePass', parent=styles['Normal'], alignment=1, spaceAfter=2)
    ))
    story.append(Paragraph("<font size=6.5 color='#9CA3AF'>RECORTAR EL PASAPORTE CORRESPONDIENTE SEGÚN EL GÉNERO ELEGIDO PARA LA INVESTIGACIÓN</font>", ParagraphStyle('CutLabel2', parent=styles['Normal'], alignment=1, spaceAfter=4)))

    story.append(Paragraph("<font size=7 color='#6B7280'><b>OPCIÓN B: EVIDENCIA PASAPORTE MASCULINO</b></font>", ParagraphStyle('HPassM', parent=styles['Normal'], alignment=1, spaceAfter=2)))
    story.append(Image(pass_male, width=pw, height=ph))

    doc.build(story)
    print("Documento 4 generado:", output_filename)

# =============================================================================
# 5. GENERAR DOCUMENTO CONSOLIDADO (5 PÁGINAS)
# =============================================================================
def generate_consolidated_pdf(output_filename="documentos_investigacion.pdf"):
    merger = pymupdf.open()
    for f in ["1_autopsia_forense.pdf", "2_periodico_warbes.pdf", "3_perfiles_personajes.pdf", "4_pasaporte_falso.pdf", "5_periodico_dia.pdf"]:
        if os.path.exists(f):
            doc = pymupdf.open(f)
            merger.insert_pdf(doc)
    merger.save(output_filename)
    print("PDF consolidado generado con éxito:", output_filename)

if __name__ == '__main__':
    generate_autopsia_pdf()
    generate_warbes_pdf()
    generate_perfiles_pdf()
    generate_pasaporte_pdf()
    from generate_periodico_dia import build_periodico_dia_pdf
    build_periodico_dia_pdf("5_periodico_dia.pdf")
    generate_consolidated_pdf()

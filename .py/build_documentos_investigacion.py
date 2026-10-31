import os
import sys
import pymupdf
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from PIL import Image as PILImage, ImageDraw

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(SCRIPT_DIR) in [".py", "py", "scripts"]:
    PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
else:
    PROJECT_ROOT = SCRIPT_DIR
os.chdir(PROJECT_ROOT)

def prepare_assets():
    # 1. Silueta con punto rojo en occipital
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

    # 2. Firma forense
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

    # 3. Pasaporte limpio con diana en Alaska
    pass_path = "src/assets/images/fake_passport.jpg"
    out_pass = "src/assets/images/fake_passport_clean.png"
    if os.path.exists(pass_path):
        im_p = PILImage.open(pass_path).convert("RGBA")
        d_p = ImageDraw.Draw(im_p)
        cx_a, cy_a = 555, 115
        d_p.ellipse((cx_a-14, cy_a-14, cx_a+14, cy_a+14), outline="#dc2626", width=3)
        d_p.ellipse((cx_a-5, cy_a-5, cx_a+5, cy_a+5), fill="#dc2626")

        tx = 690
        d_p.text((tx, 395), "HERRERA", fill="#0f172a")
        d_p.text((tx, 435), "LUCIA", fill="#0f172a")
        d_p.text((tx, 475), "UNITED STATES OF AMERICA", fill="#1e293b")
        d_p.text((tx, 515), "03 NOV 1991", fill="#991b1b")
        d_p.text((820, 515), "F", fill="#1e293b")
        d_p.text((tx, 550), "ANCHORAGE, ALASKA, U.S.A.", fill="#991b1b")

        d_p.text((490, 592), "P<USAHERRERA<<LUCIA<<<<<<<<<<<<<<<<<<<<<<<<<<", fill="#1e293b")
        d_p.text((490, 608), "5492018428USA9111032F3111038<<<<<<<<<<<<<<<02", fill="#1e293b")
        im_p.save(out_pass)

def build_autopsia_pdf(output_filename="temp_autopsia.pdf"):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(
        output_filename, pagesize=A4,
        leftMargin=25, rightMargin=25, topMargin=16, bottomMargin=16
    )

    story = []

    story.append(Paragraph("INSTITUTO DE MEDICINA LEGAL Y CIENCIAS FORENSES", ParagraphStyle('H1', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10.5, leading=13, alignment=1, textColor=colors.HexColor('#111827'))))
    story.append(Paragraph("INFORME DE INVESTIGACIÓN MÉDICO FORENSE PRELIMINAR", ParagraphStyle('H2', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=15, leading=18, alignment=1, textColor=colors.HexColor('#000000'))))
    story.append(Paragraph("JUZGADO DE GUARDIA DE PRIMERA INSTANCIA — EXPEDIENTE FORENSE: 2026-F892", ParagraphStyle('H3', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=11, alignment=1, textColor=colors.HexColor('#4B5563'))))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#000000'), spaceAfter=8))

    f_label = ParagraphStyle('FLab', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, leading=11.5, textColor=colors.HexColor('#1F2937'))
    f_tw = ParagraphStyle('FTw', parent=styles['Normal'], fontName='Courier', fontSize=9, leading=12.5, textColor=colors.HexColor('#1E293B'))

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
        Image(img_annotated_path, width=240, height=295)
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

    sig_img_path = "src/assets/images/signature_forense.png"
    sig_content = [
        [
            Paragraph("<b>FECHA:</b> <font name='Courier-Bold'>30/10/2026</font><br/><b>JUZGADO:</b> <font name='Courier-Bold'>Instrucción Nº 4</font>", f_label),
            Paragraph("<b>MÉDICO FORENSE OFICIAL ADSCRITO:</b><br/><font name='Courier-Bold'>Dr. Mateo Valbuena (Col. 28/44102)</font>", f_label),
            Image(sig_img_path, width=145, height=40)
        ]
    ]
    t_sig = Table(sig_content, colWidths=[145, 250, 150])
    t_sig.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,-1), 1, colors.HexColor('#000000')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_sig)

    doc.build(story)

def build_warbes_pdf(output_filename="temp_warbes.pdf"):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(
        output_filename, pagesize=A4,
        leftMargin=25, rightMargin=25, topMargin=15, bottomMargin=15
    )

    story = []

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

    story.append(Paragraph("WARBES", ParagraphStyle(
        'WarbesMasthead', parent=styles['Normal'],
        fontName='Times-Bold', fontSize=50, leading=52, alignment=1, textColor=colors.HexColor('#000000'), spaceBefore=2, spaceAfter=2
    )))
    story.append(Paragraph("EL DIARIO GLOBAL DE FINANZAS, MERCADOS Y GRANDES FORTUNAS", ParagraphStyle(
        'WarbesSub', parent=styles['Normal'],
        fontName='Times-Italic', fontSize=10, leading=12, alignment=1, textColor=colors.HexColor('#4B5563'), spaceAfter=6
    )))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#000000'), spaceAfter=8))

    story.append(Paragraph(
        "<b>¡BANCARROTA HISTÓRICA! EL GIGANTE EMPRESARIAL KRONOS SE DESPLOMA UN 82% EN BOLSA Y ENTRA EN PRECONCURSO DE ACREEDORES</b>",
        ParagraphStyle('MainHead', parent=styles['Heading1'], fontName='Times-Bold', fontSize=16, leading=19, textColor=colors.HexColor('#991B1B'), spaceAfter=10)
    ))

    grafica_path = "src/assets/images/grafica.png"

    col1_text = (
        "<b>NUEVA YORK / WALL STREET.</b> El conglomerado multisectorial <b>Grupo Kronos & Logística S.A.</b>, "
        "uno de los mayores imperios corporativos de la región, ha vivido hoy una jornada de pánico bursátil "
        "con una caída vertical del <b>82% en sus títulos</b> tras vencer el plazo límite para atender pagarés financieros.<br/><br/>"
        "Fuentes judiciales han confirmado que el Juzgado de lo Mercantil procederá al <b>embargo preventivo de todas las cuentas "
        "patrimoniales</b> salvo que la dirección presente antes de 48 horas una inyección irrevocable de al menos dos millones de dólares de liquidez inmediata.<br/><br/>"
        "La quiebra arrastra a proveedores estratégicos y sitúa a los principales accionistas al borde de la insolvencia penal definitiva."
    )
    col1 = [
        Paragraph(col1_text, ParagraphStyle('Col1P', parent=styles['Normal'], fontName='Times-Roman', fontSize=10, leading=14, textColor=colors.HexColor('#1F2937')))
    ]

    col2 = [
        Image(grafica_path, width=220, height=110),
        Spacer(1, 4),
        Paragraph("<font size=8 color='#4B5563'><b>Figura 1:</b> Desplome vertical de la cotización bursátil de Kronos S.A. en las últimas 72 h.</font>", styles['Normal']),
        Spacer(1, 8),
        Paragraph("<b>CRISIS DE LIQUIDEZ:</b> La caída de Kronos deja sin cobertura avales bancarios cruzados entre sociedades familiares.", ParagraphStyle('FigNote', parent=styles['Normal'], fontName='Times-Italic', fontSize=8.5, leading=12, textColor=colors.HexColor('#4B5563')))
    ]

    col3_text = (
        "<b>INVESTIGACIÓN JUDICIAL</b><br/>"
        "<b>CRECEN LAS SANCIONES POR REDES ILEGALES DE APUESTAS Y COBROS VIOLENTOS</b><br/><br/>"
        "Operativos policiales alertan de transferencias telemáticas y retiradas forzosas de efectivo para saldar deudas de juego bajo intimidación.<br/><br/>"
        "Plataformas offshore como <i>Apex Bets</i> están bajo el foco de la fiscalía por operaciones de blanqueo de capitales."
    )
    col3 = [
        Paragraph(col3_text, ParagraphStyle('Col3P', parent=styles['Normal'], fontName='Times-Roman', fontSize=9, leading=12.5, textColor=colors.HexColor('#1F2937')))
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

def build_perfiles_pdf(output_filename="temp_perfiles.pdf"):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(
        output_filename, pagesize=A4,
        leftMargin=25, rightMargin=25, topMargin=16, bottomMargin=16
    )

    story = []

    p_main_title = ParagraphStyle(
        'ProfMainTitle', parent=styles['Heading1'],
        fontName='Helvetica-Bold', fontSize=15.5, leading=18.5, alignment=1, textColor=colors.HexColor('#0284C7'), spaceAfter=2
    )
    story.append(Paragraph("REGISTRO DE PERSONAS CERCANAS AL FALLECIDO", p_main_title))
    story.append(Paragraph("<font size=8.5 color='#4B5563'>EXPEDIENTE DE IDENTIFICACIÓN — CÍRCULO SOCIAL Y FAMILIAR CONVOCADO A LA VELADA</font>", ParagraphStyle('SubSub', parent=styles['Normal'], alignment=1)))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0284C7'), spaceAfter=8))

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
            "birthplace": "Boston, Massachusetts (EE.UU.)",
            "birthdate": "29 de septiembre de 2001"
        },
        {
            "role": "6. JARDINERO DE LA FINCA",
            "subtitle": "BOTÁNICA ORNAMENTAL & EXTERIORES",
            "bio": "Especialista en botánica ornamental y cancelas exteriores. Incorporación reciente en la finca para la conservación del mirador vegetal y accesos perimetrales.",
            "birthplace": "Queens, Nueva York (EE.UU.)",
            "birthdate": "14 de mayo de 1994"
        },
        {
            "role": "7. HERMANO DE LA VÍCTIMA",
            "subtitle": "ADMINISTRACIÓN MERCANTIL",
            "bio": "Director mercantil y gestor de sociedades de inversión familiar. Hermano menor del fallecido y copropietario de activos patrimoniales comunes.",
            "birthplace": "Boston, Massachusetts (EE.UU.)",
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

def build_pasaporte_pdf(output_filename="temp_pasaporte.pdf"):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(
        output_filename, pagesize=A4,
        leftMargin=25, rightMargin=25, topMargin=15, bottomMargin=15
    )

    story = []
    pass_clean_path = "src/assets/images/fake_passport_clean.png"
    story.append(Image(pass_clean_path, width=545, height=370))
    story.append(Spacer(1, 14))

    story.append(Paragraph(
        "<font size=7 color='#6B7280'>✂ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ✂</font>",
        ParagraphStyle('ScissorLinePass', parent=styles['Normal'], alignment=1, spaceAfter=4)
    ))
    story.append(Paragraph("<font size=7 color='#9CA3AF'>LÍNEA DE RECORTE DE EVIDENCIA (OCUPA EXACTAMENTE EL 50% DE LA PÁGINA)</font>", ParagraphStyle('CutLabel2', parent=styles['Normal'], alignment=1)))

    doc.build(story)

def build_consolidated_investigacion(output_pdf="documentos_investigacion.pdf"):
    prepare_assets()
    
    # 1. Generar los 4 documentos oficiales
    temp_autopsia = "temp_autopsia.pdf"
    temp_warbes = "temp_warbes.pdf"
    temp_perfiles = "temp_perfiles.pdf"
    temp_pasaporte = "temp_pasaporte.pdf"
    
    build_autopsia_pdf(temp_autopsia)
    build_warbes_pdf(temp_warbes)
    build_perfiles_pdf(temp_perfiles)
    build_pasaporte_pdf(temp_pasaporte)
    
    # 2. Preparar el dossier fotográfico de diligencias (10 páginas)
    dossier_dir = os.path.join(PROJECT_ROOT, "src", "assets", "images", "dossier")
    desktop_dir = os.path.expanduser("~/Desktop")
    
    pages = [
        "page_cover.png",
        "page_1.png",
        "page_2.png",
        "page_3.png",
        "page_4.png",
        "page_5.png",
        "page_6.png",
        "page_7.png",
        "page_8.png",
        "page_back.png"
    ]
    
    A4_WIDTH = 595.27557
    A4_HEIGHT = 841.88977
    page_rect = pymupdf.Rect(0, 0, A4_WIDTH, A4_HEIGHT)
    
    doc_final = pymupdf.open()
    
    # A) Insertar las 10 páginas del Dossier de diligencias
    for filename in pages:
        local_path = os.path.join(dossier_dir, filename)
        desktop_path = os.path.join(desktop_dir, filename)
        img_path = local_path if os.path.exists(local_path) else desktop_path
        if not os.path.exists(img_path):
            raise FileNotFoundError(f"No se encontró la imagen: {filename}")
        page = doc_final.new_page(width=A4_WIDTH, height=A4_HEIGHT)
        page.insert_image(page_rect, filename=img_path)
        print(f"[OK] Insertada página dossier: {filename}")
        
    # B) Insertar los 4 documentos de evidencia pericial (Autopsia, Prensa Warbes, Registro DNI, Pasaporte)
    for temp_pdf in [temp_autopsia, temp_warbes, temp_perfiles, temp_pasaporte]:
        doc_part = pymupdf.open(temp_pdf)
        doc_final.insert_pdf(doc_part)
        doc_part.close()
        print(f"[OK] Insertado documento pericial: {temp_pdf}")
        
    out_path = os.path.join(PROJECT_ROOT, output_pdf)
    doc_final.save(out_path, deflate=True)
    doc_final.close()
    
    # Limpiar archivos temporales
    for temp_pdf in [temp_autopsia, temp_warbes, temp_perfiles, temp_pasaporte]:
        if os.path.exists(temp_pdf):
            os.remove(temp_pdf)
            
    print(f"\n=======================================================")
    print(f"DOCUMENTO TOTAL CONSOLIDADO GENERADO: {out_path}")
    print(f"Páginas totales: {len(pymupdf.open(out_path))} páginas")
    print(f"Tamaño: {os.path.getsize(out_path)} bytes")
    print(f"=======================================================")

if __name__ == "__main__":
    build_consolidated_investigacion("documentos_investigacion.pdf")

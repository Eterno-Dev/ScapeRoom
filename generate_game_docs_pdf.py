import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.graphics.shapes import Drawing, Rect, Circle, Line, String
import qrcode

OUTPUT_PDF = "documentos_investigacion.pdf"

def generate_qr(text, filename):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=1,
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
    return filename

def build_pdf():
    # A4: 595.27 x 841.89 pt. Con márgenes de 36pt a cada lado: ancho útil = 523pt, alto útil = 770pt
    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    qr_path = "temp_qr_autopsia.png"
    generate_qr("AUTOPSIA-1830-TOX-42MG", qr_path)

    styles = getSampleStyleSheet()

    # Tipografías y Jerarquías
    main_title = ParagraphStyle(
        'MainTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=colors.HexColor('#111827'),
        alignment=1, # Centrado
        spaceAfter=3
    )
    
    top_badge = ParagraphStyle(
        'TopBadge',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#4B5563'),
        alignment=1,
        spaceAfter=3
    )

    sub_header = ParagraphStyle(
        'SubHeader',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#6B7280'),
        alignment=1,
        spaceAfter=8
    )

    section_title = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#991B1B'),
        spaceBefore=8,
        spaceAfter=6
    )

    body_text = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#1F2937'),
        spaceAfter=4
    )

    body_bold = ParagraphStyle(
        'BodyBold',
        parent=body_text,
        fontName='Helvetica-Bold'
    )

    card_text = ParagraphStyle(
        'CardText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#1F2937')
    )

    story = []

    # =========================================================================
    # DOCUMENTO 1: INFORME MÉDICO-FORENSE Y PROTOCOLO DE AUTOPSIA (PÁGINA 1)
    # =========================================================================
    story.append(Paragraph("INSTITUTO DE MEDICINA LEGAL Y CIENCIAS FORENSES", top_badge))
    story.append(Paragraph("EXPEDIENTE FORENSE PRELIMINAR DE AUTOPSIA", main_title))
    story.append(Paragraph("JUZGADO DE INSTRUCCIÓN Nº 4 — REF. DILIGENCIAS: 2026-F892", sub_header))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#991B1B'), spaceAfter=10))

    meta_data = [
        [
            Paragraph("<b>SUJETO EXAMINADO:</b> D. Ricardo Valparaíso", body_text),
            Paragraph("<b>EDAD:</b> 72 años", body_text),
            Paragraph("<b>FECHA EXAMEN:</b> 30 de Octubre de 2026", body_text)
        ],
        [
            Paragraph("<b>HORA EXACTA DEL FALLECIMIENTO:</b> <font color='#991B1B'><b>18:30 HORAS</b></font>", body_bold),
            Paragraph("<b>ESTADO:</b> Rigidez cadavérica incipiente", body_text),
            Paragraph("<b>ESCENA DEL HALLAZGO:</b> Finca Valparaíso", body_text)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[210, 155, 158])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F3F4F6')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#D1D5DB')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E5E7EB')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # Diagrama Anatómico
    d = Drawing(523, 175)
    d.add(Rect(0, 0, 523, 175, fillColor=colors.HexColor('#FAFAFA'), strokeColor=colors.HexColor('#D1D5DB'), strokeWidth=1))
    d.add(String(14, 158, "MAPA ANATÓMICO PERICIAL DE TRAUMATISMOS Y TRAZADORES", fontName="Helvetica-Bold", fontSize=9, fillColor=colors.HexColor('#374151')))

    # Silueta anatómica
    d.add(Circle(120, 115, 18, fillColor=colors.HexColor('#E5E7EB'), strokeColor=colors.HexColor('#9CA3AF'), strokeWidth=1.2)) # Cabeza
    d.add(Rect(102, 50, 36, 54, rx=4, ry=4, fillColor=colors.HexColor('#E5E7EB'), strokeColor=colors.HexColor('#9CA3AF'), strokeWidth=1.2)) # Tronco
    d.add(Line(102, 92, 80, 45, strokeColor=colors.HexColor('#9CA3AF'), strokeWidth=4, strokeLineCap=1)) # Brazo izq
    d.add(Line(138, 92, 160, 45, strokeColor=colors.HexColor('#9CA3AF'), strokeWidth=4, strokeLineCap=1)) # Brazo der
    d.add(Line(110, 50, 108, 12, strokeColor=colors.HexColor('#9CA3AF'), strokeWidth=4, strokeLineCap=1)) # Pierna izq
    d.add(Line(130, 50, 132, 12, strokeColor=colors.HexColor('#9CA3AF'), strokeWidth=4, strokeLineCap=1)) # Pierna der

    # Marcador Lesión A (Cabeza)
    d.add(Circle(133, 127, 6, fillColor=colors.HexColor('#DC2626'), strokeColor=colors.HexColor('#7F1D1D'), strokeWidth=1.5))
    d.add(Line(133, 127, 210, 138, strokeColor=colors.HexColor('#DC2626'), strokeWidth=1.2))
    d.add(String(215, 137, "[ LESIÓN A ] TRAUMATISMO CRANEAL GRAVE (BRECHA OCCIPITAL)", fontName="Helvetica-Bold", fontSize=8.5, fillColor=colors.HexColor('#991B1B')))
    d.add(String(215, 125, "Impacto seco de alta inercia en la base posterior del cráneo. Compatible con caída libre de espaldas.", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#4B5563')))

    # Marcador Lesión B (Toxicología)
    d.add(Circle(120, 78, 6, fillColor=colors.HexColor('#7C3AED'), strokeColor=colors.HexColor('#4C1D95'), strokeWidth=1.5))
    d.add(Line(120, 78, 210, 80, strokeColor=colors.HexColor('#7C3AED'), strokeWidth=1.2))
    d.add(String(215, 79, "[ LESIÓN B ] TOXICOLOGÍA: COMPUESTO ACTIVO EN SANGRE (42.5 mg/L)", fontName="Helvetica-Bold", fontSize=8.5, fillColor=colors.HexColor('#5B21B6')))
    d.add(String(215, 67, "Sustancia química sin clasificar en el cribado inicial. Se requiere informe farmacológico especializado.", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#4B5563')))

    # Descarte balístico y punzante
    d.add(Rect(215, 14, 295, 38, fillColor=colors.HexColor('#F3F4F6'), strokeColor=colors.HexColor('#E5E7EB'), strokeWidth=0.8))
    d.add(String(222, 38, "DICTAMEN EXCLUSIVO DE LESIONES EXTERNAS:", fontName="Helvetica-Bold", fontSize=7.5, fillColor=colors.HexColor('#1F2937')))
    d.add(String(222, 27, "• CERO orificios o cavidades por proyectil balístico (descarta bala penetrante).", fontName="Helvetica", fontSize=7.5, fillColor=colors.HexColor('#374151')))
    d.add(String(222, 17, "• CERO heridas incisas o punzantes por arma blanca (descarta tijeras/punzón).", fontName="Helvetica", fontSize=7.5, fillColor=colors.HexColor('#374151')))

    story.append(d)
    story.append(Spacer(1, 10))

    story.append(Paragraph("SÍNTOMAS DETERMINANTES Y HALLAZGOS FORENSES", section_title))

    box_data = [
        [
            Paragraph(
                "<b>1. TRAUMATISMO CRANEAL SEVERO CON ROTURA CUTÁNEA (18:30 HORAS):</b><br/>"
                "La víctima presenta una brecha profunda de bordes irregulares en la región occipital izquierda, con hemorragia "
                "subaracnoidea inmediata. La orientación de la fractura es consistente con un impacto directo del cráneo "
                "contra una superficie rígida y plana como consecuencia de una <b>caída violenta e inesperada hacia atrás</b>.<br/>"
                "<i>Dictamen: Shock traumático irreversible inmediato a las 18:30 horas.</i>",
                card_text
            ),
            Image(qr_path, width=76, height=76)
        ],
        [
            Paragraph(
                "<b>2. CUADRO DE INTOXICACIÓN POR SUSTANCIA QUÍMICA SIN CATALOGAR:</b><br/>"
                "El análisis toxicológico arroja una concentración cuantificada de <b>42.5 mg/L</b> en el torrente circulatorio. "
                "El laboratorio no ha conseguido determinar el origen específico de la sustancia farmacéutica.<br/>"
                "<i>* AVISO MÉDICO-LEGAL: Un facultativo médico debe contrastar si esta concentración de 42.5 mg/L "
                "constituye una dosis letal o sub-letal antes de emitir juicio definitivo sobre envenenamiento.</i>",
                card_text
            ),
            Paragraph("<font size=7 color='#6B7280'>Escanear QR para acceso a datos espectrométricos de laboratorio</font>", sub_header)
        ]
    ]

    findings_table = Table(box_data, colWidths=[420, 103])
    findings_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#D1D5DB')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E5E7EB')),
        ('ALIGN', (1,0), (1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(findings_table)
    story.append(Spacer(1, 12))

    conclusions = (
        "<b>CONCLUSIÓN GENERAL DE LA AUTOPSIA:</b> El cadáver presentaba dos anomalías de máxima consideración: "
        "una brecha contusa occipital fulminante registrada a las <b>18:30 horas</b> y restos no tipificados de medicación/tóxico en sangre. "
        "Queda descartado el fallecimiento por disparo penetrante o herida cortante."
    )
    story.append(Paragraph(conclusions, body_text))

    # =========================================================================
    # DOCUMENTO 2: DOSSIER NOTARIAL Y PERFILES DE LOS ASISTENTES (PÁGINA 2)
    # =========================================================================
    story.append(PageBreak())

    story.append(Paragraph("DESPACHO DE ABOGACÍA & ALBACEAZGO NOTARIAL", top_badge))
    story.append(Paragraph("DOSSIER CONFIDENCIAL DE ASISTENTES A LA VELADA", main_title))
    story.append(Paragraph("REGISTRO PRELIMINAR DE ALLEGADOS Y ANTECEDENTES — DILIGENCIAS PRIVADAS", sub_header))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#1E3A8A'), spaceAfter=10))

    intro_abogacia = (
        "El presente dossier recoge los antecedentes verificados y el rol de las siete personas presentes en la mansión "
        "durante la noche del 30 de octubre. La redacción respeta la reserva legal y recopila indicios de interés patrimonial."
    )
    story.append(Paragraph(intro_abogacia, body_text))
    story.append(Spacer(1, 8))

    # Pistas de los 7 personajes en redacción totalmente neutra (sin marcar género)
    # Puzzle de letras en negrita: C - A - J - O - N - S - E - C - R - E - T - O
    characters_data = [
        [
            Paragraph("<b>PERFIL CINEGÉTICO (CAZADOR/A):</b><br/>Especialista en fauna y guardería de terrenos. <b>C</b>onservó labores técnicas en el Museo de Historia Natural de la capital hasta su repentino cese disciplinario tras descubrirse irregularidades en el catálogo de especímenes protegidos.", card_text),
            Paragraph("<b>PERFIL SANITARIO (MÉDICO/A):</b><br/>F<b>A</b>cultativo de acreditada trayectoria con consulta médica privada entre familias acaudaladas. Asumía la custodia, control y dispensación de la medicación diaria y confidencial del anfitrión.", card_text)
        ],
        [
            Paragraph("<b>PERFIL MUSICAL (CANTANTE):</b><br/>Artista solista y vocalista de referencia del afamado con<b>J</b>unto musical <b>S.V.X.</b> (Sinfonía Vocal X). Mantendría contactos reservados con el anfitrión para silenciar exclusivas de prensa que amenazaban sus giras.", card_text),
            Paragraph("<b>PERFIL MILITAR (GENERAL):</b><br/>Mando de alta graduaci<b>Ó</b>n del ejército condecorado en servicios logísticos. Mantenía correspondencia reservada y encuentros periódicos con la víctima respecto a expedientes confidenciales.", card_text)
        ],
        [
            Paragraph("<b>PERFIL DESCENDIENTE (NIETO/A):</b><br/>Aspirante a la fortu<b>N</b>a familiar con intereses en locales de ocio nocturno y plataformas virtuales de apuestas clandestinas. Frecuentes tensiones con el difunto por adelantos de capital y deudas apremiantes.", card_text),
            Paragraph("<b>PERFIL BOTÁNICO (JARDINERO/A):</b><br/>Re<b>S</b>ponsable de los accesos exteriores, cancelas y cuidado de la flora. Incorporación en plantilla reciente con documentación laboral acreditada procedente de otra comunidad autónoma.", card_text)
        ],
        [
            Paragraph("<b>PERFIL FRATERNO (HERMANO/A):</b><br/>G<b>E</b>stor de entidades mercantiles familiares. Solicitó reuniones urgentes con el anfitrión solicitando avales millonarios inmediatos para contener el colapso judicial y quiebra de sus sociedades.", card_text),
            Paragraph("<b>CLÁUSULA DE CUSTODIA PATRIMONIAL:</b><br/>El anfitrión custodiaba dossiers reservados en un <b>C</b>ompartimento privado de la mansión para garantizar la resolución ordenada de sus discrepancias familiares y mercantiles.", card_text)
        ]
    ]

    char_table = Table(characters_data, colWidths=[260, 263])
    char_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F9FAFB')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#D1D5DB')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E5E7EB')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(char_table)
    story.append(Spacer(1, 14))

    notarial_note = (
        "<b>ANOTACIÓN DEL ALBACEA JUDICIAL:</b> Varios legajos manuscritos del difunto contienen caracteres resaltados. "
        "Se ruega a los investigadores cotejar minuciosamente las letras en negrita distribuidas en este documento para "
        "descubrir la instrucción cifrada que el anfitrión dejó anotada antes de la cena."
    )
    story.append(Paragraph(notarial_note, body_text))

    # =========================================================================
    # DOCUMENTO 3: CRÓNICA MERCANTIL Y EXTRACTO BANCARIO (PÁGINA 3)
    # =========================================================================
    story.append(PageBreak())

    story.append(Paragraph("LA GACETA MERCANTIL & FINANCIERA — EDICIÓN VESPERTINA", top_badge))
    story.append(Paragraph("CRÓNICA DE MERCADOS Y AUDITORÍA DE FONDOS", main_title))
    story.append(Paragraph("BOLETÍN OFICIAL DE PROCEDIMIENTOS CONCURSALES Y MOVIMIENTOS BANCARIOS", sub_header))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#065F46'), spaceAfter=10))

    news_headline = Paragraph(
        "<font size=11 color='#991B1B'><b>BANCARROTA INMINENTE: EL GRUPO EMPRESARIAL DÁVILA SE HUNDE UN 78% Y SUSPENDE PAGOS</b></font>",
        body_text
    )
    news_body = Paragraph(
        "El conglomerado mercantil e inmobiliario familiar ha entrado formalmente en preconcurso de acreedores tras el desplome continuado de sus títulos en bolsa. "
        "Los tribunales mercantiles han advertido que se procederá al embargo total y liquidación de activos si la administración de la sociedad no aporta de forma inmediata "
        "un rescate financiero irrevocable de al menos dos millones de euros antes del fin de mes.",
        card_text
    )

    side_news_head = Paragraph("<b>CRECEN LAS SANCIONES POR REDES CLANDESTINAS DE JUEGO Y APUESTAS</b>", body_bold)
    side_news_body = Paragraph(
        "Las autoridades de supervisión financiera investigan plataformas offshore (Apex Bets) utilizadas para canalizar transferencias telemáticas rápidas destinadas a extinguir deudas de juego bajo amenazas de cobradores clandestinos.",
        card_text
    )

    news_data = [
        [
            [news_headline, Spacer(1, 4), news_body],
            [side_news_head, Spacer(1, 4), side_news_body]
        ]
    ]
    news_table = Table(news_data, colWidths=[335, 188])
    news_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor('#FFFFFF')),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor('#F3F4F6')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#D1D5DB')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E5E7EB')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(news_table)
    story.append(Spacer(1, 14))

    story.append(Paragraph("EXTRACTO OFICIAL DE MOVIMIENTOS BANCARIOS — DÍA 30 DE OCTUBRE", section_title))
    story.append(Paragraph("<b>TITULAR DE LA CUENTA:</b> D. Ricardo Valparaíso | <b>IBAN MATRIZ:</b> ES33 0049 1800 5511 2233 4455", body_text))
    story.append(Spacer(1, 6))

    # Las dos transferencias bancarias
    bank_data = [
        [
            Paragraph("<b>HORA REGISTRO</b>", body_bold),
            Paragraph("<b>CONCEPTO / OPERACIÓN BANCARIA</b>", body_bold),
            Paragraph("<b>CUENTA / CANAL DESTINO</b>", body_bold),
            Paragraph("<b>IMPORTE</b>", body_bold)
        ],
        [
            Paragraph("<b>17:45:10</b>", body_text),
            Paragraph("TRANSFERENCIA ORDINARIA URGENTE<br/><font size=7.5 color='#6B7280'>Concepto: Rescate societario / Crédito Dávila Corp</font>", card_text),
            Paragraph("ES84 2100 0418 9012 3456 7890<br/><font size=7.5 color='#6B7280'>Oficina Central Mercantil</font>", card_text),
            Paragraph("<font color='#991B1B'><b>- 1.850.000,00 €</b></font>", body_bold)
        ],
        [
            Paragraph("<font color='#991B1B'><b>18:28:44</b></font><br/><font size=7 color='#991B1B'><b>(Minutos antes)</b></font>", body_bold),
            Paragraph("TRANSFERENCIA TELEMÁTICA INMEDIATA IP-REMOTA<br/><font size=7.5 color='#6B7280'>Concepto: Liquidación saldo cuenta #9942 - Apex Bets</font>", card_text),
            Paragraph("ES12 0049 1823 4498 7654 3210<br/><font size=7.5 color='#6B7280'>Plataforma Remota Banca Móvil</font>", card_text),
            Paragraph("<font color='#991B1B'><b>- 14.250,00 €</b></font>", body_bold)
        ]
    ]

    bank_table = Table(bank_data, colWidths=[95, 200, 140, 88])
    bank_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E5E7EB')),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#FFFFFF')),
        ('BACKGROUND', (0,2), (-1,2), colors.HexColor('#FEF2F2')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#D1D5DB')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E5E7EB')),
        ('ALIGN', (3,0), (3,-1), 'RIGHT'),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(bank_table)
    story.append(Spacer(1, 14))

    bank_note = (
        "<b>DICTAMEN PERICIAL TELEMÁTICO:</b> La transferencia telemática instantánea registrada a las <b>18:28:44 horas</b> "
        "(escasos minutos antes de la hora fatal del óbito, establecida a las 18:30) fue emitida desde un dispositivo móvil "
        "mediante autenticación multifactor activa conectada a servidores de apuestas extranjeras. Quien emitió dicha orden se "
        "encontraba operando en ese instante el terminal telemático a distancia del foco del crimen."
    )
    story.append(Paragraph(bank_note, body_text))

    # Compilar documento
    doc.build(story)
    print("PDF compilado con éxito: 3 páginas independientes:", OUTPUT_PDF)

if __name__ == '__main__':
    build_pdf()

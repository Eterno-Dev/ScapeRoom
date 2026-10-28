import io
import os
import qrcode
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

CLUES_DATA = [
    {
        'num': 1,
        'title': 'Cuchillo ensangrentado',
        'category': 'Arma homicida',
        'token': 'k9x7m2',
        'desc': 'Colocar en: Cocina o bajo una tabla / mesa.'
    },
    {
        'num': 2,
        'title': 'Arañazo en la cerradura',
        'category': 'Evidencia de escena',
        'token': 'w3b8r5',
        'desc': 'Colocar en: Puerta o cerrojo de la habitación.'
    },
    {
        'num': 3,
        'title': 'Frasco de belladona',
        'category': 'Sustancia tóxica',
        'token': 'p7q2t4',
        'desc': 'Colocar en: Estantería o entre libros.'
    },
    {
        'num': 4,
        'title': 'Carta rasgada',
        'category': 'Documento sospechoso',
        'token': 'm5v8y1',
        'desc': 'Colocar en: Cajón, papelera o sobre una mesa.'
    },
    {
        'num': 5,
        'title': 'Reloj de bolsillo roto',
        'category': 'Objeto personal',
        'token': 'j4h6s9',
        'desc': 'Colocar en: Suelo o cerca de un mueble.'
    },
    {
        'num': 6,
        'title': 'Huellas de barro',
        'category': 'Rastro del sospechoso',
        'token': 'd2n8k3',
        'desc': 'Colocar en: Ventana, terraza o pasillo.'
    },
    {
        'num': 7,
        'title': 'Testamento tachado',
        'category': 'Móvil del crimen',
        'token': 'z6f3w8',
        'desc': 'Colocar en: Archivador, carpeta o escritorio.'
    },
    {
        'num': 8,
        'title': 'Copa de vino rota',
        'category': 'Evidencia química',
        'token': 'x8c5g1',
        'desc': 'Colocar en: Mesa de salón o mueble bar.'
    }
]

BASE_URL = 'https://eterno-dev.github.io/ScapeRoom/?p='

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=25,
        leftMargin=25,
        topMargin=25,
        bottomMargin=25
    )
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=17,
        leading=21,
        alignment=1, # Center
        textColor=colors.HexColor('#121214')
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        alignment=1,
        textColor=colors.HexColor('#52525b')
    )
    clue_num_style = ParagraphStyle(
        'ClueNum',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        alignment=1,
        textColor=colors.HexColor('#8b1e1e')
    )
    clue_title_style = ParagraphStyle(
        'ClueTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        alignment=1,
        textColor=colors.HexColor('#121214')
    )
    clue_cat_style = ParagraphStyle(
        'ClueCat',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        alignment=1,
        textColor=colors.HexColor('#71717a')
    )
    clue_desc_style = ParagraphStyle(
        'ClueDesc',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=10,
        alignment=1,
        textColor=colors.HexColor('#52525b')
    )
    
    story = []
    
    story.append(Paragraph('EL ASESINATO EMBRUJADO — PISTAS FÍSICAS QR', title_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph('Códigos QR imprimibles con enlaces especiales para colocar en la escena del juego.<br/>Escanea con la cámara del juego o la cámara nativa de cualquier smartphone.', subtitle_style))
    story.append(Spacer(1, 12))
    
    def make_cell(clue):
        url = BASE_URL + clue['token']
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=6,
            border=2,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color='black', back_color='white')
        
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        
        rl_img = RLImage(buf, width=125, height=125)
        
        cell_elements = [
            Spacer(1, 4),
            Paragraph(f"PISTA {clue['num']}", clue_num_style),
            Spacer(1, 2),
            Paragraph(clue['title'].upper(), clue_title_style),
            Paragraph(f"[{clue['category'].upper()}]", clue_cat_style),
            Spacer(1, 4),
            rl_img,
            Spacer(1, 4),
            Paragraph(clue['desc'], clue_desc_style),
            Spacer(1, 4)
        ]
        return cell_elements

    # Page 1: Clues 1 to 4
    row1 = [make_cell(CLUES_DATA[0]), make_cell(CLUES_DATA[1])]
    row2 = [make_cell(CLUES_DATA[2]), make_cell(CLUES_DATA[3])]
    t1 = Table([row1, row2], colWidths=[265, 265])
    t1.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#121214')),
        ('INNERGRID', (0,0), (-1,-1), 1, colors.HexColor('#d4d4d8')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t1)
    
    story.append(PageBreak())
    
    # Page 2: Clues 5 to 8
    story.append(Paragraph('EL ASESINATO EMBRUJADO — PISTAS FÍSICAS QR (PÁGINA 2)', title_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph('Recorta por la línea negra continua para tener tus 8 tarjetas físicas de evidencias.', subtitle_style))
    story.append(Spacer(1, 12))
    
    row3 = [make_cell(CLUES_DATA[4]), make_cell(CLUES_DATA[5])]
    row4 = [make_cell(CLUES_DATA[6]), make_cell(CLUES_DATA[7])]
    t2 = Table([row3, row4], colWidths=[265, 265])
    t2.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#121214')),
        ('INNERGRID', (0,0), (-1,-1), 1, colors.HexColor('#d4d4d8')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t2)
    
    doc.build(story)
    print(f'PDF created successfully at: {filename}')

if __name__ == '__main__':
    build_pdf('c:/Users/paucr/Documents/ScapeRoom/pistas_qr_imprimibles.pdf')
    build_pdf('c:/Users/paucr/Documents/CluedoWeb/pistas_qr_imprimibles.pdf')

import io
import os
import qrcode
import qrcode.image.svg
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

OBJECTS_DATA = [
    {
        'num': 2,
        'title': 'Llave grande',
        'category': 'Acceso / Puerta',
        'token': 'k9x7m2',
        'desc': 'Llave de hierro forjado. Para abrir una puerta de metal o cancela.'
    },
    {
        'num': 3,
        'title': 'Llave pequeña',
        'category': 'Cerradura Secreta',
        'token': 'w3b8r5',
        'desc': 'Llave dorada de joyero. Tirada junto a la caja de herramientas.'
    },
    {
        'num': 4,
        'title': 'Destornillador',
        'category': 'Herramienta',
        'token': 'p7q2t4',
        'desc': 'Instrumento de punta plana con signos de forcejeo en el salón.'
    },
    {
        'num': 5,
        'title': 'Collar',
        'category': 'Joya Valiosa',
        'token': 'm5v8y1',
        'desc': 'Collar de plata antigua perteneciente a una de las damas.'
    },
    {
        'num': 6,
        'title': 'Boli',
        'category': 'Escritura',
        'token': 'j4h6s9',
        'desc': 'Bolígrafo de latón con tinta fresca usada en el testamento.'
    },
    {
        'num': 7,
        'title': 'Candelabro',
        'category': 'Objeto Pesado',
        'token': 'd2n8k3',
        'desc': 'Candelabro señorial de bronce con una deformación en la base.'
    },
    {
        'num': 8,
        'title': 'Tijeras',
        'category': 'Corte',
        'token': 'z6f3w8',
        'desc': 'Tijeras de sastre largas con fibras del traje de la víctima.'
    },
    {
        'num': 9,
        'title': 'Medicina',
        'category': 'Fármaco / Botica',
        'token': 'x8c5g1',
        'desc': 'Frasco de vidrio oscuro con dosis alterada de medicación.'
    },
    {
        'num': 10,
        'title': 'Caja fuerte',
        'category': 'Seguridad',
        'token': 'b4m9v2',
        'desc': 'Caja de combinación metálica forzada y entreabierta.'
    },
    {
        'num': 11,
        'title': 'Papeles',
        'category': 'Documentación',
        'token': 'q7r3t8',
        'desc': 'Balances financieros y cartas de deuda con anotaciones secretas.'
    },
    {
        'num': 12,
        'title': 'Nota',
        'category': 'Mensaje Secreto',
        'token': 'h2j6k9',
        'desc': 'Nota de chantaje con la frase: "Sé lo que hiciste en el bosque".'
    },
    {
        'num': 13,
        'title': 'Copa',
        'category': 'Cristalería',
        'token': 'l5n8p1',
        'desc': 'Copa tallada abandonada con restos de vino y sedimento sospechoso.'
    },
    {
        'num': 14,
        'title': 'Carpeta',
        'category': 'Expediente',
        'token': 'v9w3x7',
        'desc': 'Carpeta de cuero con el borrador notarial y cláusula anulada.'
    },
    {
        'num': 15,
        'title': 'Cartuchos',
        'category': 'Munición',
        'token': 'c6d1f4',
        'desc': 'Vainas percutidas de escopeta detonadas la noche del crimen.'
    },
    {
        'num': 16,
        'title': 'Pluma',
        'category': 'Reliquia',
        'token': 'g8s4z2',
        'desc': 'Pluma estilográfica con plumín de oro e inicial grabada.'
    },
    {
        'num': 17,
        'title': 'Pasaporte',
        'category': 'Identidad',
        'token': 'pass7k',
        'desc': 'Pasaporte estadounidense con sellos consulares de Alaska.'
    }
]

BASE_URL = 'https://eterno-dev.github.io/ScapeRoom/?p='

def generate_qr_assets():
    qr_dirs = [
        'c:/Users/paucr/Documents/ScapeRoom/src/assets/images/qr',
        'c:/Users/paucr/Documents/CluedoWeb/src/assets/images/qr'
    ]
    for d in qr_dirs:
        os.makedirs(d, exist_ok=True)
        
    for item in OBJECTS_DATA:
        url = BASE_URL + item['token']
        pad_num = str(item['num']).padStart(2, '0') if hasattr(str(item['num']), 'padStart') else f"{item['num']:02d}"
        
        # PNG
        qr_png = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=8,
            border=2,
        )
        qr_png.add_data(url)
        qr_png.make(fit=True)
        img_png = qr_png.make_image(fill_color='black', back_color='white')
        
        # SVG
        factory = qrcode.image.svg.SvgPathImage
        qr_svg = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=2,
            image_factory=factory
        )
        qr_svg.add_data(url)
        qr_svg.make(fit=True)
        img_svg = qr_svg.make_image()
        
        for d in qr_dirs:
            img_png.save(os.path.join(d, f'qr-objeto-{pad_num}.png'))
            with open(os.path.join(d, f'qr-objeto-{pad_num}.svg'), 'wb') as f:
                img_svg.save(f)
                
    print('All QR PNG and SVG files generated in qr/ directories!')

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=25,
        leftMargin=25,
        topMargin=22,
        bottomMargin=22
    )
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        alignment=1,
        textColor=colors.HexColor('#121214')
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        alignment=1,
        textColor=colors.HexColor('#52525b')
    )
    clue_num_style = ParagraphStyle(
        'ClueNum',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=17,
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
    
    def make_cell(item):
        url = BASE_URL + item['token']
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=5,
            border=2,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color='black', back_color='white')
        
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        
        rl_img = RLImage(buf, width=110, height=110)
        
        cell_elements = [
            Spacer(1, 3),
            Paragraph(f"QR {item['num']} — OBJETO {item['num']}", clue_num_style),
            Spacer(1, 2),
            Paragraph(item['title'].upper(), clue_title_style),
            Paragraph(f"[{item['category'].upper()}]", clue_cat_style),
            Spacer(1, 3),
            rl_img,
            Spacer(1, 3),
            Paragraph(item['desc'], clue_desc_style),
            Spacer(1, 3)
        ]
        return cell_elements

    story = []
    
    # 15 items in chunks of 4 (pages 1 to 4)
    chunks = [OBJECTS_DATA[i:i+4] for i in range(0, len(OBJECTS_DATA), 4)]
    
    for page_idx, chunk in enumerate(chunks, start=1):
        story.append(Paragraph(f'EL ASESINATO EMBRUJADO — OBJETOS QR (PÁGINA {page_idx}/{len(chunks)})', title_style))
        story.append(Spacer(1, 3))
        story.append(Paragraph('Imprime, recorta por la línea negra y coloca cada tarjeta en la habitación.<br/>Al escanear con la cámara del juego se añadirá la tarjeta del objeto automáticamente a la baraja.', subtitle_style))
        story.append(Spacer(1, 10))
        
        # Build 2x2 rows
        row1 = [make_cell(chunk[0])]
        if len(chunk) > 1:
            row1.append(make_cell(chunk[1]))
        else:
            row1.append([])
            
        rows = [row1]
        if len(chunk) > 2:
            row2 = [make_cell(chunk[2])]
            if len(chunk) > 3:
                row2.append(make_cell(chunk[3]))
            else:
                row2.append([])
            rows.append(row2)
            
        t = Table(rows, colWidths=[265, 265])
        t.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#121214')),
            ('INNERGRID', (0,0), (-1,-1), 1, colors.HexColor('#d4d4d8')),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(t)
        
        if page_idx < len(chunks):
            story.append(PageBreak())
            
    doc.build(story)
    print(f'PDF created successfully at: {filename}')

if __name__ == '__main__':
    generate_qr_assets()
    build_pdf('c:/Users/paucr/Documents/ScapeRoom/pistas_qr_imprimibles.pdf')
    build_pdf('c:/Users/paucr/Documents/CluedoWeb/pistas_qr_imprimibles.pdf')

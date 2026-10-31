import io
import os
import sys

# Asegurar que siempre corra desde la raíz del proyecto
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(SCRIPT_DIR) in [".py", "py", "scripts"]:
    PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
else:
    PROJECT_ROOT = SCRIPT_DIR
os.chdir(PROJECT_ROOT)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

import qrcode
import qrcode.image.svg
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

OFFICIAL_CLUES = [
    {
        'letter': 'A',
        'title': 'Papeles',
        'category': 'Expediente Jurídico',
        'token': 'pap7a',
        'desc': 'Documentos de investigación aportados por el abogado.',
        'detail': 'Contiene el informe forense de la autopsia preliminar y el expediente de todos los acusados.',
        'tablePickup': False
    },
    {
        'letter': 'B',
        'title': 'Llave pequeña',
        'category': 'Cerradura Secreta',
        'token': 'llav2b',
        'desc': 'Llave pequeña. Parece para abrir algo que no es una puerta. Estaba encima del sofá.',
        'detail': 'Cerradura de dimensiones reducidas. Abre el buzón exterior (Pista K).',
        'tablePickup': False
    },
    {
        'letter': 'C',
        'title': 'Boli',
        'category': 'Objeto Militar',
        'token': 'bol9c',
        'desc': 'Boli caro con escudo militar grabado y las siglas GM (General Militar).',
        'detail': 'Bolígrafo de alta gama con grabado castrense oficial de Oficial Superior.',
        'tablePickup': False
    },
    {
        'letter': 'D',
        'title': 'Destornillador',
        'category': 'Herramienta',
        'token': 'des4d',
        'desc': 'Punta plana. Oculto intencionadamente en un lugar muy sospechoso.',
        'detail': 'Herramienta escondida a propósito con marcas recientes en el extremo de acero.',
        'tablePickup': False
    },
    {
        'letter': 'E',
        'title': 'Llave grande',
        'category': 'Acceso Principal',
        'token': 'llag5e',
        'desc': 'Llave grande de hierro. Parece que abre una puerta grande o cancela.',
        'detail': 'Pesada llave de hierro forjado diseñada para el portón exterior de la finca.',
        'tablePickup': False
    },
    {
        'letter': 'F',
        'title': 'Copa',
        'category': 'Cristalería',
        'token': 'cop3f',
        'desc': 'Copa de cristal tallado con restos secos de líquido y sedimento blanquecino.',
        'detail': 'Abandonada sobre una mesa auxiliar. El poso desprende un olor químico persistente.',
        'tablePickup': False
    },
    {
        'letter': 'G',
        'title': 'Pasaporte',
        'category': 'Identidad Oficial',
        'token': 'pass7g',
        'desc': 'Documento de viaje expedido bajo sellos de EE.UU. Sujeto a peritaje.',
        'detail': 'Inspección técnica de control fronterizo sobre sellos de Alaska y código MRZ.',
        'tablePickup': False
    },
    {
        'letter': 'H',
        'title': 'Periódico Warbes',
        'category': 'Prensa Financiera',
        'token': 'war8h',
        'desc': 'Revista de negocios y finanzas Warbes (desplome de Kronos y apuestas).',
        'detail': 'Edición vespertina especial. Recoge la prueba física en la mesa.',
        'tablePickup': True
    },
    {
        'letter': 'I',
        'title': 'Ticket roto',
        'category': 'Comprobante',
        'token': 'tic1i',
        'desc': 'Ticket roto. Parece que alguien lo tiró porque no sabía qué hacer con él.',
        'detail': 'Pase VIP rasgado con fecha 30.10 y valor $90.000. Recoge la prueba en la mesa.',
        'tablePickup': True
    },
    {
        'letter': 'K',
        'title': 'Buzón',
        'category': 'Correspondencia',
        'token': 'buz6k',
        'desc': 'Buzón exterior cerrado. Requiere la Llave pequeña (Pista B) para abrirse.',
        'detail': 'Cerradura exterior. Recoge las pistas de la parte K en la mesa.',
        'tablePickup': True
    }
]

BASE_URL = 'https://eterno-dev.github.io/ScapeRoom/?pista='

def generate_qr_assets():
    qr_dirs = [
        os.path.join(PROJECT_ROOT, 'src', 'assets', 'images', 'qr'),
        'C:/Users/paucr/Documents/ScapeRoom/src/assets/images/qr'
    ]
    for d in qr_dirs:
        os.makedirs(d, exist_ok=True)
        
    for item in OFFICIAL_CLUES:
        url = f"{BASE_URL}{item['letter']}&t={item['token']}"
        let = item['letter'].lower()
        
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
            # Guardar por letra canónica
            img_png.save(os.path.join(d, f"qr-pista-{let}.png"))
            with open(os.path.join(d, f"qr-pista-{let}.svg"), 'wb') as f:
                img_svg.save(f)
                
    print('All 10 QR PNG and SVG files generated in qr/ directories!')

def build_pdf(filename="pistas_qr_imprimibles.pdf"):
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
        fontSize=8.5,
        leading=11.5,
        alignment=1,
        textColor=colors.HexColor('#52525b')
    )
    clue_num_style = ParagraphStyle(
        'ClueNum',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=21,
        alignment=1,
        textColor=colors.HexColor('#991B1B')
    )
    clue_title_style = ParagraphStyle(
        'ClueTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=13.5,
        alignment=1,
        textColor=colors.HexColor('#121214')
    )
    clue_cat_style = ParagraphStyle(
        'ClueCat',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        alignment=1,
        textColor=colors.HexColor('#71717a')
    )
    clue_desc_style = ParagraphStyle(
        'ClueDesc',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=9.8,
        alignment=1,
        textColor=colors.HexColor('#374151')
    )
    table_pickup_style = ParagraphStyle(
        'TablePickup',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        alignment=1,
        textColor=colors.HexColor('#991B1B')
    )
    
    def make_cell(item):
        url = f"{BASE_URL}{item['letter']}&t={item['token']}"
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
        
        rl_img = RLImage(buf, width=105, height=105)
        
        cell_elements = [
            Spacer(1, 2),
            Paragraph(f"PISTA {item['letter']}", clue_num_style),
            Spacer(1, 2),
            Paragraph(item['title'].upper(), clue_title_style),
            Paragraph(f"[{item['category'].upper()}]", clue_cat_style),
            Spacer(1, 2),
            rl_img,
            Spacer(1, 2),
            Paragraph(item['desc'], clue_desc_style),
            Spacer(1, 2),
            Paragraph("<b>★ RECOGIDA FÍSICA OBLIGATORIA EN MESA ★</b>" if item['tablePickup'] else "<font color='#4B5563'>Escanea con la cámara del juego</font>", table_pickup_style),
            Spacer(1, 2)
        ]
        return cell_elements

    story = []
    
    # 10 clues in chunks of 4 (pages 1: 4 clues, page 2: 4 clues, page 3: 2 clues)
    chunks = [OFFICIAL_CLUES[i:i+4] for i in range(0, len(OFFICIAL_CLUES), 4)]
    
    for page_idx, chunk in enumerate(chunks, start=1):
        story.append(Paragraph(f'EL ASESINATO EN LA FINCA — TARJETAS QR DE PISTAS (PÁGINA {page_idx}/{len(chunks)})', title_style))
        story.append(Spacer(1, 2))
        story.append(Paragraph('Imprime, recorta por la línea y coloca cada tarjeta en la escena de la sala.<br/>Al escanear con la cámara del juego se añadirá automáticamente la carta del objeto al mazo interactivo.', subtitle_style))
        story.append(Spacer(1, 8))
        
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
            
        grid = Table(rows, colWidths=[270, 270])
        grid.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#000000')),
            ('INNERGRID', (0,0), (-1,-1), 0.8, colors.HexColor('#000000')),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FAFAFA')),
        ]))
        story.append(grid)
        
        if page_idx < len(chunks):
            story.append(PageBreak())
            
    doc.build(story)
    print(f"Generated printable QR PDF: {filename}")

if __name__ == '__main__':
    generate_qr_assets()
    build_pdf('pistas_qr_imprimibles.pdf')

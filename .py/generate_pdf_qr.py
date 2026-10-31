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
        'code': 'A-7$9K',
        'title': 'Papeles',
        'category': 'Expediente Jurídico',
        'tablePickup': True
    },
    {
        'letter': 'B',
        'code': 'B-4#2P',
        'title': 'Llave pequeña',
        'category': 'Cerradura Secreta',
        'tablePickup': True
    },
    {
        'letter': 'C',
        'code': 'C-8%1M',
        'title': 'Boli',
        'category': 'Objeto Militar',
        'tablePickup': True
    },
    {
        'letter': 'D',
        'code': 'D-3&5X',
        'title': 'Destornillador',
        'category': 'Herramienta',
        'tablePickup': True
    },
    {
        'letter': 'E',
        'code': 'E-9!4R',
        'title': 'Llave grande',
        'category': 'Acceso Principal',
        'tablePickup': True
    },
    {
        'letter': 'F',
        'code': 'F-2?8L',
        'title': 'Copa',
        'category': 'Cristalería',
        'tablePickup': True
    },
    {
        'letter': 'G',
        'code': 'G-5*7T',
        'title': 'Pasaporte y Diario',
        'category': 'Identidad / Manuscrito',
        'tablePickup': True
    },
    {
        'letter': 'H',
        'code': 'H-6@3W',
        'title': 'Periódico Warbes',
        'category': 'Prensa Financiera',
        'tablePickup': True
    },
    {
        'letter': 'I',
        'code': 'I-1#9Q',
        'title': 'Ticket roto',
        'category': 'Comprobante',
        'tablePickup': True
    },
    {
        'letter': 'J',
        'code': 'J-4$8Z',
        'title': 'Extracto bancario',
        'category': 'Documento Financiero',
        'tablePickup': True
    },
    {
        'letter': 'K',
        'code': 'K-8%2N',
        'title': 'Buzón',
        'category': 'Correspondencia',
        'tablePickup': True
    },
    {
        'letter': 'L',
        'code': 'L-7&4V',
        'title': 'Bote de pintura verde',
        'category': 'Jardinería / Exteriores',
        'tablePickup': True
    },
    {
        'letter': 'M',
        'code': 'M-3!6D',
        'title': 'Llave maestra',
        'category': 'Cerrajería / Acceso',
        'tablePickup': True
    },
    {
        'letter': 'N',
        'code': 'N-9*1B',
        'title': 'Nota y Móvil',
        'category': 'Mensaje / Móvil',
        'tablePickup': True
    },
    {
        'letter': 'O',
        'code': 'O-2?5H',
        'title': 'Móvil desechable',
        'category': 'Comunicaciones',
        'tablePickup': True
    },
    {
        'letter': 'P',
        'code': 'P-5#7J',
        'title': 'Teléfono móvil',
        'category': 'Grabaciones Telefónicas',
        'tablePickup': True
    },
    {
        'letter': 'Q',
        'code': 'Q-8$3C',
        'title': 'Caja fuerte',
        'category': 'Compartimento de Seguridad',
        'tablePickup': True
    },
    {
        'letter': 'R',
        'code': 'R-1%9F',
        'title': 'Ticket de compra',
        'category': 'Comprobante',
        'tablePickup': True
    },
    {
        'letter': 'S',
        'code': 'S-6&2Y',
        'title': 'Cartuchos',
        'category': 'Balística',
        'tablePickup': False
    },
    {
        'letter': 'T',
        'code': 'T-4!8S',
        'title': 'Ordenador',
        'category': 'Videovigilancia',
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
        url = f"{BASE_URL}{item['letter']}&c={item['code']}"
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
            img_png.save(os.path.join(d, f"qr-pista-{let}.png"))
            with open(os.path.join(d, f"qr-pista-{let}.svg"), 'wb') as f:
                img_svg.save(f)
                
    print(f'All {len(OFFICIAL_CLUES)} QR PNG and SVG files generated in qr/ directories!')

def build_pdf(filename="pistas_qr_imprimibles.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=20,
        leftMargin=20,
        topMargin=20,
        bottomMargin=20
    )
    
    styles = getSampleStyleSheet()
    
    clue_code_style = ParagraphStyle(
        'ClueCode',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=19,
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
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        alignment=1,
        textColor=colors.HexColor('#52525b')
    )
    table_pickup_style = ParagraphStyle(
        'TablePickup',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.8,
        leading=9.5,
        alignment=1,
        textColor=colors.HexColor('#991B1B')
    )
    
    def make_cell(item):
        if not item:
            return []
            
        url = f"{BASE_URL}{item['letter']}&c={item['code']}"
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
        
        rl_img = RLImage(buf, width=115, height=115)
        
        pickup_text = "<b>★ RECOGIDA FÍSICA EN MESA ★</b>" if item.get('tablePickup', True) else "&nbsp;"
        
        cell_elements = [
            Spacer(1, 4),
            Paragraph(f"<b>CÓDIGO: {item['code']}</b>", clue_code_style),
            Spacer(1, 3),
            Paragraph(item['title'].upper(), clue_title_style),
            Paragraph(f"[{item['category'].upper()}]", clue_cat_style),
            Spacer(1, 4),
            rl_img,
            Spacer(1, 5),
            Paragraph(pickup_text, table_pickup_style),
            Spacer(1, 4)
        ]
        return cell_elements

    story = []
    
    # 6 clues per page: 2 columns x 3 rows
    chunks = [OFFICIAL_CLUES[i:i+6] for i in range(0, len(OFFICIAL_CLUES), 6)]
    
    for page_idx, chunk in enumerate(chunks, start=1):
        rows = []
        for r in range(3):
            c1_idx = r * 2
            c2_idx = r * 2 + 1
            if c1_idx >= len(chunk) and c2_idx >= len(chunk):
                break
            c1 = chunk[c1_idx] if c1_idx < len(chunk) else None
            c2 = chunk[c2_idx] if c2_idx < len(chunk) else None
            rows.append([make_cell(c1), make_cell(c2)])
            
        grid = Table(rows, colWidths=[275, 275])
        grid.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#000000')),
            ('INNERGRID', (0,0), (-1,-1), 0.8, colors.HexColor('#000000')),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')),
        ]))
        story.append(grid)
        
        if page_idx < len(chunks):
            story.append(PageBreak())
            
    doc.build(story)
    print(f"Generated printable QR PDF: {filename} ({len(chunks)} pages, 6 QRs/page)")

if __name__ == '__main__':
    generate_qr_assets()
    build_pdf('pistas_qr_imprimibles.pdf')

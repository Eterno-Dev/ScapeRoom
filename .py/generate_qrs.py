"""
Generador de Códigos QR para 'El asesinato embrujado'
EternoDev Web Standards - Formatos SVG y PNG
"""

import os
import qrcode
import qrcode.image.svg

CLUES = [
    {
        "id": "PISTA-01",
        "title": "Cuchillo ensangrentado",
        "desc": "Hoja de acero inoxidable con restos hemáticos recientes. Hallado bajo las tablas de la cocina.",
        "type": "Arma"
    },
    {
        "id": "PISTA-02",
        "title": "Arañazo en la cerradura",
        "desc": "Profundas muescas de metal en el cerrojo del despacho. Indican apertura forzada desde el pasillo.",
        "type": "Escena"
    },
    {
        "id": "PISTA-03",
        "title": "Frasco de belladona",
        "desc": "Recipiente de boticario vacío con restos de extracto letal. Oculto tras los libros de medicina.",
        "type": "Veneno"
    },
    {
        "id": "PISTA-04",
        "title": "Carta rasgada",
        "desc": "Fragmento de misiva exigiendo 50.000 pesetas a cambio de silencio sobre la herencia.",
        "type": "Documento"
    },
    {
        "id": "PISTA-05",
        "title": "Reloj de bolsillo roto",
        "desc": "Esfera de plata agrietada. Las manecillas quedaron detenidas a las 23:42.",
        "type": "Objeto"
    },
    {
        "id": "PISTA-06",
        "title": "Huellas de barro",
        "desc": "Pisadas de calzado militar del número 43 procedentes del jardín hacia el balcón.",
        "type": "Rastro"
    },
    {
        "id": "PISTA-07",
        "title": "Testamento tachado",
        "desc": "Borrador notarial donde la cláusula principal del primogénito ha sido eliminada con tinta fresca.",
        "type": "Documento"
    },
    {
        "id": "PISTA-08",
        "title": "Copa de vino rota",
        "desc": "Cristal de Bohemia con restos de un sedimento blanquecino en el fondo.",
        "type": "Veneno"
    }
]

BASE_URL = "https://eterno-dev.github.io/ScapeRoom/"

def generate():
    svg_dir = os.path.join("src", "assets", "images", "svg")
    png_dir = os.path.join("src", "assets", "images", "png")
    os.makedirs(svg_dir, exist_ok=True)
    os.makedirs(png_dir, exist_ok=True)

    print("Generando codigos QR...")
    for clue in CLUES:
        content = f"{BASE_URL}?pista={clue['id']}"
        
        # 1. Generar SVG
        factory = qrcode.image.svg.SvgPathImage
        qr_svg = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=2,
            image_factory=factory
        )
        qr_svg.add_data(content)
        qr_svg.make(fit=True)
        svg_img = qr_svg.make_image(attrib={'class': 'qr-svg'})
        svg_path = os.path.join(svg_dir, f"qr-{clue['id'].lower()}.svg")
        svg_img.save(svg_path)

        # 2. Generar PNG
        qr_png = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=2
        )
        qr_png.add_data(content)
        qr_png.make(fit=True)
        png_img = qr_png.make_image(fill_color="#121214", back_color="#ffffff")
        png_path = os.path.join(png_dir, f"qr-{clue['id'].lower()}.png")
        png_img.save(png_path)

        print(f"  OK: {clue['id']} -> {svg_path} & {png_path}")

    print("Todos los QR se han generado correctamente.")

if __name__ == "__main__":
    generate()

import os
import pymupdf

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))

def build_documentos_investigacion(output_pdf="documentos_investigacion.pdf"):
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
    
    # Dimensiones estándar A4 en puntos (72 DPI)
    A4_WIDTH = 595.27557
    A4_HEIGHT = 841.88977
    page_rect = pymupdf.Rect(0, 0, A4_WIDTH, A4_HEIGHT)
    
    doc = pymupdf.open()
    
    for filename in pages:
        # Priorizar assets del proyecto; si no, buscar en el Escritorio
        local_path = os.path.join(dossier_dir, filename)
        desktop_path = os.path.join(desktop_dir, filename)
        
        img_path = local_path if os.path.exists(local_path) else desktop_path
        if not os.path.exists(img_path):
            raise FileNotFoundError(f"No se encontró la imagen: {filename}")
            
        page = doc.new_page(width=A4_WIDTH, height=A4_HEIGHT)
        page.insert_image(page_rect, filename=img_path)
        print(f"[OK] Insertada página A4: {filename} desde {img_path}")
        
    out_path = os.path.join(PROJECT_ROOT, output_pdf)
    doc.save(out_path, deflate=True)
    doc.close()
    print(f"Documento consolidado generado con éxito: {out_path} ({os.path.getsize(out_path)} bytes)")

if __name__ == "__main__":
    build_documentos_investigacion()

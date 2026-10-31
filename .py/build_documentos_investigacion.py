import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(SCRIPT_DIR) in [".py", "py", "scripts"]:
    PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
else:
    PROJECT_ROOT = SCRIPT_DIR
os.chdir(PROJECT_ROOT)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from build_all_game_documents import (
    generate_autopsia_pdf,
    generate_warbes_pdf,
    generate_perfiles_pdf,
    generate_pasaporte_pdf,
    generate_informe_medico_previo_pdf,
    generate_consolidated_pdf
)
from generate_periodico_dia import build_periodico_dia_pdf

if __name__ == "__main__":
    generate_autopsia_pdf()
    generate_warbes_pdf()
    generate_perfiles_pdf()
    generate_pasaporte_pdf()
    build_periodico_dia_pdf("5_periodico_dia.pdf")
    generate_informe_medico_previo_pdf()
    generate_consolidated_pdf("documentos_investigacion.pdf", "documentos_escritos.pdf")

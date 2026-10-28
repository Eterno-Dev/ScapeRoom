"""
Generador de Assets SVG Vectoriales para ScapeRoom (EternoDev Standard)
Sin emojis, sin degradados, diseno flat y limpio.
"""

import os

SVG_DIR = os.path.join("src", "assets", "images", "svg")
os.makedirs(SVG_DIR, exist_ok=True)

# 1. Icono Hombre (Aseo / Puerta)
male_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
  <circle cx="12" cy="4" r="2.5"/>
  <path d="M7 9a1 1 0 0 1 1-1h8a1 1 0 0 1 1 1v6a1 1 0 0 1-1 1h-1.5v6a1 1 0 0 1-1 1h-1a1 1 0 0 1-1-1v-6h-1v6a1 1 0 0 1-1 1h-1a1 1 0 0 1-1-1v-6H8a1 1 0 0 1-1-1V9z"/>
</svg>'''

# 2. Icono Mujer (Aseo / Puerta con falda)
female_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
  <circle cx="12" cy="4" r="2.5"/>
  <path d="M10 8h4a1 1 0 0 1 1 1l2 7a1 1 0 0 1-1 1h-2v4a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1v-4H8a1 1 0 0 1-1-1l2-7a1 1 0 0 1 1-1z"/>
</svg>'''

# 3. Icono Info / Pregunta (?)
info_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="10"/>
  <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/>
  <line x1="12" y1="17" x2="12.01" y2="17"/>
</svg>'''

# 4. Icono Cámara
camera_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/>
  <circle cx="12" cy="13" r="4"/>
</svg>'''

# 5. Icono Cerrar
close_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <line x1="18" y1="6" x2="6" y2="18"/>
  <line x1="6" y1="6" x2="18" y2="18"/>
</svg>'''

# 6. Icono Huella / Misterio
mystery_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
</svg>'''

with open(os.path.join(SVG_DIR, "icon-male.svg"), "w", encoding="utf-8") as f:
    f.write(male_svg)
with open(os.path.join(SVG_DIR, "icon-female.svg"), "w", encoding="utf-8") as f:
    f.write(female_svg)
with open(os.path.join(SVG_DIR, "icon-info.svg"), "w", encoding="utf-8") as f:
    f.write(info_svg)
with open(os.path.join(SVG_DIR, "icon-camera.svg"), "w", encoding="utf-8") as f:
    f.write(camera_svg)
with open(os.path.join(SVG_DIR, "icon-close.svg"), "w", encoding="utf-8") as f:
    f.write(close_svg)
with open(os.path.join(SVG_DIR, "icon-mystery.svg"), "w", encoding="utf-8") as f:
    f.write(mystery_svg)

# Generar 8 avatares vectoriales distintivos para hombre y mujer (flat, estilo perfil elegante)
roles = [
    ("m1", "f1", "#b91c1c", "Anfitrión"),
    ("m2", "f2", "#d97706", "Aristócrata"),
    ("m3", "f3", "#2563eb", "Médico"),
    ("m4", "f4", "#059669", "Detective"),
    ("m5", "f5", "#7c3aed", "Militar"),
    ("m6", "f6", "#0891b2", "Erudito"),
    ("m7", "f7", "#db2777", "Heredero"),
    ("m8", "f8", "#4b5563", "Clérigo")
]

for m_id, f_id, color, label in roles:
    # Avatar Masculino
    svg_m = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none">
      <rect width="100" height="100" fill="#1c1c20"/>
      <rect x="3" y="3" width="94" height="94" stroke="{color}" stroke-width="3"/>
      <circle cx="50" cy="38" r="18" fill="{color}"/>
      <path d="M22 84c0-16 12-28 28-28s28 12 28 28z" fill="{color}"/>
      <text x="50" y="94" fill="#ffffff" font-size="10" font-family="sans-serif" font-weight="bold" text-anchor="middle">{label}</text>
    </svg>'''
    with open(os.path.join(SVG_DIR, f"avatar-{m_id}.svg"), "w", encoding="utf-8") as f:
        f.write(svg_m)

    # Avatar Femenino
    svg_f = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none">
      <rect width="100" height="100" fill="#1c1c20"/>
      <rect x="3" y="3" width="94" height="94" stroke="{color}" stroke-width="3"/>
      <circle cx="50" cy="36" r="17" fill="{color}"/>
      <path d="M26 84c0-15 10-26 24-26s24 11 24 26z" fill="{color}"/>
      <polygon points="50,45 38,70 62,70" fill="#ffffff" opacity="0.3"/>
      <text x="50" y="94" fill="#ffffff" font-size="10" font-family="sans-serif" font-weight="bold" text-anchor="middle">{label}</text>
    </svg>'''
    with open(os.path.join(SVG_DIR, f"avatar-{f_id}.svg"), "w", encoding="utf-8") as f:
        f.write(svg_f)

print("Assets SVG vectoriales generados exitosamente.")

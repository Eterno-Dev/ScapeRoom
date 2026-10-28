# El Asesinato Embrujado — Escape Room Web Companion

Web companion interactiva para juegos de escape room y misterio presencial. Diseñada bajo los estándares de desarrollo de **EternoDev**.

## Características
- **Arquitectura GitHub Pages Ready**: `index.html` en raíz sin necesidad de pasos de build.
- **Minimalismo Extremo**: Interfaz táctil ultracompacta, diseño directo al grano sin textos de relleno.
- **Flat Design Sólido**: Sin degradados, alto contraste con paleta tenebrosa.
- **Cero Emojis**: Iconografía 100% vectorial SVG.
- **Selección de Género y Personajes**: 8 perfiles con adaptación automática masculina y femenina.
- **Escáner QR Integrado**: Detección de pistas físicas con la cámara del dispositivo (`jsQR` local offline).
- **Deck de Pistas Táctil**: Desplazamiento lateral (swipe horizontal con el dedo) para consultar los hallazgos y evidencias.
- **Lámina Imprimible**: Plantilla en `src/html/print-qrs.html` con las 8 pistas físicas listas para recortar.

## Estructura del Proyecto
```text
.
├── index.html                   <-- Entrada principal
├── README.md                    <-- Documentación
├── generate_qrs.py              <-- Generador de códigos QR con Python
├── generate_svg_assets.py       <-- Generador de iconos y avatares vectoriales
└── src/
    ├── html/                    <-- Lámina de impresión de QRs
    ├── css/                     <-- Hojas de estilo modulares
    ├── js/                      <-- Lógica JavaScript modular
    └── assets/
        └── images/              <-- Categorización estricta por extensión
            ├── png/
            ├── jpg/
            └── svg/
```

Desarrollado para **EternoDev**.

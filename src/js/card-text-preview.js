/**
 * TEMPORAL: Lógica del Panel de Ajuste de Outlines y Sombreados
 * Fija Barlow Condensed para Títulos y Fredoka para Subtítulos/Cartas.
 * Permite afinar grosores (4px a 8px) para cerrar orificios de letras interiores.
 */

export function initCardTextPreview() {
  const panel = document.getElementById("text-preview-panel");
  if (!panel) return;

  // Referencias a los elementos del formulario
  const toggleBtn = document.getElementById("btn-toggle-preview-panel");
  const flipAllBtn = document.getElementById("btn-flip-all-cards");
  const copyCssBtn = document.getElementById("btn-copy-preview-css");
  const copyToast = document.getElementById("preview-copy-toast");

  const outlineSlider = document.getElementById("preview-outline-slider");
  const outlineValBadge = document.getElementById("preview-outline-val-badge");
  const outlineMethodSelect = document.getElementById("preview-outline-method-select");
  const outlineColorInput = document.getElementById("preview-outline-color-input");
  const shadowTypeSelect = document.getElementById("preview-shadow-type-select");
  const shadowColorInput = document.getElementById("preview-shadow-color-input");
  const textColorSelect = document.getElementById("preview-text-color-select");
  const textColorInput = document.getElementById("preview-text-color-input");

  // Botones de presets de grosor (4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0)
  const thicknessPills = document.querySelectorAll("[data-outline-preset]");

  let areAllFlipped = false;
  let currentOutlineWidth = parseFloat(outlineSlider ? outlineSlider.value : 6.0);

  // Alternar Colapsar / Expandir panel
  if (toggleBtn) {
    toggleBtn.addEventListener("click", () => {
      panel.classList.toggle("minimized");
      const isMin = panel.classList.contains("minimized");
      toggleBtn.innerHTML = isMin ? "Expandir &blacktriangledown;" : "Minimizar &blacktriangle;";
    });
  }

  // Girar todas las cartas al mismo tiempo para ver el reverso
  if (flipAllBtn) {
    flipAllBtn.addEventListener("click", () => {
      areAllFlipped = !areAllFlipped;
      document.querySelectorAll(".char-card-flip").forEach(card => {
        if (areAllFlipped) {
          card.classList.add("is-flipped");
        } else {
          card.classList.remove("is-flipped");
        }
      });
      flipAllBtn.innerHTML = areAllFlipped 
        ? `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 4v6h6M23 20v-6h-6"/><path d="M20.49 9A9 9 0 0 0 5.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 0 1 3.51 15"/></svg> Ver Frente`
        : `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 4v6h6M23 20v-6h-6"/><path d="M20.49 9A9 9 0 0 0 5.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 0 1 3.51 15"/></svg> Girar Todas (Reverso)`;
    });
  }

  // Sincronizar select de color de texto con input color
  if (textColorSelect && textColorInput) {
    textColorSelect.addEventListener("change", () => {
      if (textColorSelect.value !== "custom") {
        textColorInput.value = textColorSelect.value;
      }
      applyStyles();
    });
    textColorInput.addEventListener("input", () => {
      textColorSelect.value = "custom";
      applyStyles();
    });
  }

  // Conversión de color HEX a RGBA para sombras suaves
  function hexToRgba(hex, alpha) {
    let cleanHex = hex.replace("#", "");
    if (cleanHex.length === 3) {
      cleanHex = cleanHex.split("").map(c => c + c).join("");
    }
    const r = parseInt(cleanHex.substring(0, 2), 16) || 0;
    const g = parseInt(cleanHex.substring(2, 4), 16) || 0;
    const b = parseInt(cleanHex.substring(4, 6), 16) || 0;
    return `rgba(${r}, ${g}, ${b}, ${alpha})`;
  }

  // Generador de anillo continuo de 36 ángulos para modo shadow
  function generateDenseShadowRing(radius, color) {
    if (radius <= 0) return [];
    const count = 36;
    const list = [];
    for (let i = 0; i < count; i++) {
      const rad = (i * 2 * Math.PI) / count;
      const x = (Math.cos(rad) * radius).toFixed(2);
      const y = (Math.sin(rad) * radius).toFixed(2);
      list.push(`${x}px ${y}px 0 ${color}`);
    }
    return list;
  }

  // Generador dinámico de sombras y outline vectorial limpio
  function computeStyles() {
    const outlineWidth = currentOutlineWidth;
    const outlineMethod = outlineMethodSelect ? outlineMethodSelect.value : "both";
    const outlineColor = outlineColorInput ? outlineColorInput.value : "#000000";
    const shadowType = shadowTypeSelect ? shadowTypeSelect.value : "glow-intense";
    const shadowColor = shadowColorInput ? shadowColorInput.value : "#000000";
    const textColor = textColorInput ? textColorInput.value : "#ffffff";

    let strokeTitle = "none";
    let strokeBio = "none";
    let shadowList = [];

    // Cálculo de grosor para título y bio
    // Para que los huecos de la 'e' y 'o' se sellen, bio usa casi el mismo grosor completo
    const bioStrokeWidth = outlineWidth > 0 ? (outlineWidth >= 5 ? outlineWidth : (outlineWidth * 0.95).toFixed(1)) : 0;

    // 1. TÉCNICA DE OUTLINE VECTORIAL LIMPIO
    if (outlineWidth > 0) {
      if (outlineMethod === "stroke" || outlineMethod === "both") {
        strokeTitle = `${outlineWidth}px ${outlineColor}`;
        strokeBio = `${bioStrokeWidth}px ${outlineColor}`;
      }

      if (outlineMethod === "shadow") {
        shadowList.push(...generateDenseShadowRing(outlineWidth, outlineColor));
      }
    }

    // 2. SOMBRA / AURA SUAVE (CON BLUR SUAVE PARA CERO PUNTITOS)
    const softShadowColor = hexToRgba(shadowColor, 0.85);
    const wideShadowColor = hexToRgba(shadowColor, 0.70);
    const deepShadowColor = hexToRgba(shadowColor, 0.50);

    if (shadowType === "glow-intense") {
      shadowList.push(
        `0 2px 6px ${softShadowColor}`,
        `0 0 14px ${wideShadowColor}`,
        `0 0 22px ${deepShadowColor}`
      );
    } else if (shadowType === "glow-soft") {
      shadowList.push(
        `0 1px 4px ${softShadowColor}`,
        `0 0 10px ${wideShadowColor}`
      );
    } else if (shadowType === "drop-3d") {
      shadowList.push(
        `3px 3px 0 ${outlineColor}`,
        `4px 4px 6px ${softShadowColor}`
      );
    } else if (shadowType === "drop-soft") {
      shadowList.push(
        `0 3px 8px ${softShadowColor}`,
        `0 6px 16px ${wideShadowColor}`
      );
    } else if (shadowType === "deep-contrast") {
      shadowList.push(
        `0 2px 4px rgba(0, 0, 0, 0.95)`,
        `0 4px 14px ${softShadowColor}`
      );
    }

    const finalShadow = shadowList.length > 0 ? shadowList.join(", ") : "none";

    return {
      fontTitle: "'Barlow Condensed', sans-serif",
      fontBio: "'Fredoka', sans-serif",
      textColor,
      strokeTitle,
      strokeBio,
      finalShadow,
      outlineWidth,
      outlineColor
    };
  }

  function applyStyles() {
    const s = computeStyles();
    const root = document.documentElement;

    root.style.setProperty("--preview-font-title", s.fontTitle);
    root.style.setProperty("--preview-font-bio", s.fontBio);
    root.style.setProperty("--preview-color-title", s.textColor);
    root.style.setProperty("--preview-color-bio", s.textColor);
    root.style.setProperty("--preview-stroke-title", s.strokeTitle);
    root.style.setProperty("--preview-stroke-bio", s.strokeBio);
    root.style.setProperty("--preview-shadow-title", s.finalShadow);
    root.style.setProperty("--preview-shadow-bio", s.finalShadow);

    if (outlineValBadge) {
      outlineValBadge.textContent = `${currentOutlineWidth.toFixed(1)}px`;
    }
  }

  // Slider continuo de grosor
  if (outlineSlider) {
    outlineSlider.addEventListener("input", (e) => {
      currentOutlineWidth = parseFloat(e.target.value);
      thicknessPills.forEach(p => {
        const val = parseFloat(p.getAttribute("data-outline-preset"));
        if (Math.abs(val - currentOutlineWidth) < 0.1) {
          p.classList.add("active");
        } else {
          p.classList.remove("active");
        }
      });
      applyStyles();
    });
  }

  // Presets de grosor
  thicknessPills.forEach(pill => {
    pill.addEventListener("click", () => {
      const val = parseFloat(pill.getAttribute("data-outline-preset"));
      if (isNaN(val)) return;

      currentOutlineWidth = val;
      if (outlineSlider) outlineSlider.value = val;

      thicknessPills.forEach(p => p.classList.remove("active"));
      pill.classList.add("active");

      applyStyles();
    });
  });

  // Escuchar cambios en los demás controles
  const inputs = [
    outlineMethodSelect,
    outlineColorInput,
    shadowTypeSelect,
    shadowColorInput
  ];

  inputs.forEach(input => {
    if (input) {
      input.addEventListener("input", () => applyStyles());
      input.addEventListener("change", () => applyStyles());
    }
  });

  // Copiar CSS al portapapeles
  if (copyCssBtn) {
    copyCssBtn.addEventListener("click", () => {
      const s = computeStyles();
      const cssString = `/* Estilos de Tipografía con Outline & Aura Suave */
/* Títulos: Barlow Condensed */
.char-active-name,
.modal-title,
.modal-confirm-title,
.modal-admin-title,
.modal-gender-subtitle,
.card-back-role-title,
.card-back-name,
.deck-card-counter {
  font-family: 'Barlow Condensed', sans-serif !important;
  color: ${s.textColor} !important;
  -webkit-text-stroke: ${s.strokeTitle};
  paint-order: stroke fill;
  text-shadow: ${s.finalShadow} !important;
}

/* Subtítulos y Biografía: Fredoka */
.card-back-bio,
.card-back-role,
.clue-back-description {
  font-family: 'Fredoka', sans-serif !important;
  font-weight: 700 !important;
  color: ${s.textColor} !important;
  -webkit-text-stroke: ${s.strokeBio};
  paint-order: stroke fill;
  text-shadow: ${s.finalShadow} !important;
}`;

      navigator.clipboard.writeText(cssString).then(() => {
        if (copyToast) {
          copyToast.style.display = "block";
          copyToast.textContent = "¡CSS copiado al portapapeles!";
          setTimeout(() => {
            copyToast.style.display = "none";
          }, 2400);
        }
      }).catch(() => {
        alert("Código CSS:\n\n" + cssString);
      });
    });
  }

  // Inicializar al cargar con 6.0px
  applyStyles();
}

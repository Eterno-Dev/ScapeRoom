/**
 * TEMPORAL: Lógica del Panel de Pruebas de Tipografía, Outlines y Sombreados
 * Modifica en tiempo real las variables CSS aplicadas a los reversos de las cartas
 * y a los textos de la interfaz con renderizado vectorial limpio (cero puntitos).
 */

export function initCardTextPreview() {
  const panel = document.getElementById("text-preview-panel");
  if (!panel) return;

  // Referencias a los elementos del formulario
  const toggleBtn = document.getElementById("btn-toggle-preview-panel");
  const flipAllBtn = document.getElementById("btn-flip-all-cards");
  const copyCssBtn = document.getElementById("btn-copy-preview-css");
  const copyToast = document.getElementById("preview-copy-toast");

  const fontTitleSelect = document.getElementById("preview-font-title-select");
  const fontBioSelect = document.getElementById("preview-font-bio-select");
  const outlineWidthSelect = document.getElementById("preview-outline-width-select");
  const outlineMethodSelect = document.getElementById("preview-outline-method-select");
  const outlineColorInput = document.getElementById("preview-outline-color-input");
  const shadowTypeSelect = document.getElementById("preview-shadow-type-select");
  const shadowColorInput = document.getElementById("preview-shadow-color-input");
  const textColorSelect = document.getElementById("preview-text-color-select");
  const textColorInput = document.getElementById("preview-text-color-input");
  const appOutlineCheckbox = document.getElementById("preview-app-outline-checkbox");

  // Presets
  const presetPills = document.querySelectorAll("[data-preview-preset]");

  let areAllFlipped = false;

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

  // Toggle de outline a toda la aplicación
  if (appOutlineCheckbox) {
    appOutlineCheckbox.addEventListener("change", () => {
      if (appOutlineCheckbox.checked) {
        document.body.classList.add("preview-outline-app-enabled");
      } else {
        document.body.classList.remove("preview-outline-app-enabled");
      }
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

  // Generador de anillo continuo de 36 ángulos (cero puntitos o muescas)
  function generateDenseShadowRing(radius, color) {
    if (radius <= 0) return [];
    const count = 36; // 36 puntos = 1 cada 10 grados, subpixel continuo
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
    const fontTitle = fontTitleSelect.value;
    const fontBio = fontBioSelect.value;
    const outlineWidth = parseFloat(outlineWidthSelect.value);
    const outlineMethod = outlineMethodSelect.value;
    const outlineColor = outlineColorInput.value;
    const shadowType = shadowTypeSelect.value;
    const shadowColor = shadowColorInput.value;
    const textColor = textColorInput.value;

    let strokeTitle = "none";
    let strokeBio = "none";
    let shadowList = [];

    // Cálculo proporcional de grosor para título y bio
    const bioStrokeWidth = outlineWidth > 0 ? Math.max(1.0, (outlineWidth * 0.85)).toFixed(1) : 0;

    // 1. TÉCNICA DE OUTLINE VECTORIAL LIMPIO
    if (outlineWidth > 0) {
      if (outlineMethod === "stroke" || outlineMethod === "both") {
        // Trazo vectorial puro por GPU sin dientes ni puntos
        strokeTitle = `${outlineWidth}px ${outlineColor}`;
        strokeBio = `${bioStrokeWidth}px ${outlineColor}`;
      }

      if (outlineMethod === "shadow") {
        // Anillo denso de 36 ángulos para máxima suavidad matemática
        shadowList.push(...generateDenseShadowRing(outlineWidth, outlineColor));
      }
    }

    // 2. SOMBRA / AURA SUAVE (CON BLUR SUAVE PARA CERO PUNTITOS)
    const softShadowColor = hexToRgba(shadowColor, 0.85);
    const wideShadowColor = hexToRgba(shadowColor, 0.70);
    const deepShadowColor = hexToRgba(shadowColor, 0.50);

    if (shadowType === "glow-intense") {
      // Aura intensa con desenfoque suave (sin aristas)
      shadowList.push(
        `0 2px 6px ${softShadowColor}`,
        `0 0 12px ${wideShadowColor}`,
        `0 0 20px ${deepShadowColor}`
      );
    } else if (shadowType === "glow-soft") {
      shadowList.push(
        `0 1px 4px ${softShadowColor}`,
        `0 0 10px ${wideShadowColor}`
      );
    } else if (shadowType === "drop-3d") {
      // Sombra 3D desplazada limpia
      shadowList.push(
        `3px 3px 0 ${outlineColor}`,
        `4px 4px 5px ${softShadowColor}`
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
    } else if (shadowType === "original") {
      shadowList.push(
        `0 1px 3px rgba(255, 255, 255, 0.95)`,
        `0 0 10px rgba(255, 255, 255, 0.85)`
      );
    }

    const finalShadow = shadowList.length > 0 ? shadowList.join(", ") : "none";

    return {
      fontTitle,
      fontBio,
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
  }

  // Escuchar cambios en todos los controles
  const inputs = [
    fontTitleSelect,
    fontBioSelect,
    outlineWidthSelect,
    outlineMethodSelect,
    outlineColorInput,
    shadowTypeSelect,
    shadowColorInput
  ];

  inputs.forEach(input => {
    if (input) {
      input.addEventListener("input", () => {
        presetPills.forEach(p => p.classList.remove("active"));
        applyStyles();
      });
      input.addEventListener("change", () => {
        presetPills.forEach(p => p.classList.remove("active"));
        applyStyles();
      });
    }
  });

  // Copiar CSS al portapapeles
  if (copyCssBtn) {
    copyCssBtn.addEventListener("click", () => {
      const s = computeStyles();
      const cssString = `/* Estilos de Texto para Cartas (Título Barlow Condensed + Bio Fredoka) */
.card-back-role-title {
  font-family: ${s.fontTitle};
  color: ${s.textColor};
  -webkit-text-stroke: ${s.strokeTitle};
  paint-order: stroke fill;
  text-shadow: ${s.finalShadow};
}

.card-back-bio {
  font-family: ${s.fontBio};
  color: ${s.textColor};
  -webkit-text-stroke: ${s.strokeBio};
  paint-order: stroke fill;
  text-shadow: ${s.finalShadow};
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

  // Presets preconfigurados
  const presetsData = {
    "fredoka-perfect": {
      fontTitle: "'Barlow Condensed', sans-serif",
      fontBio: "'Fredoka', sans-serif",
      outlineWidth: "2.5",
      outlineMethod: "both",
      outlineColor: "#000000",
      shadowType: "glow-intense",
      shadowColor: "#000000",
      textColor: "#ffffff"
    },
    "cartoon-pop": {
      fontTitle: "'Luckiest Guy', cursive",
      fontBio: "'Fredoka', sans-serif",
      outlineWidth: "2.5",
      outlineMethod: "both",
      outlineColor: "#000000",
      shadowType: "drop-3d",
      shadowColor: "#000000",
      textColor: "#ffffff"
    },
    "rounded-clean": {
      fontTitle: "'Barlow Condensed', sans-serif",
      fontBio: "'Fredoka', sans-serif",
      outlineWidth: "2",
      outlineMethod: "both",
      outlineColor: "#000000",
      shadowType: "glow-soft",
      shadowColor: "#000000",
      textColor: "#ffffff"
    },
    "comic-bangers": {
      fontTitle: "'Bangers', cursive",
      fontBio: "'Fredoka', sans-serif",
      outlineWidth: "3",
      outlineMethod: "both",
      outlineColor: "#000000",
      shadowType: "drop-3d",
      shadowColor: "#b91c1c",
      textColor: "#ffffff"
    },
    "poster-heavy": {
      fontTitle: "'Alfa Slab One', cursive",
      fontBio: "'Fredoka', sans-serif",
      outlineWidth: "2.2",
      outlineMethod: "both",
      outlineColor: "#000000",
      shadowType: "deep-contrast",
      shadowColor: "#000000",
      textColor: "#fef3c7"
    },
    "mystery-gothic": {
      fontTitle: "'Cinzel', serif",
      fontBio: "'Fredoka', sans-serif",
      outlineWidth: "2",
      outlineMethod: "both",
      outlineColor: "#b91c1c",
      shadowType: "deep-contrast",
      shadowColor: "#000000",
      textColor: "#ffffff"
    },
    "original-default": {
      fontTitle: "'Barlow Condensed', sans-serif",
      fontBio: "'Inter', sans-serif",
      outlineWidth: "0",
      outlineMethod: "stroke",
      outlineColor: "#000000",
      shadowType: "original",
      shadowColor: "#ffffff",
      textColor: "#121214"
    }
  };

  presetPills.forEach(pill => {
    pill.addEventListener("click", () => {
      const presetKey = pill.getAttribute("data-preview-preset");
      const config = presetsData[presetKey];
      if (!config) return;

      presetPills.forEach(p => p.classList.remove("active"));
      pill.classList.add("active");

      fontTitleSelect.value = config.fontTitle;
      fontBioSelect.value = config.fontBio;
      outlineWidthSelect.value = config.outlineWidth;
      outlineMethodSelect.value = config.outlineMethod;
      outlineColorInput.value = config.outlineColor;
      shadowTypeSelect.value = config.shadowType;
      shadowColorInput.value = config.shadowColor;
      textColorInput.value = config.textColor;
      textColorSelect.value = config.textColor;

      applyStyles();
    });
  });

  // Aplicar estilos iniciales exactos pedidos por el usuario:
  // Título: Barlow Condensed (por defecto) con outline
  // Subtítulos/Bio: Fredoka blanca con outline negro limpio y aura intensa
  if (presetsData["fredoka-perfect"]) {
    const defaultCfg = presetsData["fredoka-perfect"];
    fontTitleSelect.value = defaultCfg.fontTitle;
    fontBioSelect.value = defaultCfg.fontBio;
    outlineWidthSelect.value = defaultCfg.outlineWidth;
    outlineMethodSelect.value = defaultCfg.outlineMethod;
    outlineColorInput.value = defaultCfg.outlineColor;
    shadowTypeSelect.value = defaultCfg.shadowType;
    shadowColorInput.value = defaultCfg.shadowColor;
    textColorInput.value = defaultCfg.textColor;
    textColorSelect.value = defaultCfg.textColor;
  }

  applyStyles();
}

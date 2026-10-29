/**
 * TEMPORAL: Lógica del Panel de Pruebas de Tipografía, Outlines y Sombreados
 * Modifica en tiempo real las variables CSS aplicadas a los reversos de las cartas
 * y a los textos de la interfaz.
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

  // Generador dinámico de sombras y outline
  function computeStyles() {
    const fontTitle = fontTitleSelect.value;
    const fontBio = fontBioSelect.value;
    const outlineWidth = parseFloat(outlineWidthSelect.value);
    const outlineMethod = outlineMethodSelect.value;
    const outlineColor = outlineColorInput.value;
    const shadowType = shadowTypeSelect.value;
    const shadowColor = shadowColorInput.value;
    const textColor = textColorInput.value;

    let strokeCss = "none";
    let shadowList = [];

    // 1. Cálculo del Outline
    if (outlineWidth > 0) {
      if (outlineMethod === "stroke" || outlineMethod === "both") {
        strokeCss = `${outlineWidth}px ${outlineColor}`;
      }

      if (outlineMethod === "shadow" || outlineMethod === "both") {
        // Outline 8 direcciones mediante text-shadow (mantiene 100% el grosor de la letra)
        const d = outlineWidth;
        const dDiag = (outlineWidth * 0.707).toFixed(1);
        shadowList.push(
          `-${d}px 0 0 ${outlineColor}`,
          `${d}px 0 0 ${outlineColor}`,
          `0 -${d}px 0 ${outlineColor}`,
          `0 ${d}px 0 ${outlineColor}`,
          `-${dDiag}px -${dDiag}px 0 ${outlineColor}`,
          `${dDiag}px -${dDiag}px 0 ${outlineColor}`,
          `-${dDiag}px ${dDiag}px 0 ${outlineColor}`,
          `${dDiag}px ${dDiag}px 0 ${outlineColor}`
        );
      }
    }

    // 2. Cálculo de la Sombra / Glow
    if (shadowType === "glow-soft") {
      shadowList.push(`0 0 8px ${shadowColor}`);
    } else if (shadowType === "glow-intense") {
      shadowList.push(`0 1px 3px ${shadowColor}`, `0 0 14px ${shadowColor}`);
    } else if (shadowType === "drop-3d") {
      shadowList.push(`3px 3px 0 ${shadowColor}`, `4px 4px 2px rgba(0,0,0,0.5)`);
    } else if (shadowType === "drop-soft") {
      shadowList.push(`0 4px 10px ${shadowColor}`);
    } else if (shadowType === "deep-contrast") {
      shadowList.push(`0 2px 4px rgba(0,0,0,0.9)`, `0 4px 14px ${shadowColor}`);
    } else if (shadowType === "original") {
      shadowList.push(`0 1px 3px rgba(255, 255, 255, 0.95)`, `0 0 10px rgba(255, 255, 255, 0.85)`);
    }

    const finalShadow = shadowList.length > 0 ? shadowList.join(", ") : "none";

    return {
      fontTitle,
      fontBio,
      textColor,
      strokeCss,
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
    root.style.setProperty("--preview-color-bio", s.textColor === "#ffffff" ? "#f4f4f6" : s.textColor);
    root.style.setProperty("--preview-stroke-title", s.strokeCss);
    root.style.setProperty("--preview-stroke-bio", s.strokeCss !== "none" ? `1px ${s.outlineColor}` : "none");
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
        // Deseleccionar preset activo al modificar manualmente
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
      const cssString = `/* Estilos de Texto seleccionados para el Reverso de Cartas */
.card-back-role-title {
  font-family: ${s.fontTitle};
  color: ${s.textColor};
  -webkit-text-stroke: ${s.strokeCss};
  paint-order: stroke fill;
  text-shadow: ${s.finalShadow};
}

.card-back-bio {
  font-family: ${s.fontBio};
  color: ${s.textColor === "#ffffff" ? "#f4f4f6" : s.textColor};
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
      fontTitle: "'Fredoka', sans-serif",
      fontBio: "'Nunito', sans-serif",
      outlineWidth: "1.5",
      outlineMethod: "shadow",
      outlineColor: "#ffffff",
      shadowType: "glow-soft",
      shadowColor: "#ffffff",
      textColor: "#121214"
    },
    "comic-bangers": {
      fontTitle: "'Bangers', cursive",
      fontBio: "'Inter', sans-serif",
      outlineWidth: "3",
      outlineMethod: "both",
      outlineColor: "#000000",
      shadowType: "drop-3d",
      shadowColor: "#b91c1c",
      textColor: "#ffffff"
    },
    "poster-heavy": {
      fontTitle: "'Alfa Slab One', cursive",
      fontBio: "'Inter', sans-serif",
      outlineWidth: "2",
      outlineMethod: "both",
      outlineColor: "#000000",
      shadowType: "deep-contrast",
      shadowColor: "#000000",
      textColor: "#fef3c7"
    },
    "mystery-gothic": {
      fontTitle: "'Cinzel', serif",
      fontBio: "'Inter', sans-serif",
      outlineWidth: "1.5",
      outlineMethod: "both",
      outlineColor: "#b91c1c",
      shadowType: "deep-contrast",
      shadowColor: "#000000",
      textColor: "#ffffff"
    },
    "original-improved": {
      fontTitle: "'Barlow Condensed', sans-serif",
      fontBio: "'Inter', sans-serif",
      outlineWidth: "1.5",
      outlineMethod: "shadow",
      outlineColor: "#000000",
      shadowType: "glow-soft",
      shadowColor: "#ffffff",
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

  // Aplicar estilos iniciales al cargar
  applyStyles();
}

/**
 * ScapeRoom - Main Application Logic (EternoDev Standard)
 * Cero Degradados - Cero Emojis - Vanilla ES Modules
 * En Partida: Solo 1 carta visible en pantalla, pasando con swipe (deslizamiento lateral)
 */

import { CHARACTERS } from "./data/characters.js";
import { CLUES } from "./data/clues.js";

class ScapeRoomApp {
  constructor() {
    this.gender = localStorage.getItem("scaperoom_gender") || null;
    this.selectedCharId = parseInt(localStorage.getItem("scaperoom_char_id"), 10) || null;
    this.unlockedClues = JSON.parse(localStorage.getItem("scaperoom_clues") || "[]");

    this.stream = null;
    this.scanning = false;
    this.videoEl = null;
    this.canvasEl = document.createElement("canvas");
    this.canvasCtx = this.canvasEl.getContext("2d", { willReadFrequently: true });

    this.init();
  }

  init() {
    this.setupGlobalEvents();
    this.renderCharactersGrid();

    // Comprobar parámetros en la URL (escaneo directo desde cámara nativa)
    const params = new URLSearchParams(window.location.search);
    const pistaParam = params.get("pista");
    if (pistaParam) {
      this.unlockClue(pistaParam.toUpperCase());
    }

    // Comprobar estado inicial de género
    if (!this.gender) {
      this.showGenderModal();
    } else {
      this.applyGender(this.gender);
    }

    // Si ya tiene un personaje elegido previamente, entra directo y queda bloqueado
    if (this.selectedCharId) {
      this.enterGameView(this.selectedCharId);
    } else {
      this.showView("view-selection");
    }
  }

  /* ==========================================================================
     VISTAS Y MODALES
     ========================================================================== */
  showView(viewId) {
    document.querySelectorAll(".view").forEach(v => v.classList.remove("active"));
    const target = document.getElementById(viewId);
    if (target) {
      target.classList.add("active");
      window.scrollTo(0, 0);
    }
  }

  showGenderModal() {
    const modal = document.getElementById("gender-modal");
    if (modal) modal.classList.add("active");
  }

  closeGenderModal() {
    const modal = document.getElementById("gender-modal");
    if (modal) modal.classList.remove("active");
  }

  /* ==========================================================================
     LÓGICA DE GÉNERO Y PERSONAJES
     ========================================================================== */
  applyGender(gender) {
    this.gender = gender;
    localStorage.setItem("scaperoom_gender", gender);
    this.closeGenderModal();
    this.renderCharactersGrid();

    if (this.selectedCharId) {
      this.renderGameDeck();
    }
  }

  renderCharactersGrid() {
    const container = document.getElementById("characters-grid");
    if (!container) return;

    container.innerHTML = "";
    const activeGender = this.gender || "male";

    CHARACTERS.forEach(char => {
      const data = activeGender === "female" ? char.female : char.male;
      const isSelected = this.selectedCharId === char.id;
      const isLocked = this.selectedCharId !== null;
      const isDisabled = isLocked && !isSelected;

      const card = document.createElement("div");
      card.className = `flip-card char-card-flip ${isSelected ? "selected" : ""} ${isDisabled ? "disabled" : ""}`;
      card.setAttribute("data-char-id", char.id);

      card.innerHTML = `
        <div class="flip-card-inner">
          <!-- Cara Frontal -->
          <div class="flip-card-front">
            <img src="${data.cardImage}" alt="${data.name}" class="char-card-img" />
            <div class="flip-hint-badge">
              <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/></svg>
              Girar
            </div>
          </div>

          <!-- Cara Trasera -->
          <div class="flip-card-back">
            <div class="card-back-header">
              <span class="card-back-role">${data.role}</span>
              <h4 class="card-back-name">${data.name}</h4>
            </div>
            <p class="card-back-bio">${data.bio}</p>
            <div class="card-back-actions">
              ${!isLocked ? `<button class="btn-confirm-char" data-select-char="${char.id}">Elegir Personaje</button>` : `<span class="char-locked-badge">Elegido</span>`}
            </div>
            <div class="card-back-hint">Toca para volver al frente</div>
          </div>
        </div>
      `;

      card.addEventListener("click", (e) => {
        if (e.target.closest("[data-select-char]")) {
          e.stopPropagation();
          this.selectCharacter(char.id);
          return;
        }
        card.classList.toggle("is-flipped");
      });

      container.appendChild(card);
    });
  }

  selectCharacter(charId) {
    if (this.selectedCharId !== null) return; // Bloqueo estricto e irreversible

    this.selectedCharId = charId;
    localStorage.setItem("scaperoom_char_id", charId);
    this.renderCharactersGrid();

    setTimeout(() => {
      this.enterGameView(charId);
    }, 220);
  }

  enterGameView(charId) {
    this.selectedCharId = charId;
    this.showView("view-game");
    this.renderGameDeck();
  }

  /* ==========================================================================
     PANTALLA 2: MAZO DESLIZABLE (1 CARTA EN PANTALLA A LA VEZ)
     ========================================================================== */
  renderGameDeck() {
    const track = document.getElementById("game-deck-track");
    if (!track || !this.selectedCharId) return;

    const char = CHARACTERS.find(c => c.id === this.selectedCharId);
    if (!char) return;

    const charData = this.gender === "female" ? char.female : char.male;

    // Actualizar nombre en la barra superior
    const nameEl = document.getElementById("game-char-name");
    if (nameEl) nameEl.textContent = charData.name;

    track.innerHTML = "";

    // ------------------------------------------------------------------------
    // CARTA 0: PRESENTACIÓN DEL PERSONAJE (GIRO 3D)
    // ------------------------------------------------------------------------
    const charSlide = document.createElement("div");
    charSlide.className = "game-card-slide";
    charSlide.id = "slide-character-card";
    charSlide.innerHTML = `
      <div class="flip-card game-card-flip">
        <div class="flip-card-inner">
          <!-- Cara Frontal -->
          <div class="flip-card-front">
            <img src="${charData.cardImage}" alt="${charData.name}" class="char-card-img" />
            <div class="flip-hint-badge">
              <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/></svg>
              Toca para girar
            </div>
          </div>
          <!-- Cara Trasera -->
          <div class="flip-card-back">
            <div class="card-back-header">
              <span class="card-back-role">${charData.role}</span>
              <h4 class="card-back-name">${charData.name}</h4>
            </div>
            <p class="card-back-bio">${charData.bio}</p>
            <div class="card-back-hint" style="margin-top:auto;">Toca para volver al frente</div>
          </div>
        </div>
      </div>
    `;

    charSlide.querySelector(".game-card-flip").addEventListener("click", function() {
      this.classList.toggle("is-flipped");
    });

    track.appendChild(charSlide);

    // ------------------------------------------------------------------------
    // CARTA 1: ESCÁNER DE PISTAS QR (GIRO 3D)
    // ------------------------------------------------------------------------
    const scannerSlide = document.createElement("div");
    scannerSlide.className = "game-card-slide";
    scannerSlide.id = "slide-scanner-card";
    scannerSlide.innerHTML = `
      <div class="flip-card game-card-flip" id="scanner-flip-card">
        <div class="flip-card-inner">
          <!-- Cara Frontal del Escáner -->
          <div class="flip-card-front scanner-card-face">
            <div class="scanner-card-header">
              <span class="scanner-card-tag">Herramienta</span>
              <span class="scanner-card-title">Escáner QR</span>
            </div>

            <div class="scanner-video-wrapper" id="scanner-video-wrapper">
              <video id="scanner-video" playsinline muted></video>
              <div class="scanner-placeholder">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
                  <circle cx="12" cy="13" r="4"></circle>
                </svg>
                <span>Cámara Inactiva</span>
              </div>
              <div class="scanner-target-box"></div>
            </div>

            <button class="btn-scanner-toggle" id="btn-scanner-toggle">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
                <circle cx="12" cy="13" r="4"></circle>
              </svg>
              Activar escáner
            </button>

            <div class="code-manual-row">
              <input type="text" id="input-manual-code" class="input-code" placeholder="Código (ej: PISTA-01)" />
              <button class="btn-submit-code" id="btn-submit-code">Añadir</button>
            </div>

            <div class="card-back-hint" style="margin-top:auto;">Toca fuera para girar</div>
          </div>

          <!-- Cara Trasera del Escáner (Preparada para imagen) -->
          <div class="flip-card-back scanner-card-back">
            <div class="card-back-header">
              <span class="card-back-role">Detector Forense</span>
              <h4 class="card-back-name">Lector de Evidencias</h4>
            </div>
            <p class="card-back-bio">Escanea códigos QR físicos colocados en la escena. Cada pista descubierta se añadirá automáticamente a la derecha de este mazo deslizable.</p>
            <div class="card-back-hint" style="margin-top:auto;">Toca para volver al escáner</div>
          </div>
        </div>
      </div>
    `;

    // Giro al tocar fuera de controles interactivos
    scannerSlide.querySelector("#scanner-flip-card").addEventListener("click", function(e) {
      if (e.target.closest("#btn-scanner-toggle") || e.target.closest("#input-manual-code") || e.target.closest("#btn-submit-code")) {
        return;
      }
      this.classList.toggle("is-flipped");
    });

    track.appendChild(scannerSlide);

    // ------------------------------------------------------------------------
    // CARTAS 2+: PISTAS ESCANEADAS (AÑADIDAS AL LADO EN EL MAZO)
    // ------------------------------------------------------------------------
    this.unlockedClues.forEach((clueId, idx) => {
      const clue = CLUES[clueId];
      if (!clue) return;

      const clueSlide = document.createElement("div");
      clueSlide.className = "game-card-slide";
      clueSlide.id = `slide-clue-${clue.id.toLowerCase()}`;
      clueSlide.innerHTML = `
        <div class="flip-card game-card-flip">
          <div class="flip-card-inner">
            <!-- Cara Frontal de la Pista -->
            <div class="flip-card-front clue-front-face">
              <div class="clue-front-top">
                <span class="clue-card-tag" style="background-color: ${clue.tagColor};">${clue.category}</span>
                <span class="clue-card-id">${clue.id}</span>
              </div>
              <div class="clue-card-title">${clue.title}</div>
              <p class="clue-card-desc">${clue.desc}</p>
              <div class="clue-flip-prompt">
                <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/></svg>
                <span>Toca para voltear</span>
              </div>
            </div>

            <!-- Cara Trasera de la Pista -->
            <div class="flip-card-back clue-back-face">
              <div class="clue-back-header">
                <span class="clue-seal-badge">EVIDENCIA REGISTRADA</span>
                <span class="clue-card-id">${clue.id}</span>
              </div>
              <h4 class="clue-back-title">Análisis Forense</h4>
              <p class="clue-back-detail">${clue.detail}</p>
              <div class="clue-back-notes">
                <strong>Estado:</strong> Prueba física autenticada en el expediente.
              </div>
              <div class="clue-flip-prompt">
                <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/></svg>
                <span>Toca para volver</span>
              </div>
            </div>
          </div>
        </div>
      `;

      clueSlide.querySelector(".game-card-flip").addEventListener("click", function() {
        this.classList.toggle("is-flipped");
      });

      track.appendChild(clueSlide);
    });

    // Reasignar referencias de escáner
    this.videoEl = document.getElementById("scanner-video");
    this.attachScannerEvents();
    this.updateCardCounter();
  }

  attachScannerEvents() {
    const btnScanner = document.getElementById("btn-scanner-toggle");
    if (btnScanner) {
      btnScanner.onclick = () => this.toggleScanner();
    }

    const btnSubmit = document.getElementById("btn-submit-code");
    const inputCode = document.getElementById("input-manual-code");

    if (btnSubmit && inputCode) {
      btnSubmit.onclick = () => {
        const val = inputCode.value.trim().toUpperCase();
        if (val) {
          this.unlockClue(val);
          inputCode.value = "";
        }
      };

      inputCode.onkeydown = (e) => {
        if (e.key === "Enter") {
          const val = inputCode.value.trim().toUpperCase();
          if (val) {
            this.unlockClue(val);
            inputCode.value = "";
          }
        }
      };
    }
  }

  updateCardCounter() {
    const track = document.getElementById("game-deck-track");
    const counterEl = document.getElementById("deck-card-counter");
    if (!track || !counterEl) return;

    const slides = track.querySelectorAll(".game-card-slide");
    const total = slides.length;
    if (total === 0) return;

    // Calcular índice actual según el scroll horizontal
    const scrollLeft = track.scrollLeft;
    const slideWidth = slides[0].offsetWidth || 1;
    const currentIndex = Math.min(Math.round(scrollLeft / slideWidth) + 1, total);

    counterEl.textContent = `${currentIndex} / ${total}`;
  }

  /* ==========================================================================
     ESCÁNER QR Y CÓDIGOS FÍSICOS
     ========================================================================== */
  async toggleScanner() {
    if (this.scanning) {
      this.stopScanner();
    } else {
      await this.startScanner();
    }
  }

  async startScanner() {
    const videoWrapper = document.getElementById("scanner-video-wrapper");
    const toggleBtn = document.getElementById("btn-scanner-toggle");

    try {
      this.stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: "environment" }
      });
      if (this.videoEl) {
        this.videoEl.srcObject = this.stream;
        await this.videoEl.play();
      }

      this.scanning = true;
      if (videoWrapper) videoWrapper.classList.add("streaming");
      if (toggleBtn) {
        toggleBtn.classList.add("active");
        toggleBtn.innerHTML = `
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/></svg>
          Detener escáner
        `;
      }

      requestAnimationFrame(() => this.scanFrame());
    } catch (err) {
      console.warn("Acceso a cámara no disponible:", err);
      alert("No se pudo iniciar la cámara. Comprueba los permisos o introduce el código manualmente.");
      this.stopScanner();
    }
  }

  stopScanner() {
    this.scanning = false;
    if (this.stream) {
      this.stream.getTracks().forEach(track => track.stop());
      this.stream = null;
    }
    const videoWrapper = document.getElementById("scanner-video-wrapper");
    const toggleBtn = document.getElementById("btn-scanner-toggle");

    if (videoWrapper) videoWrapper.classList.remove("streaming");
    if (toggleBtn) {
      toggleBtn.classList.remove("active");
      toggleBtn.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg>
        Activar escáner
      `;
    }
  }

  scanFrame() {
    if (!this.scanning || !this.videoEl) return;

    if (this.videoEl.readyState === this.videoEl.HAVE_ENOUGH_DATA) {
      this.canvasEl.width = this.videoEl.videoWidth;
      this.canvasEl.height = this.videoEl.videoHeight;
      this.canvasCtx.drawImage(this.videoEl, 0, 0, this.canvasEl.width, this.canvasEl.height);

      const imageData = this.canvasCtx.getImageData(0, 0, this.canvasEl.width, this.canvasEl.height);

      if (window.jsQR) {
        const code = window.jsQR(imageData.data, imageData.width, imageData.height, {
          inversionAttempts: "dontInvert"
        });

        if (code && code.data) {
          const detected = this.extractClueId(code.data);
          if (detected) {
            this.handleDetectedCode(detected);
            return;
          }
        }
      }
    }

    if (this.scanning) {
      requestAnimationFrame(() => this.scanFrame());
    }
  }

  extractClueId(rawData) {
    if (!rawData) return null;
    const str = rawData.trim();
    if (str.startsWith("PISTA-")) {
      return str.toUpperCase();
    }
    try {
      const url = new URL(str);
      const param = url.searchParams.get("pista");
      if (param) return param.toUpperCase();
    } catch (e) {
      // No es URL
    }
    const match = str.match(/PISTA-\d+/i);
    return match ? match[0].toUpperCase() : null;
  }

  handleDetectedCode(clueId) {
    this.stopScanner();
    if (navigator.vibrate) {
      navigator.vibrate(80);
    }
    this.unlockClue(clueId);
  }

  unlockClue(clueId) {
    if (!CLUES[clueId]) {
      alert(`Código desconocido: ${clueId}`);
      return;
    }

    const alreadyAdded = this.unlockedClues.includes(clueId);
    if (!alreadyAdded) {
      this.unlockedClues.push(clueId); // Añadir a la derecha en el mazo deslizable
      localStorage.setItem("scaperoom_clues", JSON.stringify(this.unlockedClues));
    }

    this.renderGameDeck();

    // Desplazar automáticamente hacia la carta de la pista recién añadida
    setTimeout(() => {
      const targetCard = document.getElementById(`slide-clue-${clueId.toLowerCase()}`);
      if (targetCard) {
        targetCard.scrollIntoView({ behavior: "smooth", inline: "center", block: "nearest" });
      }
      this.updateCardCounter();
    }, 150);
  }

  /* ==========================================================================
     GLOBAL EVENT LISTENERS
     ========================================================================== */
  setupGlobalEvents() {
    // Modal de Género
    const btnMale = document.getElementById("btn-choose-male");
    const btnFemale = document.getElementById("btn-choose-female");

    if (btnMale) btnMale.addEventListener("click", () => this.applyGender("male"));
    if (btnFemale) btnFemale.addEventListener("click", () => this.applyGender("female"));

    // Botón de camarita en la cabecera: Salta directamente a la carta de escáner
    const btnGotoScanner = document.getElementById("btn-goto-scanner");
    if (btnGotoScanner) {
      btnGotoScanner.addEventListener("click", () => {
        const scannerSlide = document.getElementById("slide-scanner-card");
        if (scannerSlide) {
          scannerSlide.scrollIntoView({ behavior: "smooth", inline: "center", block: "nearest" });
          setTimeout(() => this.updateCardCounter(), 300);
        }
      });
    }

    // Listener de scroll en el mazo para actualizar el contador de carta visible
    const track = document.getElementById("game-deck-track");
    if (track) {
      track.addEventListener("scroll", () => {
        this.updateCardCounter();
      }, { passive: true });
    }
  }
}

// Inicialización en DOM Ready
document.addEventListener("DOMContentLoaded", () => {
  new ScapeRoomApp();
});

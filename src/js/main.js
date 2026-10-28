/**
 * ScapeRoom - Main Application Logic (EternoDev Standard)
 * Cero Degradados - Cero Emojis - Vanilla ES Modules
 * Mecánica Central: Tarjetas 3D Flip (Giro al pulsar) y Slider Lateral
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
    this.videoEl = document.getElementById("scanner-video");
    this.canvasEl = document.createElement("canvas");
    this.canvasCtx = this.canvasEl.getContext("2d", { willReadFrequently: true });

    this.init();
  }

  init() {
    this.setupEventListeners();
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

    this.renderCluesDeck();
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

  showInfoModal() {
    if (!this.selectedCharId || !this.gender) return;
    const char = CHARACTERS.find(c => c.id === this.selectedCharId);
    if (!char) return;

    const info = this.gender === "female" ? char.female : char.male;

    const avatarEl = document.getElementById("info-avatar");
    if (avatarEl) {
      avatarEl.src = info.cardImage;
    }
    document.getElementById("info-name").textContent = info.name;
    document.getElementById("info-role").textContent = info.role;
    document.getElementById("info-bio").textContent = info.bio;

    const modal = document.getElementById("info-modal");
    if (modal) modal.classList.add("active");
  }

  closeInfoModal() {
    const modal = document.getElementById("info-modal");
    if (modal) modal.classList.remove("active");
  }

  /* ==========================================================================
     LÓGICA DE GÉNERO Y PERSONAJES (CON GIRO 3D)
     ========================================================================== */
  applyGender(gender) {
    this.gender = gender;
    localStorage.setItem("scaperoom_gender", gender);
    this.closeGenderModal();
    this.renderCharactersGrid();

    if (this.selectedCharId) {
      this.updateActiveCharacterCard();
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

      // Evento de giro al tocar la tarjeta
      card.addEventListener("click", (e) => {
        // Si pulsó directamente el botón de elegir personaje, no solo gira sino que selecciona
        if (e.target.closest("[data-select-char]")) {
          e.stopPropagation();
          this.selectCharacter(char.id);
          return;
        }

        // De lo contrario, gira la tarjeta (toggle .is-flipped)
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

    // Transición fluida a la pantalla de juego
    setTimeout(() => {
      this.enterGameView(charId);
    }, 250);
  }

  enterGameView(charId) {
    this.selectedCharId = charId;
    this.updateActiveCharacterCard();
    this.showView("view-game");
    this.renderCluesDeck();
  }

  updateActiveCharacterCard() {
    if (!this.selectedCharId) return;
    const char = CHARACTERS.find(c => c.id === this.selectedCharId);
    if (!char) return;

    const data = this.gender === "female" ? char.female : char.male;

    // Actualizar nombre en la barra superior
    const nameEl = document.getElementById("game-char-name");
    if (nameEl) {
      nameEl.textContent = data.name;
    }

    // Actualizar tarjeta 3D en partida
    const imgEl = document.getElementById("game-char-img");
    const roleEl = document.getElementById("game-char-role");
    const fullnameEl = document.getElementById("game-char-fullname");
    const bioEl = document.getElementById("game-char-bio");

    if (imgEl) imgEl.src = data.cardImage;
    if (roleEl) roleEl.textContent = data.role;
    if (fullnameEl) fullnameEl.textContent = data.name;
    if (bioEl) bioEl.textContent = data.bio;
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
      this.videoEl.srcObject = this.stream;
      await this.videoEl.play();

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
      alert("No se pudo iniciar la cámara. Comprueba los permisos o introduce el código manualmente abajo.");
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
    if (!this.scanning) return;

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

    if (!this.unlockedClues.includes(clueId)) {
      this.unlockedClues.unshift(clueId); // Nueva tarjeta al frente del slider
      localStorage.setItem("scaperoom_clues", JSON.stringify(this.unlockedClues));
    }

    this.renderCluesDeck();

    // Desplazamiento horizontal fluido hacia la nueva tarjeta
    setTimeout(() => {
      const deck = document.getElementById("clues-deck-scroll");
      if (deck) {
        deck.scrollTo({ left: 0, behavior: "smooth" });
      }
    }, 120);
  }

  /* ==========================================================================
     SLIDER DE PISTAS CON GIRO 3D
     ========================================================================== */
  renderCluesDeck() {
    const deck = document.getElementById("clues-deck-scroll");
    const countEl = document.getElementById("clues-count-pill");
    if (!deck) return;

    if (countEl) {
      countEl.textContent = `${this.unlockedClues.length} / ${Object.keys(CLUES).length}`;
    }

    if (this.unlockedClues.length === 0) {
      deck.innerHTML = `
        <div class="empty-clues-placeholder">
          Aún no has registrado pistas.<br>Escanea un código QR físico para desbloquear pruebas en el slider.
        </div>
      `;
      return;
    }

    deck.innerHTML = "";

    this.unlockedClues.forEach(clueId => {
      const clue = CLUES[clueId];
      if (!clue) return;

      const card = document.createElement("div");
      card.className = "clue-flip-card";
      card.setAttribute("data-clue-id", clue.id);

      card.innerHTML = `
        <div class="clue-flip-inner">
          <!-- Cara Frontal -->
          <div class="clue-flip-front">
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

          <!-- Cara Trasera -->
          <div class="clue-flip-back">
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
      `;

      // Evento de giro de la tarjeta de pista
      card.addEventListener("click", () => {
        card.classList.toggle("is-flipped");
      });

      deck.appendChild(card);
    });
  }

  /* ==========================================================================
     EVENT LISTENERS
     ========================================================================== */
  setupEventListeners() {
    // Modal de Género
    const btnMale = document.getElementById("btn-choose-male");
    const btnFemale = document.getElementById("btn-choose-female");

    if (btnMale) {
      btnMale.addEventListener("click", () => this.applyGender("male"));
    }
    if (btnFemale) {
      btnFemale.addEventListener("click", () => this.applyGender("female"));
    }

    // Modal de Información del Personaje (?)
    const btnInfo = document.getElementById("btn-char-info");
    const btnCloseInfo = document.getElementById("btn-close-info");
    const infoModal = document.getElementById("info-modal");

    if (btnInfo) {
      btnInfo.addEventListener("click", () => this.showInfoModal());
    }
    if (btnCloseInfo) {
      btnCloseInfo.addEventListener("click", () => this.closeInfoModal());
    }
    if (infoModal) {
      infoModal.addEventListener("click", (e) => {
        if (e.target === infoModal) this.closeInfoModal();
      });
    }

    // Giro de la tarjeta del personaje activo en partida
    const activeCharFlip = document.getElementById("active-char-flip-card");
    if (activeCharFlip) {
      activeCharFlip.addEventListener("click", () => {
        activeCharFlip.classList.toggle("is-flipped");
      });
    }

    // Flechas del Slider de Pistas (Desplazamiento horizontal)
    const btnCluesPrev = document.getElementById("btn-clues-prev");
    const btnCluesNext = document.getElementById("btn-clues-next");
    const deck = document.getElementById("clues-deck-scroll");

    if (btnCluesPrev && deck) {
      btnCluesPrev.addEventListener("click", () => {
        deck.scrollBy({ left: -260, behavior: "smooth" });
      });
    }

    if (btnCluesNext && deck) {
      btnCluesNext.addEventListener("click", () => {
        deck.scrollBy({ left: 260, behavior: "smooth" });
      });
    }

    // Botón de activación del escáner
    const btnScanner = document.getElementById("btn-scanner-toggle");
    if (btnScanner) {
      btnScanner.addEventListener("click", () => this.toggleScanner());
    }

    // Entrada manual de código
    const btnSubmitCode = document.getElementById("btn-submit-code");
    const inputCode = document.getElementById("input-manual-code");

    if (btnSubmitCode && inputCode) {
      btnSubmitCode.addEventListener("click", () => {
        const val = inputCode.value.trim().toUpperCase();
        if (val) {
          this.unlockClue(val);
          inputCode.value = "";
        }
      });

      inputCode.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
          const val = inputCode.value.trim().toUpperCase();
          if (val) {
            this.unlockClue(val);
            inputCode.value = "";
          }
        }
      });
    }

    // Tecla ESC para cerrar modales
    window.addEventListener("keydown", (e) => {
      if (e.key === "Escape") {
        this.closeInfoModal();
      }
    });
  }
}

// Inicialización en DOM Ready
document.addEventListener("DOMContentLoaded", () => {
  new ScapeRoomApp();
});

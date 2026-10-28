/**
 * ScapeRoom - Main Application Logic (EternoDev Standard)
 * Cero Degradados - Cero Emojis - Vanilla ES Modules
 * Regla Estricta: Personaje Bloqueado (No se puede cambiar una vez elegido)
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

    // Comprobar estado inicial
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
     LÓGICA DE GÉNERO Y PERSONAJES
     ========================================================================== */
  applyGender(gender) {
    this.gender = gender;
    localStorage.setItem("scaperoom_gender", gender);
    this.closeGenderModal();
    this.renderCharactersGrid();

    if (this.selectedCharId) {
      this.updateActiveCharacterHeader();
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
      card.className = `char-card ${isSelected ? "selected" : ""} ${isDisabled ? "disabled" : ""}`;
      card.setAttribute("data-char-id", char.id);

      card.innerHTML = `
        <div class="char-card-frame">
          <img src="${data.cardImage}" alt="${data.name}" class="char-card-img" />
        </div>
      `;

      if (!isLocked) {
        card.addEventListener("click", () => {
          this.selectCharacter(char.id);
        });
      }

      container.appendChild(card);
    });
  }

  selectCharacter(charId) {
    if (this.selectedCharId !== null) return; // Bloqueo estricto

    this.selectedCharId = charId;
    localStorage.setItem("scaperoom_char_id", charId);
    this.renderCharactersGrid();

    // Transición visual
    setTimeout(() => {
      this.enterGameView(charId);
    }, 220);
  }

  enterGameView(charId) {
    this.selectedCharId = charId;
    this.updateActiveCharacterHeader();
    this.showView("view-game");
    this.renderCluesDeck();
  }

  updateActiveCharacterHeader() {
    if (!this.selectedCharId) return;
    const char = CHARACTERS.find(c => c.id === this.selectedCharId);
    if (!char) return;

    const data = this.gender === "female" ? char.female : char.male;
    const nameEl = document.getElementById("game-char-name");
    if (nameEl) {
      nameEl.textContent = data.name;
    }
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
      this.unlockedClues.unshift(clueId); // Nueva tarjeta al frente del scroll lateral
      localStorage.setItem("scaperoom_clues", JSON.stringify(this.unlockedClues));
    }

    this.renderCluesDeck();

    // Desplazamiento horizontal fluido hacia la nueva tarjeta
    setTimeout(() => {
      const deck = document.getElementById("clues-deck-scroll");
      if (deck) {
        deck.scrollTo({ left: 0, behavior: "smooth" });
      }
    }, 100);
  }

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
          Aún no has registrado pistas.<br>Escanea un código QR físico para desbloquear pruebas.
        </div>
      `;
      return;
    }

    deck.innerHTML = "";

    this.unlockedClues.forEach(clueId => {
      const clue = CLUES[clueId];
      if (!clue) return;

      const card = document.createElement("div");
      card.className = "clue-card-item";

      card.innerHTML = `
        <div class="clue-card-header">
          <span class="clue-card-tag" style="background-color: ${clue.tagColor};">${clue.category}</span>
          <span class="clue-card-id">${clue.id}</span>
        </div>
        <div class="clue-card-title">${clue.title}</div>
        <p class="clue-card-desc">${clue.desc}</p>
        <div class="clue-card-footer">
          <strong>Detalle forense:</strong> ${clue.detail}
        </div>
      `;

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

/**
 * ScapeRoom - Main Application Logic (EternoDev Standard)
 * Cero Degradados - Cero Emojis - Vanilla ES Modules
 * En Partida: Solo 1 carta visible en el centro, con swipe y flechas laterales animadas
 */

import { CHARACTERS } from "./data/characters.js";
import { CLUES, resolveClueId } from "./data/clues.js";

class ScapeRoomApp {
  constructor() {
    this.gender = localStorage.getItem("scaperoom_gender") || null;
    this.selectedCharId = parseInt(localStorage.getItem("scaperoom_char_id"), 10) || null;
    this.unlockedClues = JSON.parse(localStorage.getItem("scaperoom_clues") || "[]");

    // Asignar base trasera de pergamino fija por sesión si no existe
    this.savedBackBases = JSON.parse(localStorage.getItem("scaperoom_back_bases") || "{}");

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

    // Comprobar parámetros en la URL (escaneo directo desde cámara nativa con token único o pista)
    const params = new URLSearchParams(window.location.search);
    const rawClueParam = params.get("p") || params.get("token") || params.get("pista");
    if (rawClueParam) {
      const resolved = resolveClueId(rawClueParam);
      if (resolved) {
        this.unlockClue(resolved);
      }
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

  getBackBase(charId) {
    if (!this.savedBackBases[charId]) {
      const bases = ["card-back-base-1.png", "card-back-base-2.png", "card-back-base-3.png"];
      const randomBase = bases[Math.floor(Math.random() * bases.length)];
      this.savedBackBases[charId] = randomBase;
      localStorage.setItem("scaperoom_back_bases", JSON.stringify(this.savedBackBases));
    }
    return `src/assets/images/tarjetas/${this.savedBackBases[charId]}`;
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
      const backBaseUrl = this.getBackBase(char.id);

      const card = document.createElement("div");
      card.className = `flip-card char-card-flip ${isSelected ? "selected" : ""} ${isDisabled ? "disabled" : ""}`;
      card.setAttribute("data-char-id", char.id);

      card.innerHTML = `
        <div class="flip-card-inner">
          <!-- Cara Frontal -->
          <div class="flip-card-front">
            <img src="${data.cardImage}" alt="${data.name}" class="char-card-img" />
          </div>

          <!-- Cara Trasera con textura de pergamino de cartas especiales -->
          <div class="flip-card-back" style="background-image: url('${backBaseUrl}');">
            <div class="card-back-content">
              <div class="card-back-header">
                <span class="card-back-role">${data.role}</span>
                <h4 class="card-back-name">${data.name}</h4>
              </div>
              <p class="card-back-bio">${data.bio}</p>
              <div class="card-back-actions">
                ${!isLocked ? `<button class="btn-confirm-char" data-select-char="${char.id}">Elegir Personaje</button>` : `<span class="char-locked-badge">Elegido</span>`}
              </div>
            </div>
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
     PANTALLA 2: MAZO DESLIZABLE (SOLO 1 CARTA EN PANTALLA EN EL CENTRO)
     ========================================================================== */
  renderGameDeck() {
    const track = document.getElementById("game-deck-track");
    if (!track || !this.selectedCharId) return;

    const char = CHARACTERS.find(c => c.id === this.selectedCharId);
    if (!char) return;

    const charData = this.gender === "female" ? char.female : char.male;
    const backBaseUrl = this.getBackBase(char.id);

    // Actualizar nombre en la barra superior
    const nameEl = document.getElementById("game-char-name");
    if (nameEl) nameEl.textContent = charData.name;

    track.innerHTML = "";

    // ------------------------------------------------------------------------
    // CARTA 0: PRESENTACIÓN DEL PERSONAJE (GIRO 3D CON FONDO DE PERGAMINO)
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
          </div>
          <!-- Cara Trasera -->
          <div class="flip-card-back" style="background-image: url('${backBaseUrl}');">
            <div class="card-back-content">
              <div class="card-back-header">
                <span class="card-back-role">${charData.role}</span>
                <h4 class="card-back-name">${charData.name}</h4>
              </div>
              <p class="card-back-bio">${charData.bio}</p>
            </div>
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
          <!-- Cara Frontal del Escáner (Imagen de Cámara) -->
          <div class="flip-card-front">
            <img src="src/assets/images/objetos/card-scanner-camera.png" alt="Cámara de Investigación" class="char-card-img" />
          </div>

          <!-- Cara Trasera del Escáner (Cámara + Botón Activar Escáner) -->
          <div class="flip-card-back scanner-card-back" style="background-image: url('src/assets/images/tarjetas/card-back-base-2.png');">
            <div class="scanner-back-content">
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

              <p class="scanner-instruction-text">Hazle fotos a las pruebas</p>
            </div>
          </div>
        </div>
      </div>
    `;

    scannerSlide.querySelector("#scanner-flip-card").addEventListener("click", function(e) {
      if (e.target.closest("#btn-scanner-toggle")) {
        return;
      }
      this.classList.toggle("is-flipped");
    });

    track.appendChild(scannerSlide);

    // ------------------------------------------------------------------------
    // CARTAS 2+: OBJETOS ESCANEADOS (AÑADIDOS AL LADO EN EL MAZO)
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
            <!-- Cara Frontal del Objeto (Tarjeta de Imagen Real) -->
            <div class="flip-card-front">
              <img src="${clue.cardImage}" alt="${clue.title}" class="char-card-img" />
            </div>

            <!-- Cara Trasera del Objeto (Detalles e Información) -->
            <div class="flip-card-back clue-back-face" style="background-image: url('src/assets/images/tarjetas/${clue.backBase}');">
              <div class="card-back-content">
                <div class="card-back-header">
                  <span class="card-back-role">OBJETO ${clue.num} — ${clue.category}</span>
                  <h4 class="card-back-name">${clue.title}</h4>
                </div>
                <p class="card-back-bio">${clue.desc}</p>
                <div class="clue-back-detail">${clue.detail}</div>
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
    this.updateCardSliderState();
  }

  attachScannerEvents() {
    const btnScanner = document.getElementById("btn-scanner-toggle");
    if (btnScanner) {
      btnScanner.onclick = () => this.toggleScanner();
    }
  }

  updateCardSliderState() {
    const track = document.getElementById("game-deck-track");
    const counterEl = document.getElementById("deck-card-counter");
    const counterBottomEl = document.getElementById("deck-card-counter-bottom");
    const btnPrev = document.getElementById("btn-deck-prev");
    const btnNext = document.getElementById("btn-deck-next");

    if (!track) return;

    const slides = track.querySelectorAll(".game-card-slide");
    const total = slides.length;
    if (total === 0) return;

    const scrollLeft = track.scrollLeft;
    const trackWidth = track.clientWidth || 1;
    const currentIndex = Math.min(Math.max(0, Math.round(scrollLeft / trackWidth)), total - 1);

    const counterText = `${currentIndex + 1} / ${total}`;
    if (counterEl) {
      counterEl.textContent = counterText;
    }
    if (counterBottomEl) {
      counterBottomEl.textContent = counterText;
    }

    // Lógica dinámica de visibilidad de flechitas
    if (btnPrev) {
      if (currentIndex === 0) {
        btnPrev.classList.add("hidden");
      } else {
        btnPrev.classList.remove("hidden");
      }
    }

    if (btnNext) {
      if (currentIndex >= total - 1) {
        btnNext.classList.add("hidden");
      } else {
        btnNext.classList.remove("hidden");
      }
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

    try {
      const url = new URL(str);
      const param = url.searchParams.get("p") || url.searchParams.get("token") || url.searchParams.get("pista");
      if (param) {
        const resolved = resolveClueId(param);
        if (resolved) return resolved;
      }
    } catch (e) {
      // No es URL
    }

    return resolveClueId(str);
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
      const track = document.getElementById("game-deck-track");
      const targetCard = document.getElementById(`slide-clue-${clueId.toLowerCase()}`);
      if (track && targetCard) {
        targetCard.scrollIntoView({ behavior: "smooth", inline: "center", block: "nearest" });
      }
      this.updateCardSliderState();
    }, 150);
  }

  /* ==========================================================================
     GLOBAL EVENT LISTENERS
     ========================================================================== */
  setupGlobalEvents() {
    // Selección de género con tarjetas de imagen reales
    const btnMale = document.getElementById("btn-choose-male");
    const btnFemale = document.getElementById("btn-choose-female");

    if (btnMale) btnMale.addEventListener("click", () => this.applyGender("male"));
    if (btnFemale) btnFemale.addEventListener("click", () => this.applyGender("female"));

    // Botón debug para cambiar de género
    const btnBackToGender = document.getElementById("btn-back-to-gender");
    if (btnBackToGender) {
      btnBackToGender.addEventListener("click", () => {
        this.showGenderModal();
      });
    }

    // Botón debug para volver a selección de personajes
    const btnBackToSelection = document.getElementById("btn-back-to-selection");
    if (btnBackToSelection) {
      btnBackToSelection.addEventListener("click", () => {
        this.stopScanner();
        this.selectedCharId = null;
        localStorage.removeItem("scaperoom_char_id");
        this.showView("view-selection");
        this.renderCharactersGrid();
      });
    }

    // Botón de camarita en la cabecera: Salta directamente a la carta de escáner y la gira
    const btnGotoScanner = document.getElementById("btn-goto-scanner");
    if (btnGotoScanner) {
      btnGotoScanner.addEventListener("click", () => {
        const scannerSlide = document.getElementById("slide-scanner-card");
        if (scannerSlide) {
          scannerSlide.scrollIntoView({ behavior: "smooth", inline: "center", block: "nearest" });
          const flipCard = scannerSlide.querySelector(".game-card-flip");
          if (flipCard) flipCard.classList.add("is-flipped");
          setTimeout(() => this.updateCardSliderState(), 300);
        }
      });
    }

    // Flechitas flotantes de navegación con deslizamiento suave
    const btnPrev = document.getElementById("btn-deck-prev");
    const btnNext = document.getElementById("btn-deck-next");
    const track = document.getElementById("game-deck-track");

    if (btnPrev && track) {
      btnPrev.addEventListener("click", () => {
        track.scrollBy({ left: -track.clientWidth, behavior: "smooth" });
        setTimeout(() => this.updateCardSliderState(), 250);
      });
    }

    if (btnNext && track) {
      btnNext.addEventListener("click", () => {
        track.scrollBy({ left: track.clientWidth, behavior: "smooth" });
        setTimeout(() => this.updateCardSliderState(), 250);
      });
    }

    // Listener de scroll en el mazo para actualizar contador y visibilidad de flechas
    if (track) {
      track.addEventListener("scroll", () => {
        this.updateCardSliderState();
      }, { passive: true });
    }
  }
}

// Inicialización en DOM Ready
document.addEventListener("DOMContentLoaded", () => {
  new ScapeRoomApp();
});

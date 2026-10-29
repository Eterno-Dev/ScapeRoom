/**
 * ScapeRoom - Main Application Logic (EternoDev Standard)
 * Cero Degradados - Cero Emojis - Vanilla ES Modules
 * En Partida: Solo 1 carta visible en el centro, navegación fluida por swipe táctil y arrastre con ratón
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

    // Estado de arrastre con ratón para PC
    this.isDragging = false;
    this.hasDragged = false;
    this.dragStartX = 0;
    this.dragScrollStart = 0;

    // Id temporal para confirmación de personaje especial Administrador
    this.pendingAdminCharId = null;

    // Referencia al audio del reproductor de cassette de las Últimas Palabras
    this.currentCassetteAudio = null;

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

  showCodeModal() {
    const modal = document.getElementById("manual-code-modal");
    if (modal) {
      modal.classList.add("active");
      const input = document.getElementById("input-manual-code");
      if (input) {
        input.value = "";
        setTimeout(() => input.focus(), 150);
      }
    }
  }

  closeCodeModal() {
    const modal = document.getElementById("manual-code-modal");
    if (modal) modal.classList.remove("active");
  }

  showAdminConfirmModal(charId) {
    this.pendingAdminCharId = charId;
    const modal = document.getElementById("admin-confirm-modal");
    const titleEl = document.getElementById("admin-modal-role-title");
    const acceptBtn = document.getElementById("btn-accept-admin");
    const activeGender = this.gender || "male";
    if (titleEl) {
      titleEl.textContent = activeGender === "female" ? "ABOGADA" : "ABOGADO";
    }
    if (acceptBtn) {
      acceptBtn.textContent = activeGender === "female" ? "Soy administradora" : "Soy administrador";
    }
    if (modal) modal.classList.add("active");
  }

  closeAdminConfirmModal() {
    this.pendingAdminCharId = null;
    const modal = document.getElementById("admin-confirm-modal");
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

      const btnClass = char.isAdmin ? "btn-confirm-char btn-confirm-admin" : "btn-confirm-char";
      const btnText = "Elegir Personaje";
      const lockedText = "Elegido";

      const card = document.createElement("div");
      card.className = `flip-card char-card-flip ${isSelected ? "selected" : ""} ${isDisabled ? "disabled" : ""} ${char.isAdmin ? "is-admin-card" : ""}`;
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
                <h3 class="card-back-role-title">${data.role}</h3>
              </div>
              <p class="card-back-bio">${data.bio}</p>
              <div class="card-back-actions">
                ${!isLocked ? `<button class="${btnClass}" data-select-char="${char.id}">${btnText}</button>` : `<span class="char-locked-badge">${lockedText}</span>`}
              </div>
            </div>
          </div>
        </div>
      `;

      card.addEventListener("click", (e) => {
        if (e.target.closest("[data-select-char]")) {
          e.stopPropagation();
          if (char.isAdmin) {
            this.showAdminConfirmModal(char.id);
          } else {
            this.selectCharacter(char.id);
          }
          return;
        }

        const wasFlipped = card.classList.contains("is-flipped");
        // Solo 1 carta girada a la vez: devolver todas las demás cartas a su cara frontal
        container.querySelectorAll(".char-card-flip.is-flipped").forEach((otherCard) => {
          if (otherCard !== card) {
            otherCard.classList.remove("is-flipped");
          }
        });

        if (wasFlipped) {
          card.classList.remove("is-flipped");
        } else {
          card.classList.add("is-flipped");
        }
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

    // Actualizar nombre en la barra superior centrada
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
      <div class="flip-card game-card-flip ${char.isAdmin ? "is-admin-card" : ""}">
        <div class="flip-card-inner">
          <!-- Cara Frontal -->
          <div class="flip-card-front">
            <img src="${charData.cardImage}" alt="${charData.name}" class="char-card-img" />
          </div>
          <!-- Cara Trasera -->
          <div class="flip-card-back" style="background-image: url('${backBaseUrl}');">
            <div class="card-back-content">
              <div class="card-back-header">
                <h3 class="card-back-role-title">${charData.role}</h3>
              </div>
              <p class="card-back-bio">${charData.bio}</p>
            </div>
          </div>
        </div>
      </div>
    `;

    charSlide.querySelector(".game-card-flip").addEventListener("click", (e) => {
      if (this.hasDragged) return;
      e.currentTarget.classList.toggle("is-flipped");
    });

    track.appendChild(charSlide);

    // ------------------------------------------------------------------------
    // CARTA 1: CÁMARA (O CASSETTE DE ÚLTIMAS PALABRAS PARA EL ABOGADO)
    // ------------------------------------------------------------------------
    const scannerSlide = document.createElement("div");
    scannerSlide.className = "game-card-slide";
    scannerSlide.id = "slide-scanner-card";

    if (char.isAdmin) {
      // Tarjeta exclusiva para el Abogado: Cassette con las Últimas Palabras del difunto
      scannerSlide.innerHTML = `
        <div class="flip-card game-card-flip is-admin-card" id="scanner-flip-card">
          <div class="flip-card-inner">
            <!-- Cara Frontal de la Tarjeta (Imagen de Cámara con Borde Azul) -->
            <div class="flip-card-front">
              <img src="src/assets/images/objetos/card-scanner-camera.png" alt="Grabación de las Últimas Palabras" class="char-card-img" />
            </div>

            <!-- Cara Trasera: Reproductor de Cassette con Audio -->
            <div class="flip-card-back tape-card-back" style="background-image: url('src/assets/images/tarjetas/card-back-base-2.png');">
              <div class="tape-back-content">
                <div class="tape-header">
                  <span class="tape-badge">GRABACIÓN CONFIDENCIAL</span>
                  <h3 class="tape-title">ÚLTIMAS PALABRAS</h3>
                </div>

                <!-- Reproductor de Cassette -->
                <div class="cassette-player-box" id="cassette-player-box">
                  <div class="cassette-body">
                    <div class="cassette-label">DISQUETE TESTAMENTARIO</div>
                    <div class="cassette-window">
                      <div class="cassette-spool left-spool"></div>
                      <div class="cassette-tape-bridge"></div>
                      <div class="cassette-spool right-spool"></div>
                    </div>
                  </div>

                  <div class="audio-timeline">
                    <input type="range" class="audio-progress" id="audio-progress-bar" value="0" min="0" max="100" step="0.1" />
                    <div class="audio-time-row">
                      <span id="audio-time-current">0:00</span>
                      <span id="audio-time-total">--:--</span>
                    </div>
                  </div>

                  <div class="audio-controls-row">
                    <button class="btn-audio-reset" id="btn-audio-rewind" type="button" title="Reiniciar">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                        <polygon points="11 19 2 12 11 5 11 19"></polygon>
                        <polygon points="22 19 13 12 22 5 22 19"></polygon>
                      </svg>
                    </button>

                    <button class="btn-audio-play" id="btn-audio-play-toggle" type="button" title="Reproducir">
                      <svg class="icon-play" xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="currentColor">
                        <polygon points="5 3 19 12 5 21 5 3"></polygon>
                      </svg>
                      <svg class="icon-pause" style="display:none;" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                        <rect x="6" y="4" width="4" height="16"></rect>
                        <rect x="14" y="4" width="4" height="16"></rect>
                      </svg>
                    </button>
                  </div>

                  <audio id="audio-ultimas-palabras" src="src/assets/audio/ultimas_palabras.mp3" preload="metadata"></audio>
                </div>

                <!-- Transcripción del Audio para lectura -->
                <div class="tape-transcript-box">
                  <p>«Si estáis escuchando esto... mis sospechas eran ciertas: estoy muerto, y uno de vosotros me ha quitado la vida. Y el resto... habéis venido como buitres, esperando un cheque. Llevo meses notando cómo alguien intentaba acabar conmigo poco a poco... En la carpeta que custodia mi abogado hay documentos suficientes para mandar a prisión a cualquiera de los que estáis sentados en esa sala. Mi fortuna pasará íntegra a la persona que sea capaz de señalar con pruebas quién me ha matado y cómo lo ha hecho. Quien lo resuelva se queda con la herencia. Si vence el plazo y nadie descubre al culpable, mi abogado remitirá todos vuestros expedientes a los juzgados... Os quedaréis sin un céntimo, arruinados y compartiendo celda con mi asesino. Mi tiempo se ha acabado... pero el vuestro empieza ahora. Suerte.»</p>
                </div>

                <!-- Botón para escribir código de pistas -->
                <button class="btn-scanner-toggle btn-scanner-manual btn-scanner-blue" id="btn-open-code-modal" type="button">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                    <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                  </svg>
                  Introduce el código de la pista
                </button>
              </div>
            </div>
          </div>
        </div>
      `;

      scannerSlide.querySelector("#scanner-flip-card").addEventListener("click", (e) => {
        if (this.hasDragged) return;
        if (e.target.closest("#cassette-player-box") || e.target.closest("#btn-open-code-modal") || e.target.closest(".tape-transcript-box")) {
          return;
        }
        e.currentTarget.classList.toggle("is-flipped");
      });

      this.setupCassettePlayer(scannerSlide);
    } else {
      // Tarjeta estándar para los demás jugadores: Escáner de Cámara QR
      scannerSlide.innerHTML = `
        <div class="flip-card game-card-flip" id="scanner-flip-card">
          <div class="flip-card-inner">
            <!-- Cara Frontal del Escáner (Imagen de Cámara) -->
            <div class="flip-card-front">
              <img src="src/assets/images/objetos/card-scanner-camera.png" alt="Cámara de Investigación" class="char-card-img" />
            </div>

            <!-- Cara Trasera del Escáner (Cámara + Botón Activar Escáner + Acciones de Respaldo) -->
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
                  <div class="scanner-perm-alert" id="scanner-perm-alert" style="display: none;">
                    <p>Cámara no disponible</p>
                    <span>Permite la cámara en el navegador o usa las opciones de abajo.</span>
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

                <button class="btn-scanner-toggle btn-scanner-manual" id="btn-open-code-modal" type="button">
                  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                    <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                  </svg>
                  Introduce el código de la pista
                </button>
              </div>
            </div>
          </div>
        </div>
      `;

      scannerSlide.querySelector("#scanner-flip-card").addEventListener("click", (e) => {
        if (this.hasDragged) return;
        if (e.target.closest("#btn-scanner-toggle") || e.target.closest("#btn-open-code-modal")) {
          return;
        }
        e.currentTarget.classList.toggle("is-flipped");
      });
    }

    track.appendChild(scannerSlide);

    // ------------------------------------------------------------------------
    // CARTAS 2+: OBJETOS ESCANEADOS (AÑADIDOS AL LADO EN EL MAZO)
    // ------------------------------------------------------------------------
    this.unlockedClues.forEach((clueId) => {
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
              
              <!-- Letra Indicadora en la Esquina Superior (Identificador para sobres de pistas) -->
              <div class="clue-corner-letter" title="Pista ${clue.letter}">
                <span>${clue.letter}</span>
              </div>

              <!-- Escudo de Confidencialidad para Pistas Privadas (Ojito) -->
              ${clue.isPrivate ? `
                <div class="private-shield-overlay" id="shield-${clue.id}" style="background-image: url('src/assets/images/tarjetas/${clue.backBase}');">
                  <div class="shield-eye-icon-box">
                    <svg class="shield-eye-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
                      <line x1="1" y1="1" x2="23" y2="23"></line>
                    </svg>
                  </div>

                  <h3 class="shield-title">¿ESTÁS SEGURO?</h3>
                  <p class="shield-warning">
                    Esta pista contiene información reservada, no se puede compartir.
                  </p>

                  <button class="btn-reveal-sensitive" data-target-shield="shield-${clue.id}" type="button">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                      <circle cx="12" cy="13" r="3"></circle>
                    </svg>
                    <span>Clica para ver</span>
                  </button>
                </div>
              ` : ""}

              <div class="card-back-content">
                <div class="card-back-header">
                  <h4 class="card-back-name">${clue.title}</h4>
                </div>
                <p class="card-back-bio">${clue.desc}</p>
                <div class="clue-back-detail">${clue.detail}</div>

                ${clue.isPrivate ? `
                  <button class="btn-reshield-sensitive" data-shield-id="shield-${clue.id}" type="button">
                    <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path><line x1="1" y1="1" x2="23" y2="23"></line></svg>
                    Ocultar pista confidencial
                  </button>
                ` : ""}
              </div>

            </div>
          </div>
        </div>
      `;

      clueSlide.querySelector(".game-card-flip").addEventListener("click", (e) => {
        if (this.hasDragged) return;
        if (e.target.closest(".btn-reveal-sensitive") || e.target.closest(".btn-reshield-sensitive")) {
          return;
        }
        e.currentTarget.classList.toggle("is-flipped");
      });

      // Eventos para revelar u ocultar la pista confidencial
      if (clue.isPrivate) {
        const btnReveal = clueSlide.querySelector(".btn-reveal-sensitive");
        const btnReshield = clueSlide.querySelector(".btn-reshield-sensitive");
        const shieldEl = clueSlide.querySelector(`#shield-${clue.id}`);

        if (btnReveal && shieldEl) {
          btnReveal.addEventListener("click", (e) => {
            e.stopPropagation();
            shieldEl.classList.add("revealed");
          });
        }

        if (btnReshield && shieldEl) {
          btnReshield.addEventListener("click", (e) => {
            e.stopPropagation();
            shieldEl.classList.remove("revealed");
          });
        }
      }

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

    const btnOpenModal = document.getElementById("btn-open-code-modal");
    if (btnOpenModal) {
      btnOpenModal.onclick = () => this.showCodeModal();
    }
  }

  setupCassettePlayer(container) {
    const audio = container.querySelector("#audio-ultimas-palabras");
    const btnPlay = container.querySelector("#btn-audio-play-toggle");
    const btnRewind = container.querySelector("#btn-audio-rewind");
    const iconPlay = btnPlay?.querySelector(".icon-play");
    const iconPause = btnPlay?.querySelector(".icon-pause");
    const progressBar = container.querySelector("#audio-progress-bar");
    const timeCurrent = container.querySelector("#audio-time-current");
    const timeTotal = container.querySelector("#audio-time-total");
    const playerBox = container.querySelector("#cassette-player-box");

    if (!audio || !btnPlay) return;
    this.currentCassetteAudio = audio;

    const formatTime = (secs) => {
      if (isNaN(secs) || secs < 0) return "0:00";
      const m = Math.floor(secs / 60);
      const s = Math.floor(secs % 60);
      return `${m}:${s < 10 ? "0" : ""}${s}`;
    };

    audio.addEventListener("loadedmetadata", () => {
      if (timeTotal && !isNaN(audio.duration)) {
        timeTotal.textContent = formatTime(audio.duration);
      }
    });

    if (!isNaN(audio.duration) && audio.duration > 0 && timeTotal) {
      timeTotal.textContent = formatTime(audio.duration);
    }

    btnPlay.addEventListener("click", (e) => {
      e.stopPropagation();
      if (audio.paused) {
        audio.play().then(() => {
          playerBox?.classList.add("is-playing");
          if (iconPlay) iconPlay.style.display = "none";
          if (iconPause) iconPause.style.display = "block";
        }).catch(err => {
          console.warn("Audio play prevented:", err);
        });
      } else {
        audio.pause();
        playerBox?.classList.remove("is-playing");
        if (iconPlay) iconPlay.style.display = "block";
        if (iconPause) iconPause.style.display = "none";
      }
    });

    if (btnRewind) {
      btnRewind.addEventListener("click", (e) => {
        e.stopPropagation();
        audio.currentTime = 0;
        if (progressBar) progressBar.value = 0;
        if (timeCurrent) timeCurrent.textContent = "0:00";
      });
    }

    audio.addEventListener("timeupdate", () => {
      if (!isNaN(audio.duration) && audio.duration > 0) {
        const progress = (audio.currentTime / audio.duration) * 100;
        if (progressBar) progressBar.value = progress;
        if (timeCurrent) timeCurrent.textContent = formatTime(audio.currentTime);
        if (timeTotal && (timeTotal.textContent === "--:--" || timeTotal.textContent === "0:00")) {
          timeTotal.textContent = formatTime(audio.duration);
        }
      }
    });

    if (progressBar) {
      progressBar.addEventListener("input", (e) => {
        e.stopPropagation();
        if (!isNaN(audio.duration) && audio.duration > 0) {
          audio.currentTime = (progressBar.value / 100) * audio.duration;
        }
      });
      progressBar.addEventListener("click", (e) => e.stopPropagation());
    }

    audio.addEventListener("ended", () => {
      playerBox?.classList.remove("is-playing");
      if (iconPlay) iconPlay.style.display = "block";
      if (iconPause) iconPause.style.display = "none";
      if (progressBar) progressBar.value = 0;
      if (timeCurrent) timeCurrent.textContent = "0:00";
    });
  }

  stopCassetteAudio() {
    if (this.currentCassetteAudio) {
      this.currentCassetteAudio.pause();
      this.currentCassetteAudio.currentTime = 0;
      this.currentCassetteAudio = null;
    }
    const playerBox = document.getElementById("cassette-player-box");
    if (playerBox) playerBox.classList.remove("is-playing");
  }

  updateCardSliderState() {
    const track = document.getElementById("game-deck-track");
    const counterBottomEl = document.getElementById("deck-card-counter-bottom");

    if (!track) return;

    const slides = track.querySelectorAll(".game-card-slide");
    const total = slides.length;
    if (total === 0) return;

    const scrollLeft = track.scrollLeft;
    const trackWidth = track.clientWidth || 1;
    const currentIndex = Math.min(Math.max(0, Math.round(scrollLeft / trackWidth)), total - 1);

    const counterText = `${currentIndex + 1} / ${total}`;
    if (counterBottomEl) {
      counterBottomEl.textContent = counterText;
    }

    // Auto-volteo: La información nunca debe quedar a la vista al pasar de carta
    slides.forEach((slide, idx) => {
      if (idx !== currentIndex) {
        const flipCard = slide.querySelector(".flip-card");
        if (flipCard && flipCard.classList.contains("is-flipped")) {
          flipCard.classList.remove("is-flipped");
        }
        const shield = slide.querySelector(".private-shield-overlay");
        if (shield && shield.classList.contains("revealed")) {
          shield.classList.remove("revealed");
        }
      }
    });
  }

  snapToClosestCard() {
    const track = document.getElementById("game-deck-track");
    if (!track) return;
    const trackWidth = track.clientWidth || 1;
    const targetIndex = Math.round(track.scrollLeft / trackWidth);
    track.scrollTo({
      left: targetIndex * trackWidth,
      behavior: "smooth"
    });
    setTimeout(() => this.updateCardSliderState(), 200);
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
    const alertEl = document.getElementById("scanner-perm-alert");

    if (alertEl) alertEl.style.display = "none";

    try {
      // 1. Intentar con cámara trasera ideal
      try {
        this.stream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: { ideal: "environment" }, width: { ideal: 1280 } }
        });
      } catch (errConstraint) {
        // 2. Fallback a cualquier cámara de vídeo disponible
        this.stream = await navigator.mediaDevices.getUserMedia({ video: true });
      }

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
      if (alertEl) {
        alertEl.style.display = "block";
      }
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

  handlePhotoFile(file) {
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (e) => {
      const img = new Image();
      img.onload = () => {
        const canvas = document.createElement("canvas");
        canvas.width = img.width;
        canvas.height = img.height;
        const ctx = canvas.getContext("2d");
        ctx.drawImage(img, 0, 0);

        const imgData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        if (window.jsQR) {
          const code = window.jsQR(imgData.data, imgData.width, imgData.height, {
            inversionAttempts: "attemptBoth"
          });
          if (code && code.data) {
            const detected = this.extractClueId(code.data);
            if (detected) {
              this.handleDetectedCode(detected);
              return;
            }
          }
        }
        alert("No se detectó un código QR nítido en la imagen. Intenta enfocar más de cerca o escribe el código.");
      };
      img.src = e.target.result;
    };
    reader.readAsDataURL(file);
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
      alert(`Código desconocido o pista inexistente: ${clueId}`);
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
     GLOBAL EVENT LISTENERS & PC MOUSE DRAG
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

    // Botón para volver a selección de personajes con Doble Verificación
    const btnBackToSelection = document.getElementById("btn-back-to-selection");
    const confirmBackModal = document.getElementById("confirm-back-modal");
    const btnCancelBack = document.getElementById("btn-cancel-back");
    const btnAcceptBack = document.getElementById("btn-accept-back");

    if (btnBackToSelection) {
      btnBackToSelection.addEventListener("click", () => {
        if (confirmBackModal) {
          confirmBackModal.classList.add("active");
        }
      });
    }

    if (btnCancelBack && confirmBackModal) {
      btnCancelBack.addEventListener("click", () => {
        confirmBackModal.classList.remove("active");
      });
    }

    if (btnAcceptBack && confirmBackModal) {
      btnAcceptBack.addEventListener("click", () => {
        confirmBackModal.classList.remove("active");
        this.stopScanner();
        this.stopCassetteAudio();
        this.selectedCharId = null;
        localStorage.removeItem("scaperoom_char_id");
        this.showView("view-selection");
        this.renderCharactersGrid();
      });
    }

    // Modal de confirmación para Personaje Especial (Administrador)
    const btnCancelAdmin = document.getElementById("btn-cancel-admin");
    const btnAcceptAdmin = document.getElementById("btn-accept-admin");

    if (btnCancelAdmin) {
      btnCancelAdmin.addEventListener("click", () => {
        this.closeAdminConfirmModal();
      });
    }

    if (btnAcceptAdmin) {
      btnAcceptAdmin.addEventListener("click", () => {
        const charId = this.pendingAdminCharId;
        this.closeAdminConfirmModal();
        if (charId) {
          this.selectCharacter(charId);
        }
      });
    }

    // Botón de camarita en la cabecera: Salta directamente a la carta de escáner (mostrando la cara frontal de cámara)
    const btnGotoScanner = document.getElementById("btn-goto-scanner");
    if (btnGotoScanner) {
      btnGotoScanner.addEventListener("click", () => {
        const scannerSlide = document.getElementById("slide-scanner-card");
        if (scannerSlide) {
          // Asegurar que todas las cartas vuelvan a su cara frontal
          document.querySelectorAll(".game-card-flip.is-flipped").forEach(c => c.classList.remove("is-flipped"));
          scannerSlide.scrollIntoView({ behavior: "smooth", inline: "center", block: "nearest" });
          setTimeout(() => this.updateCardSliderState(), 300);
        }
      });
    }

    // Modal de entrada manual de códigos
    const btnCloseCodeModal = document.getElementById("btn-close-code-modal");
    if (btnCloseCodeModal) {
      btnCloseCodeModal.addEventListener("click", () => this.closeCodeModal());
    }

    const formManual = document.getElementById("form-manual-code");
    if (formManual) {
      formManual.addEventListener("submit", (e) => {
        e.preventDefault();
        const input = document.getElementById("input-manual-code");
        if (!input) return;
        const val = input.value.trim();
        const resolved = resolveClueId(val);
        if (resolved) {
          this.closeCodeModal();
          this.unlockClue(resolved);
        } else {
          alert(`Código no reconocido ("${val}"). Introduce el código de la pista.`);
        }
      });
    }

    // Listener de scroll en el mazo para actualizar contador
    const track = document.getElementById("game-deck-track");
    if (track) {
      track.addEventListener("scroll", () => {
        this.updateCardSliderState();
      }, { passive: true });

      // Configurar soporte de arrastre con ratón (Drag-to-Scroll) en PC
      this.setupMouseDrag(track);
    }
  }

  setupMouseDrag(track) {
    track.addEventListener("mousedown", (e) => {
      // Ignorar si se hace clic con botón secundario o en botones/inputs interactivos
      if (e.button !== 0 || e.target.closest("button") || e.target.closest("input")) return;
      this.isDragging = true;
      this.hasDragged = false;
      this.dragStartX = e.pageX - track.offsetLeft;
      this.dragScrollStart = track.scrollLeft;
      track.classList.add("is-dragging");
    });

    window.addEventListener("mouseup", () => {
      if (!this.isDragging) return;
      this.isDragging = false;
      track.classList.remove("is-dragging");
      if (this.hasDragged) {
        this.snapToClosestCard();
      }
    });

    track.addEventListener("mousemove", (e) => {
      if (!this.isDragging) return;
      e.preventDefault();
      const x = e.pageX - track.offsetLeft;
      const walk = x - this.dragStartX;
      if (Math.abs(walk) > 8) {
        this.hasDragged = true;
      }
      track.scrollLeft = this.dragScrollStart - walk;
    });
  }
}

// Inicialización en DOM Ready
document.addEventListener("DOMContentLoaded", () => {
  new ScapeRoomApp();
});

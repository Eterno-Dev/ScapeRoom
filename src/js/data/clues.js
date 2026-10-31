/**
 * Registro Oficial de Pistas y Objetos Físicos del Juego
 * CluedoWeb / ScapeRoom — Configuración de 10 Pistas Oficiales (A a J)
 */

export const CLUES = {
  "PISTA-A": {
    id: "PISTA-A",
    letter: "A",
    num: 1,
    token: "A",
    title: "Papeles",
    category: "Expediente Jurídico",
    cardImage: "src/assets/images/objetos/card-obj-11.png",
    backBase: "card-back-base-1.png",
    desc: "Documentos de investigación aportados por el abogado.",
    isPrivate: false,
    tablePickup: true
  },
  "PISTA-B": {
    id: "PISTA-B",
    letter: "B",
    num: 2,
    token: "B",
    title: "Llave pequeña",
    category: "Cerradura / Objeto Pequeño",
    cardImage: "src/assets/images/objetos/card-obj-3.png",
    backBase: "card-back-base-2.png",
    desc: "Llave pequeña. Parece para abrir algo que no es una puerta, parece de algo pequeño. Estaba encima del sofá.",
    isPrivate: false,
    tablePickup: true
  },
  "PISTA-C": {
    id: "PISTA-C",
    letter: "C",
    num: 3,
    token: "C",
    title: "Boli",
    category: "Objeto Militar",
    cardImage: "src/assets/images/objetos/card-obj-6.png",
    backBase: "card-back-base-3.png",
    desc: "Es un boli que parece bastante caro. Tiene un escudo militar grabado y las siglas GM (General Militar).",
    isPrivate: false,
    tablePickup: true
  },
  "PISTA-D": {
    id: "PISTA-D",
    letter: "D",
    num: 4,
    token: "D",
    title: "Destornillador",
    category: "Herramienta",
    cardImage: "src/assets/images/objetos/card-obj-4.png",
    backBase: "card-back-base-1.png",
    desc: "Es de punta plana y parece que estaba escondido casi a propósito. El lugar donde se encontraba era muy sospechoso; no es normal que termine ahí.",
    isPrivate: false,
    tablePickup: true
  },
  "PISTA-E": {
    id: "PISTA-E",
    letter: "E",
    num: 5,
    token: "E",
    title: "Llave grande",
    category: "Acceso Principal",
    cardImage: "src/assets/images/objetos/card-obj-2.png",
    backBase: "card-back-base-2.png",
    desc: "Llave grande. Parece que abre una puerta grande o una cancela principal.",
    isPrivate: false,
    tablePickup: true
  },
  "PISTA-F": {
    id: "PISTA-F",
    letter: "F",
    num: 6,
    token: "F",
    title: "Copa",
    category: "Cristalería",
    cardImage: "src/assets/images/objetos/card-obj-13.png",
    backBase: "card-back-base-3.png",
    desc: "Copa de cristal tallado con restos secos en la base y un poso blanquecino sospechoso.",
    isPrivate: false,
    tablePickup: true
  },
  "PISTA-G": {
    id: "PISTA-G",
    letter: "G",
    num: 7,
    token: "G",
    title: "Pasaporte",
    category: "Identidad",
    cardImage: "src/assets/images/objetos/card-obj-17.png",
    backBase: "card-back-base-1.png",
    desc: "Documento de viaje e identificación aparentemente oficial expedido bajo los sellos de los Estados Unidos.",
    isPrivate: false,
    tablePickup: true,
    linkedClues: ["PISTA-G2"]
  },
  "PISTA-G2": {
    id: "PISTA-G2",
    letter: "G",
    num: 7.2,
    token: "G",
    title: "Hoja de diario",
    category: "Manuscrito Personal",
    cardImage: "src/assets/images/objetos/card-obj-12.png",
    backBase: "card-back-base-3.png",
    desc: "Parece una hoja de diario escrita a mano.",
    isPrivate: false,
    tablePickup: true
  },
  "PISTA-H": {
    id: "PISTA-H",
    letter: "H",
    num: 8,
    token: "H",
    title: "Periódico Warbes",
    category: "Prensa Financiera",
    cardImage: "src/assets/images/objetos/card-obj-10.png",
    backBase: "card-back-base-2.png",
    desc: "Revista de negocios y página de periódico sobre finanzas y emprendimiento, llamada Warbes (como Forbes pero con W).",
    isPrivate: false,
    tablePickup: true
  },
  "PISTA-I": {
    id: "PISTA-I",
    letter: "I",
    num: 9,
    token: "I",
    title: "Ticket roto",
    category: "Comprobante",
    cardImage: "src/assets/images/objetos/card-obj-14.png",
    backBase: "card-back-base-3.png",
    desc: "Un ticket roto. Parece que alguien lo ha tirado porque no sabía qué hacer con él.",
    isPrivate: false,
    tablePickup: true
  },
  "PISTA-J": {
    id: "PISTA-J",
    letter: "J",
    num: 10,
    token: "J",
    title: "Extracto bancario",
    category: "Documento Financiero",
    cardImage: "src/assets/images/objetos/card-obj-15.png",
    backBase: "card-back-base-2.png",
    desc: "Extracto de movimientos bancarios y transferencias de cuentas de alta cuantía.",
    isPrivate: false,
    tablePickup: true
  },
  "PISTA-K": {
    id: "PISTA-K",
    letter: "K",
    num: 11,
    token: "K",
    title: "Buzón",
    category: "Correspondencia",
    cardImage: "src/assets/images/objetos/card-obj-12.png",
    backBase: "card-back-base-1.png",
    desc: "Buzón exterior cerrado con combinación. Introduce el código de la llave para abrirlo.",
    requiresCode: true,
    passcode: "4821",
    isPrivate: false,
    tablePickup: true
  },
  "PISTA-L": {
    id: "PISTA-L",
    letter: "L",
    num: 12,
    token: "L",
    title: "Bote de pintura verde",
    category: "Jardinería / Exteriores",
    cardImage: "src/assets/images/objetos/card-obj-16.png",
    backBase: "card-back-base-1.png",
    desc: "La pintura se ha derramado. Parece que el que estaba en el jardín estaba pintando y ha tenido un accidente.",
    isPrivate: false,
    tablePickup: true
  },
  "PISTA-M": {
    id: "PISTA-M",
    letter: "M",
    num: 13,
    token: "M",
    title: "Llave maestra",
    category: "Cerrajería / Acceso",
    cardImage: "src/assets/images/objetos/card-obj-7.png",
    backBase: "card-back-base-2.png",
    desc: "Una llave maestra que abre todas las puertas de la finca.",
    isPrivate: false,
    tablePickup: true
  },
  "PISTA-N": {
    id: "PISTA-N",
    letter: "N",
    num: 14,
    token: "N",
    title: "Nota manuscrita",
    category: "Nota / Mensaje",
    cardImage: "src/assets/images/objetos/card-obj-8.png",
    backBase: "card-back-base-3.png",
    desc: "Una pequeña nota tipo post-it encontrada en la cocina con una anotación apresurada.",
    isPrivate: false,
    tablePickup: true,
    specialBackImage: "src/assets/images/tarjetas/card-esp-frame-3.png",
    specialViewChars: [5, 6, 7],
    linkedClues: ["PISTA-O"]
  },
  "PISTA-O": {
    id: "PISTA-O",
    letter: "O",
    num: 15,
    token: "O",
    title: "Móvil desechable",
    category: "Comunicaciones",
    cardImage: "src/assets/images/objetos/card-obj-5.png",
    backBase: "card-back-base-1.png",
    desc: "Móvil desechable. Estaba escondido en el cajón de los cubiertos.",
    isPrivate: false,
    tablePickup: true
  },
  "PISTA-P": {
    id: "PISTA-P",
    letter: "P",
    num: 16,
    token: "P",
    title: "Teléfono móvil",
    category: "Grabaciones Telefónicas",
    cardImage: "src/assets/images/objetos/card-obj-10.png",
    backBase: "card-back-base-2.png",
    desc: "Teléfono móvil con dos grabaciones de audio guardadas en memoria.",
    hasAudioPlayer: true,
    audioCalls: [
      { id: 1, title: "Llamada 1 (Interceptada)", file: "src/assets/audio/phone-safe-1.mp3" },
      { id: 2, title: "Llamada 2 (Buzón de voz)", file: "src/assets/audio/phone-safe-2.mp3" }
    ],
    isPrivate: false,
    tablePickup: true
  },
  "PISTA-Q": {
    id: "PISTA-Q",
    letter: "Q",
    num: 17,
    token: "Q",
    title: "Caja fuerte",
    category: "Compartimento de Seguridad",
    cardImage: "src/assets/images/objetos/card-obj-9.png",
    backBase: "card-back-base-3.png",
    desc: "Caja fuerte acorazada con combinación digital. Requiere clave de 5 caracteres para desbloquearse.",
    requiresCode: true,
    passcode: "KZ4C5",
    unlockedTitle: "Archivos clasificados",
    unlockedDesc: "Caja fuerte abierta con éxito (código KZ4C5). Los archivos clasificados y documentos confidenciales han quedado al descubierto.",
    isPrivate: false,
    tablePickup: true
  },
  "PISTA-R": {
    id: "PISTA-R",
    letter: "R",
    num: 18,
    token: "R",
    title: "Ticket de compra",
    category: "Comprobante",
    cardImage: "src/assets/images/objetos/card-obj-14.png",
    backBase: "card-back-base-1.png",
    desc: "Un ticket de compra reciente de un establecimiento local con detalles sospechosos.",
    isPrivate: false,
    tablePickup: true
  },
  "PISTA-S": {
    id: "PISTA-S",
    letter: "S",
    num: 19,
    token: "S",
    title: "Cartuchos",
    category: "Balística",
    cardImage: "src/assets/images/objetos/card-obj-15.png",
    backBase: "card-back-base-2.png",
    desc: "Varios cartuchos percutidos encontrados en la escena. Sin formación balística, no es posible determinar si contenían munición real.",
    isBlankAmmo: true,
    expertChars: [1, 4], // Cazador (1) y Militar (4)
    expertText: "¡SON CARTUCHOS DE FOGUEO! Tu experiencia en armas te permite verificar que estos casquillos no contenían proyectiles reales. Los disparos fueron simulados; no hubo proyectil letal.",
    isPrivate: false,
    tablePickup: false
  },
  "PISTA-T": {
    id: "PISTA-T",
    letter: "T",
    num: 20,
    token: "T",
    title: "Ordenador",
    category: "Sistema de Videovigilancia",
    cardImage: "src/assets/images/objetos/card-scanner-camera.png",
    backBase: "card-back-base-3.png",
    desc: "Ordenador de videovigilancia de la finca. La mayoría de vídeos de las cámaras se han perdido por un fallo del sistema.",
    requiresCode: true,
    passcode: "1628",
    unlockedTitle: "Ordenador (Acceso concedido)",
    unlockedDesc: "Acceso al sistema concedido. Las cámaras exteriores confirman fallos técnicos y grabaciones fragmentadas.",
    isPrivate: false,
    tablePickup: true
  }
};

/**
 * Resuelve cualquier entrada del usuario (letra, nombre, token o id) a su identificador canónico
 */
export function resolveClueId(rawInput) {
  if (!rawInput) return null;
  const input = String(rawInput).trim().toLowerCase();

  // 1. Alias semánticos directos por palabras clave
  const nameAliases = {
    "papeles": "PISTA-A",
    "papel": "PISTA-A",
    "documentos": "PISTA-A",
    "abogado": "PISTA-A",

    "llave pequeña": "PISTA-B",
    "llave pekeña": "PISTA-B",
    "llave pequenya": "PISTA-B",
    "llave sofa": "PISTA-B",

    "boli": "PISTA-C",
    "boligrafo": "PISTA-C",
    "bolígrafo": "PISTA-C",
    "pluma": "PISTA-C",
    "gm": "PISTA-C",

    "destornillador": "PISTA-D",
    "punta plana": "PISTA-D",

    "llave grande": "PISTA-E",
    "llave puerta": "PISTA-E",

    "copa": "PISTA-F",
    "copa vino": "PISTA-F",
    "vaso": "PISTA-F",

    "pasaporte": "PISTA-G",
    "passport": "PISTA-G",
    "pass": "PISTA-G",
    "diario": "PISTA-G",
    "hoja de diario": "PISTA-G",
    "hoja diario": "PISTA-G",
    "diario personal": "PISTA-G",

    "periodico": "PISTA-H",
    "periódico": "PISTA-H",
    "warbes": "PISTA-H",
    "forbes": "PISTA-H",
    "revista": "PISTA-H",

    "ticket": "PISTA-I",
    "ticket roto": "PISTA-I",
    "recibo": "PISTA-I",
    "billete": "PISTA-I",

    "extracto": "PISTA-J",
    "extracto bancario": "PISTA-J",
    "extractos": "PISTA-J",
    "banco": "PISTA-J",
    "cuenta": "PISTA-J",
    "cuenta bancaria": "PISTA-J",
    "transferencia": "PISTA-J",

    "pintura": "PISTA-L",
    "bote de pintura": "PISTA-L",
    "bote pintura": "PISTA-L",
    "pintura verde": "PISTA-L",
    "bote verde": "PISTA-L",
    "jardin": "PISTA-L",
    "jardín": "PISTA-L",

    "llave maestra": "PISTA-M",
    "maestra": "PISTA-M",
    "tarjeta": "PISTA-M",
    "tarjeta de personal": "PISTA-M",
    "tarjeta personal": "PISTA-M",

    "nota": "PISTA-N",
    "postit": "PISTA-N",
    "post-it": "PISTA-N",
    "nota post-it": "PISTA-N",
    "nota adhesiva": "PISTA-N",
    "nota manuscrita": "PISTA-N",

    "movil": "PISTA-O",
    "móvil": "PISTA-O",
    "movil desechable": "PISTA-O",
    "móvil desechable": "PISTA-O",
    "cubiertos": "PISTA-O",

    "telefono": "PISTA-P",
    "teléfono": "PISTA-P",
    "llamada": "PISTA-P",
    "llamadas": "PISTA-P",
    "audios": "PISTA-P",
    "audio": "PISTA-P",

    "caja fuerte": "PISTA-Q",
    "cajafuerte": "PISTA-Q",
    "caja": "PISTA-Q",
    "archivos clasificados": "PISTA-Q",
    "documentos clasificados": "PISTA-Q",
    "kz4c5": "PISTA-Q",

    "ticket compra": "PISTA-R",
    "ticket de compra": "PISTA-R",
    "compra": "PISTA-R",

    "cartuchos": "PISTA-S",
    "cartucho": "PISTA-S",
    "fogueo": "PISTA-S",
    "balas": "PISTA-S",

    "ordenador": "PISTA-T",
    "pc": "PISTA-T",
    "camaras": "PISTA-T",
    "cámaras": "PISTA-T",
    "seguridad": "PISTA-T",

    "buzon": "PISTA-K",
    "buzón": "PISTA-K"
  };

  if (nameAliases[input]) {
    return nameAliases[input];
  }

  // Soporte de compatibilidad para tokens alfanuméricos anteriores
  const legacyTokens = {
    "pap7a": "PISTA-A",
    "llav2b": "PISTA-B",
    "bol9c": "PISTA-C",
    "des4d": "PISTA-D",
    "llag5e": "PISTA-E",
    "cop3f": "PISTA-F",
    "pass7g": "PISTA-G",
    "war8h": "PISTA-H",
    "tic1i": "PISTA-I",
    "ext7j": "PISTA-J"
  };
  if (legacyTokens[input]) {
    return legacyTokens[input];
  }

  // 2. Coincidencia directa por letra única (ej: "a", "b", "c", ..., "k")
  for (const [id, clue] of Object.entries(CLUES)) {
    if (clue.letter && clue.letter.toLowerCase() === input) {
      return id;
    }
  }

  // 3. Patrón prefijo (ej: "pista a", "pista k", "sobre b", "letra c", "objeto d")
  const prefixMatch = input.match(/^(?:pista|objeto|sobre|letra)\s*([a-z])$/i);
  if (prefixMatch) {
    const targetLetter = prefixMatch[1].toUpperCase();
    for (const [id, clue] of Object.entries(CLUES)) {
      if (clue.letter === targetLetter) {
        return id;
      }
    }
  }

  // 4. Búsqueda por token del código QR
  for (const [id, clue] of Object.entries(CLUES)) {
    if (clue.token && clue.token.toLowerCase() === input) {
      return id;
    }
  }

  // 5. Búsqueda por ID exacto (ej: PISTA-A, PISTA-B, OBJETO-A)
  const upper = input.toUpperCase();
  if (CLUES[upper]) return upper;
  if (upper.startsWith("OBJETO-")) {
    const letter = upper.replace("OBJETO-", "");
    if (CLUES[`PISTA-${letter}`]) return `PISTA-${letter}`;
  }

  // 6. Coincidencia por número correlativo (1 a 10)
  const numMatch = input.match(/^(\d+)$/);
  if (numMatch) {
    const num = parseInt(numMatch[1], 10);
    for (const [id, clue] of Object.entries(CLUES)) {
      if (clue.num === num) {
        return id;
      }
    }
  }

  return null;
}

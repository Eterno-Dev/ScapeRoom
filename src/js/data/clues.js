/**
 * Registro Oficial de Pistas y Objetos Físicos del Juego
 * CluedoWeb / ScapeRoom — Configuración de 10 Pistas Oficiales (A a J)
 */

export const CLUES = {
  "PISTA-A": {
    id: "PISTA-A",
    letter: "A",
    code: "A-7$9K",
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
    code: "B-4#2P",
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
    code: "C-8%1M",
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
    code: "D-3&5X",
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
    code: "E-9!4R",
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
    code: "F-2?8L",
    num: 6,
    token: "F",
    title: "Copa",
    category: "Cristalería",
    cardImage: "src/assets/images/objetos/card-obj-13.png",
    backBase: "card-back-base-3.png",
    desc: "Es una copa que está encima de la mesa. No parece muy importante ni muestra detalles sospechosos a simple vista; parece una pista sin mayor relevancia.",
    isPrivate: false,
    tablePickup: true
  },
  "PISTA-G": {
    id: "PISTA-G",
    letter: "G",
    code: "G-5*7T",
    num: 7,
    token: "G",
    title: "Pasaporte",
    category: "Identidad",
    cardImage: "src/assets/images/objetos/card-obj-17.png",
    backBase: "card-back-base-1.png",
    desc: "Documento de viaje en un estado extraño. Al examinarlo con atención, hay algo raro y sospechoso en él.",
    isPrivate: false,
    tablePickup: true,
    linkedClues: ["PISTA-G2"]
  },
  "PISTA-G2": {
    id: "PISTA-G2",
    letter: "G",
    code: "G-5*7T",
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
    code: "H-6@3W",
    num: 8,
    token: "H",
    title: "Periódico Warbes",
    category: "Prensa Financiera",
    cardImage: "src/assets/images/objetos/card-obj-periodico.png",
    backBase: "card-back-base-2.png",
    desc: "Es una copia del día de ayer del periódico empresarial famoso WARBES.",
    isPrivate: false,
    tablePickup: true
  },
  "PISTA-I": {
    id: "PISTA-I",
    letter: "I",
    code: "I-1#9Q",
    num: 9,
    token: "I",
    title: "Ticket roto",
    category: "Comprobante",
    cardImage: "src/assets/images/objetos/card-obj-ticket-roto.png",
    backBase: "card-back-base-3.png",
    desc: "Parece un ticket bastante arreglado, propio de la alta sociedad. Da la impresión de que alguien lo ha tirado deliberadamente para deshacerse de las pruebas o eliminar cualquier rastro.",
    isPrivate: false,
    tablePickup: true
  },
  "PISTA-J": {
    id: "PISTA-J",
    letter: "J",
    code: "J-4$8Z",
    num: 10,
    token: "J",
    title: "Documentos archivo",
    category: "Archivo de Documentos",
    cardImage: "src/assets/images/objetos/card-obj-documentos.png",
    backBase: "card-back-base-2.png",
    desc: "Conjunto de documentos como transacciones bancarias, extractos bancarios y consultas médicas.",
    isPrivate: false,
    tablePickup: true
  },
  "PISTA-K": {
    id: "PISTA-K",
    letter: "K",
    code: "K-8%2N",
    num: 11,
    token: "K",
    title: "Buzón",
    category: "Correspondencia",
    cardImage: "src/assets/images/objetos/card-obj-buzon.png",
    backBase: "card-back-base-1.png",
    desc: "Buzón exterior cerrado. Contiene correspondencia privada.",
    isPrivate: false,
    tablePickup: true
  },
  "PISTA-L": {
    id: "PISTA-L",
    letter: "L",
    code: "L-7&4V",
    num: 12,
    token: "L",
    title: "Bote de pintura verde",
    category: "Jardinería / Exteriores",
    cardImage: "src/assets/images/objetos/card-obj-16.png",
    backBase: "card-back-base-1.png",
    desc: "La pintura se ha derramado. Parece que el que estaba en el jardín estaba pintando y ha tenido un accidente.",
    witnessChars: [1, 3, 5], // 1: Cazador, 3: Médico, 5: Nieto (Heredero)
    witnessText: "Recuerdas que la persona que estaba pintando fue el/la jardinero/a. Además, lo viste discutir acaloradamente con la víctima en esta misma zona.",
    isPrivate: false,
    tablePickup: true
  },
  "PISTA-M": {
    id: "PISTA-M",
    letter: "M",
    code: "M-3!6D",
    num: 13,
    token: "M",
    title: "Llave maestra",
    category: "Cerrajería / Acceso",
    cardImage: "src/assets/images/objetos/card-obj-7.png",
    backBase: "card-back-base-2.png",
    desc: "Es un poco sospechoso que esté por aquí tirada. Da acceso al resto de puertas del lugar.",
    isPrivate: false,
    tablePickup: true
  },
  "PISTA-N": {
    id: "PISTA-N",
    letter: "N",
    code: "N-9*1B",
    num: 14,
    token: "N",
    title: "Notas",
    category: "Nota / Mensaje",
    cardImage: "src/assets/images/objetos/card-obj-12.png",
    backBase: "card-back-base-3.png",
    desc: "Una pequeña nota tipo post-it encontrada en la cocina con una anotación apresurada.",
    isPrivate: false,
    tablePickup: true,
    specialBackImage: "src/assets/images/tarjetas/card-morse.png",
    specialViewChars: [1, 4] // 1: Cazador, 4: Militar
  },
  "PISTA-O": {
    id: "PISTA-O",
    letter: "O",
    code: "O-2?5H",
    num: 15,
    token: "O",
    title: "Móvil desechable",
    category: "Comunicaciones",
    cardImage: "src/assets/images/objetos/card-obj-5.png",
    backBase: "card-back-base-1.png",
    desc: "Móvil desechable bloqueado. Estaba escondido en el cajón de los cubiertos de la cocina. Requiere contraseña para desbloquearlo.",
    requiresCode: true,
    passcode: "3JF6",
    unlockedTitle: "Móvil desbloqueado",
    unlockedDesc: "Móvil desechable desbloqueado. Contiene un único número en la agenda y mensajes sobre el corte de luz previo al crimen.",
    isPrivate: false,
    tablePickup: true
  },
  "PISTA-P": {
    id: "PISTA-P",
    letter: "P",
    code: "P-5#7J",
    num: 16,
    token: "P",
    title: "Teléfono móvil",
    category: "Grabaciones Telefónicas",
    cardImage: "src/assets/images/objetos/card-obj-10.png",
    backBase: "card-back-base-2.png",
    desc: "Teléfono móvil con dos grabaciones de audio guardadas en memoria.",
    hasAudioPlayer: true,
    audioCalls: [
      { id: 1, title: "Llamada 1 (Interceptada)", file: "src/assets/audio/phone_safe_1.mp3" },
      { id: 2, title: "Llamada 2 (Buzón de voz)", file: "src/assets/audio/phone_safe_2.mp3" }
    ],
    isPrivate: false,
    tablePickup: true
  },
  "PISTA-Q": {
    id: "PISTA-Q",
    letter: "Q",
    code: "Q-8$3C",
    num: 17,
    token: "Q",
    title: "Caja fuerte",
    category: "Compartimento de Seguridad",
    cardImage: "src/assets/images/objetos/card-obj-9.png",
    backBase: "card-back-base-3.png",
    desc: "Caja fuerte acorazada de alta seguridad. El panel electrónico requiere una clave de acceso de 5 caracteres.",
    requiresCode: true,
    passcode: "KZ4C5",
    unlockedTitle: "Archivos clasificados",
    unlockedDesc: "Caja fuerte abierta. Los archivos clasificados y documentos confidenciales han quedado al descubierto.",
    isPrivate: false,
    tablePickup: true
  },
  "PISTA-R": {
    id: "PISTA-R",
    letter: "R",
    code: "R-1%9F",
    num: 18,
    token: "R",
    title: "Ticket de compra",
    category: "Comprobante",
    cardImage: "src/assets/images/objetos/card-obj-ticket-compra.png",
    backBase: "card-back-base-1.png",
    desc: "Es un ticket de una tienda de armas en Dakota.",
    isPrivate: false,
    tablePickup: true
  },
  "PISTA-S": {
    id: "PISTA-S",
    letter: "S",
    code: "S-6&2Y",
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
    code: "T-4!8S",
    num: 20,
    token: "T",
    title: "Ordenador",
    category: "Sistema de Videovigilancia",
    cardImage: "src/assets/images/objetos/card-obj-ordenador.png",
    backBase: "card-back-base-3.png",
    desc: "Ordenador de videovigilancia de la finca. El sistema está bloqueado y requiere contraseña de administrador para consultar las cámaras.",
    requiresCode: true,
    passcode: "8008135",
    unlockedTitle: "Ordenador de seguridad",
    unlockedDesc: "Terminal de seguridad desbloqueado. Las grabaciones de las cámaras de seguridad están corruptas, pero se ha podido recuperar un archivo de imagen y varios fotogramas clave de los vídeos en diferentes horas.",
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

    "documentos archivo": "PISTA-J",
    "documentos y el archivo": "PISTA-J",
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

    "notas": "PISTA-N",
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
    "3jf6": "PISTA-O",

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
    "8008135": "PISTA-T",

    "buzon": "PISTA-K",
    "buzón": "PISTA-K"
  };

  if (nameAliases[input]) {
    return nameAliases[input];
  }

  // 0. Coincidencia directa por contraseña / passcode
  for (const [id, clue] of Object.entries(CLUES)) {
    if (clue.passcode && clue.passcode.toLowerCase() === input) {
      return id;
    }
  }

  // 0.1 Coincidencia por código de impresión exacto (ej: "A-7$9K", "B-4#2P")
  for (const [id, clue] of Object.entries(CLUES)) {
    if (clue.code && clue.code.toLowerCase() === input) {
      return id;
    }
  }

  // 0.1 Prefijo con guión de código (ej: "A-...", "B-...")
  const codePrefixMatch = input.match(/^([a-z])[-_]/i);
  if (codePrefixMatch) {
    const targetLetter = codePrefixMatch[1].toUpperCase();
    for (const [id, clue] of Object.entries(CLUES)) {
      if (clue.letter === targetLetter) {
        return id;
      }
    }
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

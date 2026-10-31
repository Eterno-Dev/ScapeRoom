/**
 * Registro Oficial de Pistas y Objetos Físicos del Juego
 * CluedoWeb / ScapeRoom — Configuración de 10 Pistas Oficiales (A a K)
 */

export const CLUES = {
  "PISTA-A": {
    id: "PISTA-A",
    letter: "A",
    num: 1,
    token: "pap7a",
    title: "Papeles",
    category: "Expediente Jurídico",
    cardImage: "src/assets/images/objetos/card-obj-11.png",
    backBase: "card-back-base-1.png",
    desc: "Documentos de investigación aportados por el abogado.",
    isPrivate: false,
    tablePickup: false
  },
  "PISTA-B": {
    id: "PISTA-B",
    letter: "B",
    num: 2,
    token: "llav2b",
    title: "Llave pequeña",
    category: "Cerradura / Objeto Pequeño",
    cardImage: "src/assets/images/objetos/card-obj-3.png",
    backBase: "card-back-base-2.png",
    desc: "Llave pequeña. Parece para abrir algo que no es una puerta, parece de algo pequeño. Estaba encima del sofá.",
    isPrivate: false,
    tablePickup: false
  },
  "PISTA-C": {
    id: "PISTA-C",
    letter: "C",
    num: 3,
    token: "bol9c",
    title: "Boli",
    category: "Objeto Militar",
    cardImage: "src/assets/images/objetos/card-obj-6.png",
    backBase: "card-back-base-3.png",
    desc: "Es un boli que parece bastante caro. Tiene un escudo militar grabado y las siglas GM (General Militar).",
    isPrivate: false,
    tablePickup: false
  },
  "PISTA-D": {
    id: "PISTA-D",
    letter: "D",
    num: 4,
    token: "des4d",
    title: "Destornillador",
    category: "Herramienta",
    cardImage: "src/assets/images/objetos/card-obj-4.png",
    backBase: "card-back-base-1.png",
    desc: "Es de punta plana y parece que estaba escondido casi a propósito. El lugar donde se encontraba era muy sospechoso; no es normal que termine ahí.",
    isPrivate: false,
    tablePickup: false
  },
  "PISTA-E": {
    id: "PISTA-E",
    letter: "E",
    num: 5,
    token: "llag5e",
    title: "Llave grande",
    category: "Acceso Principal",
    cardImage: "src/assets/images/objetos/card-obj-2.png",
    backBase: "card-back-base-2.png",
    desc: "Llave grande. Parece que abre una puerta grande o una cancela principal.",
    isPrivate: false,
    tablePickup: false
  },
  "PISTA-F": {
    id: "PISTA-F",
    letter: "F",
    num: 6,
    token: "cop3f",
    title: "Copa",
    category: "Cristalería",
    cardImage: "src/assets/images/objetos/card-obj-13.png",
    backBase: "card-back-base-3.png",
    desc: "Copa de cristal tallado con restos secos en la base y un poso blanquecino sospechoso.",
    isPrivate: false,
    tablePickup: false
  },
  "PISTA-G": {
    id: "PISTA-G",
    letter: "G",
    num: 7,
    token: "pass7g",
    title: "Pasaporte",
    category: "Identidad",
    cardImage: "src/assets/images/objetos/card-obj-17.png",
    backBase: "card-back-base-1.png",
    desc: "Documento de viaje e identificación aparentemente oficial expedido bajo los sellos de los Estados Unidos.",
    detailNormal: "A simple vista parece un pasaporte ordinario y legítimo en regla para viajes internacionales y residencia. No obstante, solo un profesional instruido en control fronterizo o leyes consulares sabría comprobar la validez técnica de sus marcas y sellos.",
    detailExpert: "¡DOCUMENTO FALSIFICADO! Al ser una persona entendida en el tema, detectas de inmediato que este pasaporte ha sido FALSIFICADO: la tipografía del código MRZ está alterada, el sello de Alaska no corresponde a la demarcación federal y los datos biográficos han sido manipulados para ocultar una orden de captura.",
    isPassport: true,
    isPrivate: false,
    tablePickup: false
  },
  "PISTA-H": {
    id: "PISTA-H",
    letter: "H",
    num: 8,
    token: "war8h",
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
    token: "tic1i",
    title: "Ticket roto",
    category: "Comprobante",
    cardImage: "src/assets/images/objetos/card-obj-14.png",
    backBase: "card-back-base-3.png",
    desc: "Un ticket roto. Parece que alguien lo ha tirado porque no sabía qué hacer con él.",
    isPrivate: false,
    tablePickup: true
  },
  "PISTA-K": {
    id: "PISTA-K",
    letter: "K",
    num: 10,
    token: "buz6k",
    title: "Buzón",
    category: "Correspondencia",
    cardImage: "src/assets/images/objetos/card-obj-12.png",
    backBase: "card-back-base-1.png",
    desc: "Buzón exterior cerrado. Parece que requiere una llave pequeña para poder abrirse.",
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

    "periodico": "PISTA-H",
    "periódico": "PISTA-H",
    "warbes": "PISTA-H",
    "forbes": "PISTA-H",
    "revista": "PISTA-H",

    "ticket": "PISTA-I",
    "ticket roto": "PISTA-I",
    "recibo": "PISTA-I",
    "billete": "PISTA-I",

    "buzon": "PISTA-K",
    "buzón": "PISTA-K"
  };

  if (nameAliases[input]) {
    return nameAliases[input];
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

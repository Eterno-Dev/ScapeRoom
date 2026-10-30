/**
 * Registro de Objetos y Pistas Físicas (Escaneables por QR)
 * EternoDev Web Standards - 15 Objetos Oficiales (Objeto 2 al Objeto 16)
 */

export const CLUES = {
  "OBJETO-02": {
    id: "OBJETO-02",
    num: 2,
    letter: "B",
    token: "k9x7m2",
    title: "Llave grande",
    category: "Acceso / Puerta",
    cardImage: "src/assets/images/objetos/card-obj-2.png",
    backBase: "card-back-base-1.png",
    desc: "Llave antigua de hierro forjado de gran tamaño. Aparentemente sirve para abrir una pesada puerta de metal o una cancela exterior.",
    detail: "Hallada cerca del zaguán. Los bordes tienen raspaduras recientes, lo que indica que alguien la usó poco antes de la medianoche."
  },
  "OBJETO-03": {
    id: "OBJETO-03",
    num: 3,
    letter: "C",
    token: "w3b8r5",
    title: "Llave pequeña",
    category: "Cerradura Secreta",
    cardImage: "src/assets/images/objetos/card-obj-3.png",
    backBase: "card-back-base-2.png",
    desc: "Pequeña llave dorada finamente grabada. Parece una llave de un joyero o de un compartimento íntimo.",
    detail: "Estaba tirada al lado de la caja de herramientas cerca del dormitorio principal, oculta bajo una alfombra."
  },
  "OBJETO-04": {
    id: "OBJETO-04",
    num: 4,
    letter: "D",
    token: "p7q2t4",
    title: "Destornillador",
    category: "Herramienta",
    cardImage: "src/assets/images/objetos/card-obj-4.png",
    backBase: "card-back-base-3.png",
    desc: "Instrumento para desatornillar con mango de madera desgastado. Se trata de un modelo de punta plana con signos de forcejeo.",
    detail: "La punta metálica encaja con las muescas encontradas en el marco del cuadro del salón principal."
  },
  "OBJETO-05": {
    id: "OBJETO-05",
    num: 5,
    letter: "E",
    token: "m5v8y1",
    title: "Collar",
    category: "Joya Valiosa",
    cardImage: "src/assets/images/objetos/card-obj-5.png",
    backBase: "card-back-base-1.png",
    desc: "Collar de plata antigua con piedras oscuras engastadas. Una joya elegante perteneciente a una de las damas de la mansión.",
    detail: "El cierre trasero está quebrado violentamente, sugiriendo un forcejeo durante la velada."
  },
  "OBJETO-06": {
    id: "OBJETO-06",
    num: 6,
    letter: "F",
    token: "j4h6s9",
    title: "Boli",
    category: "Escritura",
    cardImage: "src/assets/images/objetos/card-obj-6.png",
    backBase: "card-back-base-2.png",
    desc: "Bolígrafo de latón pesado de recambio negro. Todavía conserva tinta fresca en la punta.",
    detail: "El tono de la tinta coincide milimétricamente con las tachaduras encontradas en el documento notarial."
  },
  "OBJETO-07": {
    id: "OBJETO-07",
    num: 7,
    letter: "G",
    token: "d2n8k3",
    title: "Candelabro",
    category: "Objeto Pesado",
    cardImage: "src/assets/images/objetos/card-obj-7.png",
    backBase: "card-back-base-3.png",
    desc: "Candelabro señorial de bronce con tres brazos y restos de cera endurecida. Presenta una deformación en la base.",
    detail: "La base metálica muestra una leve hendidura con restos biológicos secos."
  },
  "OBJETO-08": {
    id: "OBJETO-08",
    num: 8,
    letter: "H",
    token: "z6f3w8",
    title: "Tijeras",
    category: "Corte",
    cardImage: "src/assets/images/objetos/card-obj-8.png",
    backBase: "card-back-base-1.png",
    desc: "Tijeras de sastre largas y afiladas, de hojas de acero al carbono pulido.",
    detail: "Tienen diminutas fibras de paño atrapadas en el tornillo del eje, del mismo tejido que el traje de la víctima."
  },
  "OBJETO-09": {
    id: "OBJETO-09",
    num: 9,
    letter: "I",
    token: "x8c5g1",
    title: "Medicina",
    category: "Fármaco / Botica",
    cardImage: "src/assets/images/objetos/card-obj-9.png",
    backBase: "card-back-base-2.png",
    desc: "Frasco de vidrio oscuro con restos de gotas medicinales y etiqueta parcialmente arrancada.",
    detail: "El análisis del contenido revela una dosis triple a la prescrita por el médico de cabecera."
  },
  "OBJETO-10": {
    id: "OBJETO-10",
    num: 10,
    letter: "J",
    token: "b4m9v2",
    title: "Caja fuerte",
    category: "Seguridad",
    cardImage: "src/assets/images/objetos/card-obj-10.png",
    backBase: "card-back-base-3.png",
    desc: "Caja fuerte portátil de combinación de dial metálico. El mecanismo se encuentra forzado y entreabierto.",
    detail: "El interior estaba vacío a excepción de una carpeta y cenizas de papeles quemados."
  },
  "OBJETO-11": {
    id: "OBJETO-11",
    num: 11,
    letter: "K",
    token: "q7r3t8",
    title: "Papeles",
    category: "Documentación",
    isPrivate: true,
    cardImage: "src/assets/images/objetos/card-obj-11.png",
    backBase: "card-back-base-1.png",
    desc: "Hojas de papel bancario y balances financieros con anotaciones manuscritas apresuradas en los márgenes.",
    detail: "Revelan una deuda monumental y amenazas de desahucio si la herencia no se liquidaba de inmediato."
  },
  "OBJETO-12": {
    id: "OBJETO-12",
    num: 12,
    letter: "L",
    token: "h2j6k9",
    title: "Nota",
    category: "Mensaje Secreto",
    isPrivate: true,
    cardImage: "src/assets/images/objetos/card-obj-12.png",
    backBase: "card-back-base-2.png",
    desc: "Trozo de papel doblado en cuatro partes con letra temblorosa: 'Sé lo que hiciste en el bosque. Esta noche termina todo'.",
    detail: "El pliegue aún huele a tabaco de pipa holandés."
  },
  "OBJETO-13": {
    id: "OBJETO-13",
    num: 13,
    letter: "M",
    token: "l5n8p1",
    title: "Copa",
    category: "Cristalería",
    cardImage: "src/assets/images/objetos/card-obj-13.png",
    backBase: "card-back-base-3.png",
    desc: "Copa de cristal tallado con restos secos de vino tinto en el fondo y un sedimento blanquecino sospechoso.",
    detail: "Se encontraba abandonada sobre una mesilla auxiliar junto a la chimenea apagada."
  },
  "OBJETO-14": {
    id: "OBJETO-14",
    num: 14,
    letter: "N",
    token: "v9w3x7",
    title: "Carpeta",
    category: "Expediente",
    isPrivate: true,
    cardImage: "src/assets/images/objetos/card-obj-14.png",
    backBase: "card-back-base-1.png",
    desc: "Carpeta de cuero negro marcada con las iniciales de la familia y sellos lacrados rotos.",
    detail: "Contenía la última versión sin firmar del testamento y una cláusula de exclusión hereditaria."
  },
  "OBJETO-15": {
    id: "OBJETO-15",
    num: 15,
    letter: "O",
    token: "c6d1f4",
    title: "Cartuchos",
    category: "Munición",
    cardImage: "src/assets/images/objetos/card-obj-15.png",
    backBase: "card-back-base-2.png",
    desc: "Vainas de cartuchos de escopeta del calibre 12 ya percutidos, guardados dentro de una bolsa de fieltro.",
    detail: "El fulminante detonado indica que fueron disparados la misma noche en los terrenos traseros."
  },
  "OBJETO-16": {
    id: "OBJETO-16",
    num: 16,
    letter: "P",
    token: "g8s4z2",
    title: "Pluma",
    category: "Reliquia",
    cardImage: "src/assets/images/objetos/card-obj-16.png",
    backBase: "card-back-base-3.png",
    desc: "Pluma estilográfica con plumín de oro de 14 quilates y cuerpo de resina negra con un monograma grabado.",
    detail: "Faltaba en el estuche del despacho principal y fue encontrada entre las sombras del pasillo exterior."
  },
  "OBJETO-17": {
    id: "OBJETO-17",
    num: 17,
    letter: "Q",
    token: "pass7k",
    title: "Pasaporte",
    category: "Identidad",
    isPassport: true,
    cardImage: "src/assets/images/objetos/card-obj-17.png",
    backBase: "card-back-base-1.png",
    desc: "Documento de viaje e identificación aparentemente oficial expedido bajo los sellos de los Estados Unidos.",
    detailNormal: "A simple vista parece un pasaporte ordinario y legítimo en regla para viajes internacionales y residencia. No obstante, solo un profesional instruido en control fronterizo o leyes consulares sabría comprobar la validez técnica de sus marcas y sellos.",
    detailExpert: "¡DOCUMENTO FALSIFICADO! Al ser una persona entendida en el tema, detectas de inmediato que este pasaporte ha sido FALSIFICADO: la tipografía del código MRZ está alterada, el sello de Alaska no corresponde a la demarcación federal y los datos biográficos han sido manipulados para ocultar una orden de captura."
  }
};

/**
 * Resuelve una entrada (token único, ID completo, letra indicadora, o número de objeto/QR) al ID canónico (ej: OBJETO-02)
 */
export function resolveClueId(rawInput) {
  if (!rawInput) return null;
  const input = String(rawInput).trim().toLowerCase();

  // Alias directos para el pasaporte
  if (input === "pasaporte" || input === "passport" || input === "pass" || input === "pass7k") {
    return "OBJETO-17";
  }

  // 1. Buscar coincidencia por letra única (ej: "b", "c", "k") o frase (ej: "pista b", "sobre b")
  for (const [id, clue] of Object.entries(CLUES)) {
    if (clue.letter && clue.letter.toLowerCase() === input) {
      return id;
    }
  }
  const letterPrefixMatch = input.match(/^(?:pista|objeto|sobre|letra)\s*([a-z])$/i);
  if (letterPrefixMatch) {
    const targetLetter = letterPrefixMatch[1].toUpperCase();
    for (const [id, clue] of Object.entries(CLUES)) {
      if (clue.letter === targetLetter) {
        return id;
      }
    }
  }

  // 2. Buscar coincidencia exacta por token secreto (del QR)
  for (const [id, clue] of Object.entries(CLUES)) {
    if (clue.token && clue.token.toLowerCase() === input) {
      return id;
    }
  }

  // 3. Buscar por ID estándar (ej: OBJETO-02 u OBJETO-2)
  const upper = input.toUpperCase();
  if (CLUES[upper]) return upper;

  // 4. Buscar por coincidencia con número de objeto o QR (ej: "2", "qr2", "objeto2", "pista2")
  const numMatch = input.match(/(\d+)/);
  if (numMatch) {
    const num = parseInt(numMatch[1], 10);
    const padded = `OBJETO-${String(num).padStart(2, "0")}`;
    if (CLUES[padded]) return padded;
  }

  return null;
}

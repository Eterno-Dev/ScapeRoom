/**
 * Registro de Pistas Físicas y Hallazgos
 * EternoDev Web Standards - Estricto minimalismo
 */

export const CLUES = {
  "PISTA-01": {
    id: "PISTA-01",
    num: 1,
    token: "k9x7m2",
    title: "Cuchillo ensangrentado",
    category: "Arma",
    tagColor: "#dc2626",
    desc: "Hoja de acero inoxidable con restos de sangre seca. Hallado oculto bajo las tablas de la cocina.",
    detail: "El filo coincide con la herida punzante en el tórax de la víctima."
  },
  "PISTA-02": {
    id: "PISTA-02",
    num: 2,
    token: "w3b8r5",
    title: "Arañazo en la cerradura",
    category: "Escena",
    tagColor: "#d97706",
    desc: "Muescas metálicas profundas en el cerrojo del despacho principal.",
    detail: "Indican que la puerta fue forzada desde el pasillo minutos antes del crimen."
  },
  "PISTA-03": {
    id: "PISTA-03",
    num: 3,
    token: "p7q2t4",
    title: "Frasco de belladona",
    category: "Veneno",
    tagColor: "#7c3aed",
    desc: "Frasco de boticario vacío con residuo alcaloide letal de extracto botánico.",
    detail: "Oculto entre los volúmenes de botánica en la estantería de la biblioteca."
  },
  "PISTA-04": {
    id: "PISTA-04",
    num: 4,
    token: "m5v8y1",
    title: "Carta rasgada",
    category: "Documento",
    tagColor: "#2563eb",
    desc: "Fragmento de carta exigiendo 50.000 pesetas a cambio de silencio sobre la herencia.",
    detail: "La firma inferior fue arrancada con violencia para no revelar al remitente."
  },
  "PISTA-05": {
    id: "PISTA-05",
    num: 5,
    token: "j4h6s9",
    title: "Reloj de bolsillo roto",
    category: "Objeto",
    tagColor: "#059669",
    desc: "Reloj de plata con la esfera estrellada. Manecillas detenidas a las 23:42.",
    detail: "Fija con precisión la hora en la que se produjo el forcejeo mortal."
  },
  "PISTA-06": {
    id: "PISTA-06",
    num: 6,
    token: "d2n8k3",
    title: "Huellas de barro",
    category: "Rastro",
    tagColor: "#ea580c",
    desc: "Pisadas de calzado militar del número 43 procedentes del jardín hacia el balcón.",
    detail: "El agresor huyó cruzando el invernadero durante la tormenta nocturna."
  },
  "PISTA-07": {
    id: "PISTA-07",
    num: 7,
    token: "z6f3w8",
    title: "Testamento tachado",
    category: "Documento",
    tagColor: "#0891b2",
    desc: "Borrador notarial con la cláusula del primogénito anulada con tachaduras de tinta fresca.",
    detail: "El fallecido planeaba cambiar a su heredero universal esa misma noche."
  },
  "PISTA-08": {
    id: "PISTA-08",
    num: 8,
    token: "x8c5g1",
    title: "Copa de vino rota",
    category: "Veneno",
    tagColor: "#b91c1c",
    desc: "Cáliz de cristal de Bohemia con restos de vino tinto y posos blanquecinos.",
    detail: "El análisis químico preliminar confirma presencia de sedante concentrado."
  }
};

/**
 * Resuelve una entrada (token único, ID completo o número) al ID de pista canónico
 */
export function resolveClueId(rawInput) {
  if (!rawInput) return null;
  const input = String(rawInput).trim().toLowerCase();

  // 1. Buscar coincidencia exacta por token secreto
  for (const [id, clue] of Object.entries(CLUES)) {
    if (clue.token && clue.token.toLowerCase() === input) {
      return id;
    }
  }

  // 2. Buscar por ID estándar (ej: PISTA-01)
  const upper = input.toUpperCase();
  if (CLUES[upper]) return upper;

  // 3. Buscar por coincidencia con número de pista
  for (const [id, clue] of Object.entries(CLUES)) {
    if (String(clue.num) === input || `pista-${clue.num}` === input) {
      return id;
    }
  }

  return null;
}

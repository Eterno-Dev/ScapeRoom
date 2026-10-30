/**
 * Catálogo Oficial de Personajes — El Asesinato Embrujado
 * EternoDev Web Standards - 8 Personajes Oficiales (Aventura para 8 Jugadores)
 * Incluye al Administrador Especial de la Campaña (Javier Escudero / Carmen Ruiz) con selección en azul
 */

export const CHARACTERS = [
  {
    id: 1,
    tag: "Persona 1",
    backBase: "card-back-base-1.png",
    male: {
      name: "El Cazador",
      role: "Cazador",
      bio: "Conoce todos los senderos y secretos del bosque de la finca.",
      secret: "Posesión y tráfico ilícito de aves y animales protegidos ocultos disecados en la finca.",
      cardImage: "src/assets/images/personajes_masculinos/card-m-cazador.png"
    },
    female: {
      name: "La Cazadora",
      role: "Cazadora",
      bio: "Conoce todos los senderos y secretos del bosque de la finca.",
      secret: "Posesión y tráfico ilícito de aves y animales protegidos ocultos disecados en la finca.",
      cardImage: "src/assets/images/personajes_femeninos/card-f-cazadora.png"
    }
  },
  {
    id: 2,
    tag: "Persona 2",
    backBase: "card-back-base-2.png",
    male: {
      name: "Leonardo Vargas",
      role: "Músico",
      bio: "Amenizaba la velada exclusiva antes de que se apagaran las luces.",
      secret: "Sobornos continuados a medios de comunicación para silenciar graves escándalos de abusos sexuales.",
      cardImage: "src/assets/images/personajes_masculinos/card-m-leonardo.png"
    },
    female: {
      name: "Valentina Santos",
      role: "Música",
      bio: "Amenizaba la velada exclusiva antes de que se apagaran las luces.",
      secret: "Sobornos continuados a medios de comunicación para silenciar graves escándalos de abusos sexuales.",
      cardImage: "src/assets/images/personajes_femeninos/card-f-valentina.png"
    }
  },
  {
    id: 3,
    tag: "Persona 3",
    backBase: "card-back-base-3.png",
    male: {
      name: "Dr. Alfonso Rivas",
      role: "Médico",
      bio: "Administraba la medicación diaria y confidencial del difunto.",
      secret: "Sustracción sistemática de joyas y pertenencias de gran valor a pacientes durante las consultas.",
      cardImage: "src/assets/images/personajes_masculinos/card-m-alfonso.png"
    },
    female: {
      name: "Dra. Isabel Ortega",
      role: "Médica",
      bio: "Administraba la medicación diaria y confidencial del difunto.",
      secret: "Sustracción sistemática de joyas y pertenencias de gran valor a pacientes durante las consultas.",
      cardImage: "src/assets/images/personajes_femeninos/card-f-isabel.png"
    }
  },
  {
    id: 4,
    tag: "Persona 4",
    backBase: "card-back-base-1.png",
    male: {
      name: "General Santamaría",
      role: "Militar",
      bio: "General y viejo amigo de juventud de la víctima.",
      secret: "Ascenso en la jerarquía militar financiado mediante extorsión continuada y comisiones del tráfico de armas.",
      cardImage: "src/assets/images/personajes_masculinos/card-m-santamaria.png"
    },
    female: {
      name: "General Araujo",
      role: "Militar",
      bio: "General y vieja amiga de juventud de la víctima.",
      secret: "Ascenso en la jerarquía militar financiado mediante extorsión continuada y comisiones del tráfico de armas.",
      cardImage: "src/assets/images/personajes_femeninos/card-f-araujo.png"
    }
  },
  {
    id: 5,
    tag: "Persona 5",
    backBase: "card-back-base-2.png",
    male: {
      name: "Elías Moreno",
      role: "Heredero",
      bio: "Nieto del difunto y aspirante directo a la fortuna familiar.",
      secret: "Vínculos directos con redes de narcotráfico y deudas masivas por apuestas clandestinas ilegales.",
      cardImage: "src/assets/images/personajes_masculinos/card-m-elias.png"
    },
    female: {
      name: "Sofía Villalba",
      role: "Heredera",
      bio: "Nieta del difunto y aspirante directa a la fortuna familiar.",
      secret: "Vínculos directos con redes de narcotráfico y deudas masivas por apuestas clandestinas ilegales.",
      cardImage: "src/assets/images/personajes_femeninos/card-f-sofia.png"
    }
  },
  {
    id: 6,
    tag: "Persona 6",
    backBase: "card-back-base-3.png",
    male: {
      name: "Hugo Bermejo",
      role: "Jardinero",
      bio: "Cuida los terrenos y sabe quién usó los accesos exteriores.",
      secret: "Estancia en el país bajo una identidad falsa para eludir una orden judicial de captura y expulsión.",
      cardImage: "src/assets/images/personajes_masculinos/card-m-hugo.png"
    },
    female: {
      name: "Lucía Herrera",
      role: "Jardinera",
      bio: "Cuida los terrenos y sabe quién usó los accesos exteriores.",
      secret: "Estancia en el país bajo una identidad falsa para eludir una orden judicial de captura y expulsión.",
      cardImage: "src/assets/images/personajes_femeninos/card-f-lucia.png"
    }
  },
  {
    id: 7,
    tag: "Persona 7",
    backBase: "card-back-base-1.png",
    male: {
      name: "Víctor Dávila",
      role: "Heredero",
      bio: "Era hermano del fallecido en disputa por el testamento.",
      secret: "Quiebra fraudulenta y deudas millonarias impagables tras el colapso financiero de su última empresa.",
      cardImage: "src/assets/images/personajes_masculinos/card-m-victor.png"
    },
    female: {
      name: "Elena Torres",
      role: "Heredera",
      bio: "Era hermana de la víctima en disputa por el testamento.",
      secret: "Quiebra fraudulenta y deudas millonarias impagables tras el colapso financiero de su última empresa.",
      cardImage: "src/assets/images/personajes_femeninos/card-f-elena.png"
    }
  },
  {
    id: 8,
    tag: "Persona 8",
    backBase: "card-back-base-2.png",
    isAdmin: true,
    male: {
      name: "Javier Escudero",
      role: "Abogado",
      bio: "Abogado albacea de la familia. Custodia los documentos legales y secretos de la finca.",
      cardImage: "src/assets/images/personajes_masculinos/card-m-javier.png"
    },
    female: {
      name: "Carmen Ruiz",
      role: "Abogada",
      bio: "Abogada albacea de la familia. Custodia los documentos legales y secretos de la finca.",
      cardImage: "src/assets/images/personajes_femeninos/card-f-carmen.png"
    }
  }
];

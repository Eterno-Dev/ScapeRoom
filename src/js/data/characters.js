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
      cardImage: "src/assets/images/personajes_masculinos/card-m-cazador.png"
    },
    female: {
      name: "La Cazadora",
      role: "Cazadora",
      bio: "Conoce todos los senderos y secretos del bosque de la finca.",
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
      cardImage: "src/assets/images/personajes_masculinos/card-m-leonardo.png"
    },
    female: {
      name: "Valentina Santos",
      role: "Música",
      bio: "Amenizaba la velada exclusiva antes de que se apagaran las luces.",
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
      cardImage: "src/assets/images/personajes_masculinos/card-m-alfonso.png"
    },
    female: {
      name: "Dra. Isabel Ortega",
      role: "Médica",
      bio: "Administraba la medicación diaria y confidencial del difunto.",
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
      cardImage: "src/assets/images/personajes_masculinos/card-m-santamaria.png"
    },
    female: {
      name: "General Araujo",
      role: "Militar",
      bio: "General y vieja amiga de juventud de la víctima.",
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
      cardImage: "src/assets/images/personajes_masculinos/card-m-elias.png"
    },
    female: {
      name: "Sofía Villalba",
      role: "Heredera",
      bio: "Nieta del difunto y aspirante directa a la fortuna familiar.",
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
      cardImage: "src/assets/images/personajes_masculinos/card-m-hugo.png"
    },
    female: {
      name: "Lucía Herrera",
      role: "Jardinera",
      bio: "Cuida los terrenos y sabe quién usó los accesos exteriores.",
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
      bio: "Hermano del fallecido en disputa económica por el testamento.",
      cardImage: "src/assets/images/personajes_masculinos/card-m-victor.png"
    },
    female: {
      name: "Elena Torres",
      role: "Heredera",
      bio: "Hermana de la víctima en disputa económica por el testamento.",
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

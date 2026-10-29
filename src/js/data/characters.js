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
      secret: "Colecciona y diseca ilegalmente animales en peligro de extinción cazados en la finca.",
      cardImage: "src/assets/images/personajes_masculinos/card-m-cazador.png"
    },
    female: {
      name: "La Cazadora",
      role: "Cazadora",
      bio: "Conoce todos los senderos y secretos del bosque de la finca.",
      secret: "Colecciona y diseca ilegalmente animales en peligro de extinción cazados en la finca.",
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
      secret: "Chantajeado tras plagiar las sinfonías maestras que el difunto guardaba bajo llave.",
      cardImage: "src/assets/images/personajes_masculinos/card-m-leonardo.png"
    },
    female: {
      name: "Valentina Santos",
      role: "Música",
      bio: "Amenizaba la velada exclusiva antes de que se apagaran las luces.",
      secret: "Chantajeada tras plagiar las sinfonías maestras que el difunto guardaba bajo llave.",
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
      secret: "Prescribió intencionadamente sustancias peligrosas para encubrir una negligencia médica.",
      cardImage: "src/assets/images/personajes_masculinos/card-m-alfonso.png"
    },
    female: {
      name: "Dra. Isabel Ortega",
      role: "Médica",
      bio: "Administraba la medicación diaria y confidencial del difunto.",
      secret: "Prescribió intencionadamente sustancias peligrosas para encubrir una negligencia médica.",
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
      secret: "La víctima poseía informes oficiales sobre su implicación en tráfico ilícito de armas.",
      cardImage: "src/assets/images/personajes_masculinos/card-m-santamaria.png"
    },
    female: {
      name: "General Araujo",
      role: "Militar",
      bio: "General y vieja amiga de juventud de la víctima.",
      secret: "La víctima poseía informes oficiales sobre su implicación en tráfico ilícito de armas.",
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
      secret: "Vació cuentas bancarias familiares simulando inversiones urgentes ya descubiertas.",
      cardImage: "src/assets/images/personajes_masculinos/card-m-elias.png"
    },
    female: {
      name: "Sofía Villalba",
      role: "Heredera",
      bio: "Nieta del difunto y aspirante directa a la fortuna familiar.",
      secret: "Vació cuentas bancarias familiares simulando inversiones urgentes ya descubiertas.",
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
      secret: "Enterró evidencias incriminatorias en los terrenos exteriores a cambio de dinero negro.",
      cardImage: "src/assets/images/personajes_masculinos/card-m-hugo.png"
    },
    female: {
      name: "Lucía Herrera",
      role: "Jardinera",
      bio: "Cuida los terrenos y sabe quién usó los accesos exteriores.",
      secret: "Enterró evidencias incriminatorias en los terrenos exteriores a cambio de dinero negro.",
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
      secret: "Iba a ser formalmente desheredado esa noche tras amenazar a la víctima por el testamento.",
      cardImage: "src/assets/images/personajes_masculinos/card-m-victor.png"
    },
    female: {
      name: "Elena Torres",
      role: "Heredera",
      bio: "Era hermana de la víctima en disputa por el testamento.",
      secret: "Iba a ser formalmente desheredada esa noche tras amenazar a la víctima por el testamento.",
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

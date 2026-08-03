/**
 * Character Builder Spanish Translation Dictionary (es)
 */
window.BUILDER_I18N = window.BUILDER_I18N || {};

window.BUILDER_I18N['es'] = {
  rankTiers: {
    rookie: 'Novato',
    seasoned: 'Experimentado',
    veteran: 'Veterano',
    exemplar: 'Ejemplar',
    legend: 'Leyenda'
  },
  ui: {
    creationPoints: 'Puntos de Creación',
    advancementAP: 'PA de Avance',
    grandTotal: 'Suma Total',
    totalSkillCostsSummary: 'Suma Total de Costes de Habilidad',
    cumulativeSummary: 'Resumen acumulado de todos los costes por habilidad',
    speciesFree: 'ESPECIE (GRATIS)',
    favored: 'FAVORECIDA',
    capReached: 'LÍMITE ALCANZADO',
    maxSkillRank: 'Rango Máx Habilidad',
    maxBroadSkills: 'Máx Habilidades Generales',
    baseAP: 'PA Base',
    earnedAP: 'PA Ganados / XP',
    availableSP: 'PH Disponibles',
    spentSP: 'PH Gastados',
    availableAP: 'PA Disponibles',
    spentAP: 'PA Gastados',
    finalizeCharacter: 'Finalizar Personaje e Iniciar Campaña',
    enterCampaign: 'Modo Campaña',
    characterFinalized: 'Personaje Finalizado en Campaña',
    saveCharacter: 'Guardar Personaje JSON',
    loadCharacter: 'Cargar Personaje JSON',
    printSheet: 'Imprimir Hoja de Personaje',
    resetBuilder: 'Reiniciar Creador',
    confirmReset: '¿Estás seguro de que deseas reiniciar todas las opciones?',
    confirmFinalize: 'Al entrar en Modo Campaña se bloquearán tus Puntos de Creación (BP). ¿Continuar?'
  },
  factions: {
    austrin: {
      name: 'Esencialidad Austrin',
      bonus: '-1 paso en Armas Pesadas o Armas a Distancia Modernas (acumulable con Combate Especialista para -2).',
      desc: 'El vínculo entre un Austrin y su arma trasciende la comprensión. Cultura entrenada en la serenidad bajo fuego enemigo.'
    },
    borealis: {
      name: 'República de Boreal',
      bonus: '+1 Inteligencia (máx. 15) y Defecto "Obsesionado" moderado (+4) automático.',
      desc: 'Educación adaptativa avanzada y siglos de selección intelectual. Propensos a distracción por investigación desmedida.'
    },
    hatire: {
      name: 'Comunidad Hatire',
      bonus: 'Ventaja "Fe" (Faith) gratis. Opción de mejorar a dado base -d8 con Puntos de Habilidad.',
      desc: 'Sociedad caracterizada por la devoción, pasión y vínculos espirituales con el Cosimir.'
    },
    kristand: {
      name: 'Unión Libre de Kristand',
      bonus: '-1 paso en actividades informáticas/Grid; +1 paso de penalización en cheques de acción del mundo real.',
      desc: 'Mentes perfeccionadas para medios digitales e interfaces de la Red que reaccionan más lento en el entorno físico.'
    },
    nariac: {
      name: 'Dominio Nariac',
      bonus: 'Ventaja "Interfaz Cibernética" gratis + 1 objeto ciberware gratis (≤ $5,000) + Monitor de Seguridad gratis.',
      desc: 'Integración cibernética desde la infancia y superficies metálicas bajo la vigilancia constante del Dominio.'
    },
    orion: {
      name: 'Liga de Orión',
      bonus: '+1 Personalidad (máx. 15) y -1 paso de bonificación en habilidad Cultura.',
      desc: 'Fundadores de valores de relaciones interpersonales, entendimiento intercultural y reputación de buena voluntad.'
    },
    orlamu: {
      name: 'Teocracia Orlamu',
      bonus: '-1 paso en Ciencias Físicas/Navegación. Mindwalkers Orlamu descuentan 1 PT en habilidades psiónicas.',
      desc: 'Pioneros científicos y espirituales con prestigiosas academias psiónicas e influencia Fraal.'
    },
    rigunmor: {
      name: 'Consorcio Estelar Rigunmor',
      bonus: '-1 paso en Interacción y Engaño; descuento en Bargain; Ventaja "Filthy Rich" gratis o +6 Puntos de Habilidad.',
      desc: 'Los comerciantes más prósperos y hábiles de la galaxia capaces de confortar al cliente en cualquier trato.'
    },
    starmech: {
      name: 'Colectivo StarMech',
      bonus: '-1 paso en Ciencias Técnicas; opción de Defecto Oblivious (doble PH: +8) u Obsessed (4/8/12 PH).',
      desc: 'Formación ocupacional técnica insuperable con propensión al hedonismo y evasión física.'
    },
    thuldan: {
      name: 'Imperio Thuldano',
      bonus: 'Máximos de Fuerza (FUE) y Constitución (CON) aumentados a 15 para humanos thuldanos.',
      desc: 'Manipulación genética continua y programas de educación física extrema para la perfección corporal.'
    },
    sol: {
      name: 'Unión de Sol',
      bonus: '+2 Puntos de Característica adicionales (presupuesto de 62 puntos en lugar de 60).',
      desc: 'La rica diversidad y desarrollo cultural de la cuna de la humanidad fortalece las capacidades base.'
    },
    voidcorp: {
      name: 'VoidCorp',
      bonus: 'Habilidades "Business" y "Business-corporate" GRATIS (-1 paso de bonificación en Business) + 1º logro lleno.',
      desc: 'Preparación despiadada para el mundo corporativo interestelar con avance acelerado de carrera.'
    },
    concord: {
      name: 'Concordia Galáctica',
      bonus: '+1 al Modificador de Resistencia a elección (FUE, DES, CON, VOL o INT).',
      desc: 'Defensores de la humanidad que encarnan el honor, serenidad y resistencia contra perturbaciones.'
    }
  },
  species: {
    human: { name: 'Humano', desc: 'Versátiles y culturalmente diversos, con tendencia a especializarse.' },
    fraal: { name: 'Fraal', desc: 'Navegantes estelares ancestrales dotados de habilidades psiónicas.' },
    mechalus: { name: 'Mechalus', desc: 'Humanoides integrados cibernéticamente guiados por la lógica.' },
    sesheyan: { name: 'Sesheyan', desc: 'Cazadores alados con múltiples ojos y mentalidad alienígena.' },
    tsa: { name: 'T\'sa', desc: 'Reptiloides ágiles y apasionados por la velocidad y la ingeniería.' },
    weren: { name: 'Weren', desc: 'Gigantescos guerreros peludos con una fuerza inmensa.' }
  }
};

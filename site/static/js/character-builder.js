/**
 * Alternity RPG Character Builder Suite
 * Includes Official Star*Drive Faction Rules & Benefits
 */

document.addEventListener('DOMContentLoaded', () => {
  const data = window.AAA_CHARACTER_DATA || {};
  const isEs = data.lang === 'es';

  // State
  const state = {
    step: 1,
    bio: {
      name: '',
      player: '',
      concept: '',
      motivation: '',
      attitude: '',
      traits: ''
    },
    faction: 'concord',
    concordResModStat: 'WIL', // Default choice for Concord +1 Res Mod
    austrinSpecSkill: 'Modern Ranged Weapons', // Default choice for Austrin
    rigunmorBonusChoice: 'points', // 'perk' (Filthy Rich) or 'points' (+6 SP)
    species: 'human',
    background: null,
    profession: 'combat-spec',
    abilities: {
      STR: 10,
      DEX: 10,
      CON: 10,
      INT: 10,
      WIL: 10,
      PER: 10
    },
    skills: {},
    perks: [],
    flaws: [],
    // Campaign Advancement
    isFinalized: false,
    earnedAP: 0,
    advancementSkills: {},
    advancementAbilities: {}
  };

  function getCharacterTitle(totalAP) {
    if (totalAP >= 300) return { title: isEs ? 'Leyenda' : 'Legend', maxSkillRank: isEs ? 'Sin Límite' : 'No Limit', maxBroad: 13 };
    if (totalAP >= 200) return { title: isEs ? 'Ejemplar' : 'Exemplar', maxSkillRank: 12, maxBroad: 11 };
    if (totalAP >= 100) return { title: isEs ? 'Veterano' : 'Veteran', maxSkillRank: 10, maxBroad: 9 };
    if (totalAP >= 50) return { title: isEs ? 'Experimentado' : 'Seasoned', maxSkillRank: 8, maxBroad: 7 };
    return { title: isEs ? 'Novato' : 'Rookie', maxSkillRank: 5, maxBroad: 5 };
  }

  function getRankBenefitDescription(ranks) {
    if (!ranks || ranks <= 0) return isEs ? 'Sin Rango' : 'Untrained';
    if (ranks === 1) return isEs ? 'Rango 1: Puntuación Base (+1 Objetivo)' : 'Rank 1: Base Score (+1 Target)';
    if (ranks === 2) return isEs ? 'Rango 2: Precisión (+2 Objetivo)' : 'Rank 2: Precision (+2 Target)';
    if (ranks === 3) return isEs ? 'Rango 3: Maestría de Creación (+3 Objetivo)' : 'Rank 3: Creation Mastery (+3 Target)';
    return isEs ? `Rango ${ranks}: Especialista (+${ranks} Objetivo)` : `Rank ${ranks}: Specialist (+${ranks} Target)`;
  }

  function getAdvancementSkillCost(skillName, targetRank) {
    let standardCost = 3;
    let isBroad = false;
    let category = 'Other';

    if (data.skillsTable && data.skillsTable.items) {
      for (const cat of data.skillsTable.items) {
        for (const broad of cat.items) {
          if (broad.skill === skillName) {
            standardCost = broad.cost || 3;
            isBroad = true;
            category = cat.skill;
            break;
          }
          if (broad.items) {
            const spec = broad.items.find(s => s.skill === skillName);
            if (spec) {
              standardCost = spec.cost || 3;
              isBroad = false;
              category = cat.skill;
              break;
            }
          }
        }
      }
    }

    if (isBroad) {
      let favored = isFavored(skillName, category);
      return favored ? Math.max(1, standardCost - 1) : standardCost;
    } else {
      let parentBroadName = getParentBroadSkillName(skillName);
      let favored = isFavored(skillName, category, parentBroadName);
      let baseCost = favored ? Math.max(1, standardCost - 1) : standardCost;

      if (targetRank >= 11) baseCost += 6;
      else if (targetRank >= 9) baseCost += 4;
      else if (targetRank >= 6) baseCost += 2;

      return baseCost;
    }
  }

  function calculateCampaignSpentAP() {
    let spent = 0;
    if (state.advancementAbilities) {
      Object.values(state.advancementAbilities).forEach(pts => {
        spent += (parseInt(pts, 10) || 0) * 10;
      });
    }

    if (state.advancementSkills) {
      Object.entries(state.advancementSkills).forEach(([skillName, campaignRanks]) => {
        const totalRanks = state.skills[skillName] ? state.skills[skillName].ranks : 0;
        const creationRanks = Math.max(0, totalRanks - campaignRanks);
        for (let r = 1; r <= campaignRanks; r++) {
          const targetRank = creationRanks + r;
          spent += getAdvancementSkillCost(skillName, targetRank);
        }
      });
    }

    return spent;
  }

  const STORAGE_KEY = 'stardrive_character_builder_state_v1';

  function saveStateToLocalStorage() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    } catch (e) {
      console.warn('Unable to save character state to localStorage', e);
    }
  }

  function loadStateFromLocalStorage() {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) {
        const parsed = JSON.parse(saved);
        Object.assign(state, parsed);
        if (state.bio) {
          const fields = {
            'cb-input-name': state.bio.name,
            'cb-input-player': state.bio.player,
            'cb-input-concept': state.bio.concept,
            'cb-input-motivation': state.bio.motivation,
            'cb-input-attitude': state.bio.attitude,
            'cb-input-traits': state.bio.traits
          };
          Object.entries(fields).forEach(([id, val]) => {
            const el = document.getElementById(id);
            if (el && val !== undefined) el.value = val;
          });
        }
      }
    } catch (e) {
      console.warn('Unable to load character state from localStorage', e);
    }
  }

  // Official Star*Drive Factions Data & Mechanics
  const FACTION_DATA = {
    austrin_ontis: {
      id: 'austrin_ontis',
      name: 'Austrin-Ontis Unlimited',
      bonus: isEs ? '-1 paso en Armas Pesadas o Armas a Distancia Modernas (acumulable con Combate Especialista para -2).' : '-1 step bonus to Heavy Weapons or Modern Ranged Weapons (stacks with Combat Spec for -2).',
      desc: isEs ? 'El vínculo entre un Austrin y su arma trasciende la comprensión. Cultura entrenada en la serenidad bajo fuego enemigo.' : 'Cultural flair for firearms born from centuries of coolness under fire and enhanced hand-eye coordination.',
      apply: (st) => {}
    },
    borealis: {
      id: 'borealis',
      name: isEs ? 'República de Boreal' : 'Borealis Republic',
      bonus: isEs ? '+1 Inteligencia (máx. 15) y Defecto "Obsesionado" moderado (+4) automático.' : '+1 Intelligence score (max 15 for Humans) & automatic Moderate Obsessed (+4) flaw.',
      desc: isEs ? 'Educación adaptativa avanzada y siglos de selección intelectual. Propensos a distracción por investigación desmedida.' : 'Highly adaptive early education and intellect, though prone to obsession with new discovery.',
      apply: (st) => {
        if (!st.flaws.includes('Obsessed (Borealin Discovery)')) {
          st.flaws.push('Obsessed (Borealin Discovery)');
        }
      }
    },
    hatire: {
      id: 'hatire',
      name: isEs ? 'Comunidad Hatire' : 'Hatire Community',
      bonus: isEs ? 'Ventaja "Fe" (Faith) gratis. Opción de mejorar a dado base -d8 con Puntos de Habilidad.' : 'Free "Faith" perk. Ability to enhance Faith strength to base -d8 situation die.',
      desc: isEs ? 'Sociedad caracterizada por la devoción, pasión y vínculos espirituales con el Cosimir.' : 'A society of passionate devotion and spiritual bond with the Cosimir.',
      apply: (st) => {
        if (!st.perks.includes('Faith')) {
          st.perks.push('Faith');
        }
      }
    },
    insight: {
      id: 'insight',
      name: 'Insight',
      bonus: isEs ? '-1 paso en actividades informáticas/Grid; +1 paso de penalización en cheques de acción del mundo real.' : '-1 step bonus to all Computer/Grid activities; +1 step penalty on real-world action checks.',
      desc: isEs ? 'Mentes perfeccionadas para medios digitales e interfaces de la Red que reaccionan más lento en el entorno físico.' : 'Genius technical wizardry and Grid mastery, coupled with slower physical real-world reaction.',
      apply: (st) => {}
    },
    nariac: {
      id: 'nariac',
      name: isEs ? 'Dominio Nariac' : 'Nariac Domain',
      bonus: isEs ? '1 objeto ciberware gratis (≤ $5,000, no cuenta en cibertolerancia) + Monitor de Seguridad gratis.' : '1 free cyber gear item (≤ $5,000, free cyber tolerance) + free implanted security tracking monitor.',
      desc: isEs ? 'Integración cibernética desde la infancia y superficies metálicas bajo la vigilancia constante del Dominio.' : 'Cybernetic integration from childhood monitored constantly by Domain security trackers.',
      apply: (st) => {
        if (!st.perks.includes('Free Cyber Gear ($5,000)')) {
          st.perks.push('Free Cyber Gear ($5,000)');
        }
      }
    },
    orion: {
      id: 'orion',
      name: isEs ? 'Liga de Orión' : 'Orion League',
      bonus: isEs ? '+1 Personalidad (máx. 15) y -1 paso de bonificación en habilidad Cultura.' : '+1 Personality score (max 15) & -1 step bonus to Culture broad/specialty skills.',
      desc: isEs ? 'Fundadores de valores de relaciones interpersonales, entendimiento intercultural y reputación de buena voluntad.' : 'Emphasizes intercultural goodwill, high interpersonal relations, and universal tolerance.',
      apply: (st) => {}
    },
    orlamu: {
      id: 'orlamu',
      name: isEs ? 'Teocracia Orlamu' : 'Orlamu Theocracy',
      bonus: isEs ? '-1 paso en Ciencias Físicas/Navegación. Mindwalkers Orlamu descuentan 1 PT en habilidades psiónicas.' : '-1 step bonus to Physical Science/Navigation. Orlamu Mindwalkers discount all psionic skills by 1 SP/AP.',
      desc: isEs ? 'Pioneros científicos y espirituales con prestigiosas academias psiónicas e influencia Fraal.' : 'Scientific and spiritual pioneers with legendary psionic academies and Fraal influence.',
      apply: (st) => {}
    },
    rigunmor: {
      id: 'rigunmor',
      name: isEs ? 'Consorcio Estelar Rigunmor' : 'Rigunmor Star Consortium',
      bonus: isEs ? '-1 paso en Interacción y Engaño; descuento en Bargain; Ventaja "Filthy Rich" gratis o +6 Puntos de Habilidad.' : '-1 step to Interaction & Deception; discount on Bargain; Free "Filthy Rich" perk OR +6 Skill Points.',
      desc: isEs ? 'Los comerciantes más prósperos y hábiles de la galaxia capaces de confortar al cliente en cualquier trato.' : 'Prosperous trading conglomerate with unmatched bargaining skill and wealthy assets.',
      apply: (st) => {
        if (st.rigunmorBonusChoice === 'perk' && !st.perks.includes('Filthy Rich')) {
          st.perks.push('Filthy Rich');
        }
      }
    },
    starmech: {
      id: 'starmech',
      name: isEs ? 'Colectivo StarMech' : 'StarMech Collective',
      bonus: isEs ? '-1 paso en Ciencias Técnicas; opción de Defecto Oblivious (doble PH: +8) u Obsessed (4/8/12 PH).' : '-1 step bonus to Technical Science; option for Oblivious flaw (double SP: 8) or Obsessed flaw (4/8/12 SP).',
      desc: isEs ? 'Formación ocupacional técnica insuperable con propensión al hedonismo y evasión física.' : 'Unmatched technical training combined with a culture prone to sensory hedonism.',
      apply: (st) => {}
    },
    thuldan: {
      id: 'thuldan',
      name: isEs ? 'Imperio Thuldano' : 'Thuldan Empire',
      bonus: isEs ? 'Máximos de Fuerza (FUE) y Constitución (CON) aumentados a 15 para humanos thuldanos.' : 'Human Thuldan heroes increase maximum Strength & Constitution bounds to 15.',
      desc: isEs ? 'Manipulación genética continua y programas de educación física extrema para la perfección corporal.' : 'Centuries of genetic manipulation and extreme physical education programs.',
      apply: (st) => {}
    },
    union_of_sol: {
      id: 'union_of_sol',
      name: isEs ? 'Unión de Sol' : 'Union of Sol',
      bonus: isEs ? '+2 Puntos de Característica adicionales (presupuesto de 62 puntos en lugar de 60).' : '+2 bonus Ability Points during character creation (62 points budget instead of 60).',
      desc: isEs ? 'La rica diversidad y desarrollo cultural de la cuna de la humanidad fortalece las capacidades base.' : 'Richly diverse ancestral homeworld culture providing unweakened foundational abilities.',
      apply: (st) => {}
    },
    voidcorp: {
      id: 'voidcorp',
      name: 'Voidcorp',
      bonus: isEs ? 'Habilidades "Business" y "Business-corporate" GRATIS (-1 paso de bonificación en Business) + 1º logro lleno.' : 'FREE Business broad & Business-corporate specialty skills (-1 step bonus) + 1st achievement box filled.',
      desc: isEs ? 'Preparación despiadada para el mundo corporativo interestelar con avance acelerado de carrera.' : 'Ruthless corporate preparation ensuring faster career advancement and business mastery.',
      apply: (st) => {
        if (!st.skills['Business']) {
          st.skills['Business'] = { ranks: 1, isBroad: true, standardCost: 0, category: 'Social' };
        }
        if (!st.skills['Business-corporate']) {
          st.skills['Business-corporate'] = { ranks: 1, isBroad: false, standardCost: 0, category: 'Social' };
        }
      }
    },
    concord: {
      id: 'concord',
      name: isEs ? 'Concordia Galáctica' : 'Galactic Concord',
      bonus: isEs ? '+1 al Modificador de Resistencia a elección (FUE, DES, CON, VOL o INT).' : '+1 bonus to a chosen Resistance Modifier (STR, DEX, CON, WIL, or INT).',
      desc: isEs ? 'Defensores de la humanidad que encarnan el honor, serenidad y resistencia contra perturbaciones.' : 'Peacekeeping interstellar guardians trained to resist physical and mental influences.',
      apply: (st) => {}
    }
  };

  // Species Data & Base Limits
  const SPECIES_DATA = {
    human: {
      id: 'human',
      name: isEs ? 'Humano' : 'Human',
      limits: { STR: [4, 14], DEX: [4, 14], CON: [4, 14], INT: [4, 14], WIL: [4, 14], PER: [4, 14] },
      desc: isEs ? 'Versátiles y culturalmente diversos, con tendencia a especializarse.' : 'Versatile and culturally diverse, while individuals tend to specialize.',
      freePerks: []
    },
    fraal: {
      id: 'fraal',
      name: isEs ? 'Fraal' : 'Fraal',
      limits: { STR: [3, 12], DEX: [4, 14], CON: [3, 12], INT: [7, 17], WIL: [7, 17], PER: [5, 15] },
      desc: isEs ? 'Navegantes estelares ancestrales dotados de habilidades psiónicas.' : 'Ancient, psionically gifted starfarers.',
      freePerks: [isEs ? 'Psiónica innata' : 'Innate Psionics']
    },
    mechalus: {
      id: 'mechalus',
      name: isEs ? 'Mechalus' : 'Mechalus',
      limits: { STR: [5, 15], DEX: [4, 14], CON: [5, 15], INT: [7, 17], WIL: [3, 12], PER: [3, 12] },
      desc: isEs ? 'Humanoides integrados cibernéticamente guiados por la lógica.' : 'Cybernetically integrated logic-driven humanoids.',
      freePerks: [isEs ? 'Interfaz cibernética' : 'Cybernetic Interface']
    },
    sesheyan: {
      id: 'sesheyan',
      name: isEs ? 'Sesheyan' : 'Sesheyan',
      limits: { STR: [3, 12], DEX: [5, 15], CON: [4, 14], INT: [3, 12], WIL: [5, 15], PER: [3, 12] },
      desc: isEs ? 'Cazadores alados con múltiples ojos y mentalidad alienígena.' : 'Winged hunters with multiple eyes and alien mindset.',
      freePerks: [isEs ? 'Vuelo de planeo' : 'Gliding Flight']
    },
    tsa: {
      id: 'tsa',
      name: "T'sa",
      limits: { STR: [3, 12], DEX: [7, 17], CON: [3, 12], INT: [5, 15], WIL: [4, 14], PER: [5, 15] },
      desc: isEs ? 'Manitas reptilianos rápidos y de instinto agudo.' : 'Fast, reptilian tinkers with sharp instincts.',
      freePerks: [isEs ? 'Piel escamosa' : 'Scaly Hide']
    },
    weren: {
      id: 'weren',
      name: isEs ? 'Weren' : 'Weren',
      limits: { STR: [7, 17], DEX: [3, 12], CON: [7, 17], INT: [3, 12], WIL: [3, 12], PER: [3, 12] },
      desc: isEs ? 'Grandes guerreros-filósofos peludos.' : 'Large, furry philosopher-warriors.',
      freePerks: [isEs ? 'Armas naturales (Garras)' : 'Natural Weapons (Claws)']
    }
  };

  const PROFESSION_DATA = {
    'combat-spec': {
      id: 'combat-spec',
      name: isEs ? 'Especialista de Combate' : 'Combat Spec',
      reqs: { STR: 11, CON: 9 },
      desc: isEs ? 'Maestros del combate táctico y el armamento pesado.' : 'Masters of tactical combat and weaponry.',
      favoredCategories: ['Combat'],
      favoredSkills: ['Athletics', 'Armor Operation', 'Tactics', 'Heavy Weapons', 'Melee Combat', 'Modern Ranged Weapons']
    },
    'free-agent': {
      id: 'free-agent',
      name: isEs ? 'Agente Libre' : 'Free Agent',
      reqs: { DEX: 11, WIL: 9 },
      desc: isEs ? 'Expertos en sigilo, pilotaje y operaciones encubiertas.' : 'Experts in stealth, piloting, and covert ops.',
      favoredCategories: ['Social'],
      favoredSkills: ['Covert Ops', 'Deception', 'Stealth', 'Drive', 'Pilot', 'Acrobatics', 'Culture']
    },
    'tech-op': {
      id: 'tech-op',
      name: isEs ? 'Operador Técnico' : 'Tech Op',
      reqs: { DEX: 9, INT: 11 },
      desc: isEs ? 'Especialistas en tecnología, informática e ingeniería.' : 'Specialists in technology, computers, and engineering.',
      favoredCategories: ['Technical', 'Academic'],
      favoredSkills: ['Computer Science', 'Technical Sciences', 'Physical Science', 'System Operation', 'Navigation', 'Repair']
    },
    'mindwalker': {
      id: 'mindwalker',
      name: isEs ? 'Mindwalker (Psiónico)' : 'Mindwalker',
      reqs: { CON: 9, INT: 9, WIL: 11 },
      desc: isEs ? 'Maestros de las disciplinas y poderes psiónicos.' : 'Masters of psionic disciplines and mental powers.',
      favoredCategories: ['Psionics'],
      favoredSkills: ['Awareness', 'Resolve', 'Telepathy', 'Telekinesis', 'Biokinesis', 'ESP', 'Psychoportation']
    }
  };

  // Helper Functions
  function getBackgroundItems() {
    if (!data.backgrounds) return [];
    if (Array.isArray(data.backgrounds)) return data.backgrounds;
    if (data.backgrounds.all && data.backgrounds.all.items && data.backgrounds.all.items[0]) {
      return data.backgrounds.all.items[0].items || [];
    }
    return [];
  }

  function getBackgroundFavoredSkills(bg) {
    if (!bg) return [];
    if (Array.isArray(bg.favored_skills)) return bg.favored_skills;
    const skills = [];
    const str = `${bg.favored_broad_skill || ''} ${bg.favored_specialty_skills || ''}`;
    const matches = str.match(/\[(.*?)\]/g);
    if (matches) {
      matches.forEach(m => {
        const clean = m.replace(/^\[/, '').replace(/\]$/, '').trim();
        if (clean && !skills.includes(clean)) skills.push(clean);
      });
    }
    return skills;
  }

  function getBackgroundFavoredPerks(bg) {
    if (!bg) return [];
    const str = bg.favored_perks || '';
    const perks = [];
    const matches = str.match(/\[(.*?)\]/g);
    if (matches) {
      matches.forEach(m => {
        const clean = m.replace(/^\[/, '').replace(/\]$/, '').trim();
        if (clean && !perks.includes(clean)) perks.push(clean);
      });
    }
    if (perks.length === 0 && str.trim()) {
      perks.push(str.replace(/\*/g, '').trim());
    }
    return perks;
  }

  function getBackgroundFlaw(bg) {
    if (!bg || !bg.flaw) return null;
    const str = bg.flaw;
    const match = str.match(/\[(.*?)\]/);
    if (match && match[1]) {
      return match[1].trim();
    }
    const clean = str.split('(')[0].replace(/\*/g, '').trim();
    return clean || null;
  }

  function getPerksList() {
    if (!data.perksFlaws) return [];
    const p = data.perksFlaws.perks;
    if (!p) return [];
    if (Array.isArray(p)) return p;
    if (p.items && p.items[0] && Array.isArray(p.items[0].items)) {
      return p.items[0].items;
    }
    if (Array.isArray(p.items)) return p.items;
    return [];
  }

  function getFlawsList() {
    if (!data.perksFlaws) return [];
    const f = data.perksFlaws.flaws;
    if (!f) return [];
    if (Array.isArray(f)) return f;
    if (f.items && f.items[0] && Array.isArray(f.items[0].items)) {
      return f.items[0].items;
    }
    if (Array.isArray(f.items)) return f.items;
    return [];
  }

  function isFavoredPerk(perkName) {
    if (!perkName) return false;
    const bgItems = getBackgroundItems();
    if (state.background && bgItems.length > 0) {
      const bg = bgItems.find(b => b.name === state.background || b.id === state.background);
      if (bg) {
        const bgFav = getBackgroundFavoredPerks(bg);
        if (bgFav.some(fp => perkName.toLowerCase().includes(fp.toLowerCase()) || fp.toLowerCase().includes(perkName.toLowerCase()))) {
          return true;
        }
      }
    }
    const prof = PROFESSION_DATA[state.profession];
    if (prof && prof.favoredPerks) {
      if (prof.favoredPerks.some(fp => perkName.toLowerCase().includes(fp.toLowerCase()) || fp.toLowerCase().includes(perkName.toLowerCase()))) {
        return true;
      }
    }
    return false;
  }

  function getPerkCost(perkObjOrName, level = 1) {
    const perksList = getPerksList();
    const perkName = typeof perkObjOrName === 'string' ? perkObjOrName : (perkObjOrName ? perkObjOrName.name : '');
    if (typeof perkObjOrName === 'object' && perkObjOrName && perkObjOrName.level) {
      level = perkObjOrName.level;
    }
    const perkObj = perksList.find(p => p.name === perkName);

    let options = [3];
    if (perkObj && perkObj.cost) {
      const parts = perkObj.cost.split('/');
      const parsed = parts.map(p => parseInt(p, 10)).filter(n => !isNaN(n));
      if (parsed.length > 0) options = parsed;
    }

    const selectedIdx = Math.min(Math.max(0, level - 1), options.length - 1);
    const rawCost = options[selectedIdx];

    const favored = isFavoredPerk(perkName);
    const finalCost = favored ? Math.max(1, rawCost - 1) : rawCost;
    return { rawCost, finalCost, favored, options };
  }

  function getFlawBonus(flawObjOrName, level = 1) {
    const flawsList = getFlawsList();
    const flawName = typeof flawObjOrName === 'string' ? flawObjOrName : (flawObjOrName ? flawObjOrName.name : '');
    if (typeof flawObjOrName === 'object' && flawObjOrName && flawObjOrName.level) {
      level = flawObjOrName.level;
    }
    const flawObj = flawsList.find(f => f.name === flawName);

    let options = [3];
    if (flawObj && flawObj.bonus_points) {
      const clean = flawObj.bonus_points.replace(/\+/g, '');
      const parts = clean.split('/');
      const parsed = parts.map(p => parseInt(p, 10)).filter(n => !isNaN(n));
      if (parsed.length > 0) options = parsed;
    }

    const selectedIdx = Math.min(Math.max(0, level - 1), options.length - 1);
    const rawBonus = options[selectedIdx];
    return { rawBonus, options };
  }

  function getResMod(score) {
    if (score <= 4) return -2;
    if (score <= 6) return -1;
    if (score <= 10) return 0;
    if (score <= 12) return 1;
    if (score <= 14) return 2;
    if (score <= 16) return 3;
    if (score <= 18) return 4;
    return 5;
  }

  function getMovementRates(strPlusDex) {
    if (strPlusDex <= 7) return { sprint: 6, run: 4, walk: 2, swim: 1, glide: 6 };
    if (strPlusDex <= 9) return { sprint: 8, run: 6, walk: 3, swim: 1, glide: 8 };
    if (strPlusDex <= 11) return { sprint: 10, run: 8, walk: 4, swim: 2, glide: 10 };
    if (strPlusDex <= 13) return { sprint: 12, run: 8, walk: 4, swim: 2, glide: 12 };
    if (strPlusDex <= 15) return { sprint: 14, run: 10, walk: 5, swim: 2, glide: 14 };
    if (strPlusDex <= 17) return { sprint: 16, run: 10, walk: 5, swim: 3, glide: 16 };
    if (strPlusDex <= 19) return { sprint: 18, run: 12, walk: 6, swim: 3, glide: 18 };
    if (strPlusDex <= 21) return { sprint: 20, run: 12, walk: 6, swim: 3, glide: 20 };
    if (strPlusDex <= 23) return { sprint: 22, run: 14, walk: 7, swim: 3, glide: 22 };
    if (strPlusDex <= 25) return { sprint: 24, run: 16, walk: 8, swim: 4, glide: 24 };
    if (strPlusDex <= 27) return { sprint: 26, run: 16, walk: 8, swim: 4, glide: 26 };
    if (strPlusDex <= 29) return { sprint: 28, run: 18, walk: 9, swim: 4, glide: 28 };
    if (strPlusDex <= 31) return { sprint: 30, run: 20, walk: 10, swim: 5, glide: 30 };
    return { sprint: 32, run: 20, walk: 10, swim: 5, glide: 32 };
  }

  function getActionsPerRound(conPlusWil) {
    if (conPlusWil <= 15) return 1;
    if (conPlusWil <= 23) return 2;
    if (conPlusWil <= 31) return 3;
    return 4;
  }

  const SPECIES_FREE_BROAD_SLUGS = {
    human: ['athletics', 'vehicle-operation', 'stamina', 'knowledge', 'awareness', 'interaction'],
    fraal: ['awareness', 'resolve', 'vehicle-operation', 'knowledge', 'interaction', 'telepathy'],
    mechalus: ['athletics', 'vehicle-operation', 'stamina', 'knowledge', 'awareness', 'computer-science'],
    sesheyan: ['melee-combat', 'acrobatics', 'stamina', 'knowledge', 'awareness', 'interaction'],
    tsa: ['athletics', 'covert-ops', 'stamina', 'knowledge', 'awareness', 'interaction'],
    weren: ['athletics', 'melee-combat', 'stamina', 'knowledge', 'awareness', 'interaction']
  };

  function isSpeciesFreeBroad(broadSkill) {
    if (!broadSkill) return false;
    const slugs = SPECIES_FREE_BROAD_SLUGS[state.species] || [];
    const skillName = typeof broadSkill === 'string' ? broadSkill : (broadSkill.skill || '');
    const skillUrl = typeof broadSkill === 'object' && broadSkill.url ? broadSkill.url : '';

    if (skillUrl) {
      const slug = skillUrl.toLowerCase().split('#')[0].split('/').filter(Boolean).pop();
      if (slugs.includes(slug)) return true;
    }

    const nameLower = skillName.toLowerCase();
    return slugs.some(s => {
      const norm = s.replace('-', ' ');
      return nameLower.includes(norm) || nameLower.includes(s);
    });
  }

  function syncSpeciesFreeSkills() {
    if (!data.skillsTable || !data.skillsTable.items) return;
    data.skillsTable.items.forEach(category => {
      category.items.forEach(broadSkill => {
        if (isSpeciesFreeBroad(broadSkill)) {
          if (!state.skills[broadSkill.skill]) {
            state.skills[broadSkill.skill] = {
              ranks: 1,
              isBroad: true,
              isSpeciesFree: true,
              standardCost: broadSkill.cost,
              category: category.skill
            };
          } else {
            state.skills[broadSkill.skill].isSpeciesFree = true;
          }
        }
      });
    });
  }

  function isFavored(skillName, skillCategory, parentBroadSkillName = null) {
    if (parentBroadSkillName && isFavored(parentBroadSkillName, skillCategory)) {
      return true;
    }
    const prof = PROFESSION_DATA[state.profession];
    if (prof) {
      if (prof.favoredCategories && prof.favoredCategories.includes(skillCategory)) return true;
      if (prof.favoredSkills && prof.favoredSkills.some(s => skillName.toLowerCase().includes(s.toLowerCase()) || s.toLowerCase().includes(skillName.toLowerCase()))) return true;
    }
    const bgItems = getBackgroundItems();
    if (state.background && bgItems.length > 0) {
      const bg = bgItems.find(b => b.name === state.background || b.id === state.background);
      if (bg) {
        const bgFav = getBackgroundFavoredSkills(bg);
        if (bgFav.some(s => skillName.toLowerCase().includes(s.toLowerCase()) || s.toLowerCase().includes(skillName.toLowerCase()))) return true;
      }
    }
    if (state.faction === 'austrin_ontis' && (skillName.includes('Heavy Weapons') || skillName.includes('Modern Ranged Weapons') || skillName.includes('Armas pesadas') || skillName.includes('Armas a distancia modernas'))) return true;
    if (state.faction === 'orion' && (skillName.includes('Culture') || skillName.includes('Cultura') || skillCategory === 'Culture' || skillCategory === 'Cultura')) return true;
    if (state.faction === 'orlamu' && (skillName.includes('Physical Science') || skillName.includes('Navigation') || skillName.includes('Ciencias físicas') || skillName.includes('Navegación'))) return true;
    if (state.faction === 'starmech' && (skillName.includes('Technical Science') || skillName.includes('Ciencias técnicas') || skillCategory === 'Technical Science')) return true;

    return false;
  }

  function getEffectiveSpeciesLimits() {
    const spec = JSON.parse(JSON.stringify(SPECIES_DATA[state.species].limits));
    if (state.species === 'human') {
      if (state.faction === 'borealis') spec.INT[1] = 15;
      if (state.faction === 'orion') spec.PER[1] = 15;
      if (state.faction === 'thuldan') {
        spec.STR[1] = 15;
        spec.CON[1] = 15;
      }
    }
    return spec;
  }

  function getEffectiveAbilityScore(stat) {
    let score = parseInt(state.abilities[stat], 10) || 10;
    if (state.species === 'human') {
      if (state.faction === 'orion' && stat === 'PER') score += 1;
      if (state.faction === 'borealis' && stat === 'INT') score += 1;
    }
    return score;
  }

  function getParentBroadSkillName(specSkillName) {
    if (!data.skillsTable || !data.skillsTable.items) return null;
    for (const category of data.skillsTable.items) {
      for (const broadSkill of category.items) {
        if (broadSkill.items && broadSkill.items.some(s => s.skill === specSkillName)) {
          return broadSkill.skill;
        }
      }
    }
    return null;
  }

  // Calculation of Budgets
  function recalculateBudgets() {
    syncSpeciesFreeSkills();

    const fact = FACTION_DATA[state.faction];
    if (fact && fact.apply) fact.apply(state);

    const heightenedCount = state.perks.filter(p => {
      const pName = typeof p === 'string' ? p : (p ? p.name : '');
      return pName && pName.toLowerCase().includes('heightened ability');
    }).length;
    const targetAbilityBudget = (state.faction === 'union_of_sol' ? 62 : 60) + heightenedCount;

    let abilityPtsSpent = 0;
    Object.values(state.abilities).forEach(val => abilityPtsSpent += (parseInt(val, 10) || 0));

    let baseSkillPoints = 70;
    if (state.faction === 'rigunmor' && state.rigunmorBonusChoice === 'points') {
      baseSkillPoints += 6;
    }

    let perkCost = 0;
    state.perks.forEach(p => {
      const { finalCost } = getPerkCost(p);
      perkCost += finalCost;
    });

    let flawBonus = 0;
    state.flaws.forEach(f => {
      const { rawBonus } = getFlawBonus(f);
      flawBonus += (rawBonus || 0);
    });

    let totalSkillBudget = baseSkillPoints - perkCost + flawBonus;

    let skillPtsSpent = 0;
    let totalAP = 0;
    let broadSkillCount = 0;
    let psionicBroadCount = 0;

    Object.entries(state.skills).forEach(([skillName, item]) => {
      if (item.ranks > 0) {
        let isFree = isSpeciesFreeBroad(skillName) || (state.faction === 'voidcorp' && (skillName.includes('Business') || skillName.includes('Negocios')));

        if (item.isBroad) {
          if (!isFree) {
            let favored = isFavored(skillName, item.category);
            let discount = 0;
            if (state.faction === 'orlamu' && state.profession === 'mindwalker' && item.category === 'Psionics') discount += 1;
            let baseCost = favored ? Math.max(1, item.standardCost - 1) : item.standardCost;
            let actualCost = Math.max(0, baseCost - discount);
            skillPtsSpent += actualCost;
            totalAP += item.standardCost;
            if (item.category !== 'Psionics') broadSkillCount++;
            else psionicBroadCount++;
          }
        } else {
          let parentBroadName = getParentBroadSkillName(skillName);
          let favored = isFavored(skillName, item.category, parentBroadName);
          let discount = 0;
          if (state.faction === 'rigunmor' && (skillName.includes('bargain') || skillName.includes('regatear'))) discount += 1;
          if (state.faction === 'orlamu' && state.profession === 'mindwalker' && item.category === 'Psionics') discount += 1;

          let baseCostPerRank = favored ? Math.max(1, item.standardCost - 1) : item.standardCost;
          let actualCostPerRank = Math.max(0, baseCostPerRank - discount);
          skillPtsSpent += actualCostPerRank * item.ranks;
          totalAP += item.standardCost * item.ranks;
        }
      }
    });

    let warnings = [];
    const limits = getEffectiveSpeciesLimits();
    const prof = PROFESSION_DATA[state.profession];

    Object.entries(state.abilities).forEach(([stat, val]) => {
      const [min, max] = limits[stat];
      if (val < min || val > max) {
        warnings.push(`${stat} (${val}) ${isEs ? 'fuera de límites de Especie' : 'out of Species bounds'} [${min}-${max}]`);
      }
    });

    if (prof && prof.reqs) {
      Object.entries(prof.reqs).forEach(([stat, minVal]) => {
        if (state.abilities[stat] < minVal) {
          warnings.push(`${stat} (${state.abilities[stat]}) ${isEs ? 'es inferior al mínimo de Profesión' : 'is below Profession min'} (${minVal})`);
        }
      });
    }

    if (abilityPtsSpent > targetAbilityBudget) warnings.push(isEs ? `Puntos de Característica excedidos (> ${targetAbilityBudget})` : `Ability Points exceeded (> ${targetAbilityBudget})`);
    if (skillPtsSpent > totalSkillBudget) warnings.push(isEs ? 'Puntos de Habilidad excedidos' : 'Skill Points exceeded');
    if (broadSkillCount > 5) warnings.push(isEs ? 'Máximo 5 Habilidades Generales excedido' : 'Max 5 Broad Skills exceeded');
    if (psionicBroadCount > (state.profession === 'mindwalker' ? 3 : 0)) {
      warnings.push(isEs ? 'Límite de Habilidades Psiónicas Generales excedido' : 'Psionic Broad Skills limit exceeded');
    }

    // Update Right Sidebar Tracked Choices
    const elTrackName = document.getElementById('cb-tracker-name');
    const elTrackFaction = document.getElementById('cb-tracker-faction');
    const elTrackSpecies = document.getElementById('cb-tracker-species');
    const elTrackBg = document.getElementById('cb-tracker-bg');
    const elTrackProf = document.getElementById('cb-tracker-prof');

    if (elTrackName) elTrackName.textContent = state.bio.name || '—';
    if (elTrackFaction) elTrackFaction.textContent = FACTION_DATA[state.faction]?.name || '—';
    if (elTrackSpecies) elTrackSpecies.textContent = SPECIES_DATA[state.species]?.name || '—';
    if (elTrackBg) elTrackBg.textContent = state.background || '—';
    if (elTrackProf) elTrackProf.textContent = PROFESSION_DATA[state.profession]?.name || '—';

    // Creation vs Campaign Mode Sidebar View Switch
    const elCreationWrap = document.getElementById('cb-creation-budget-wrap');
    const elCampaignWrap = document.getElementById('cb-campaign-budget-wrap');
    const elSidebarTitle = document.getElementById('cb-budget-sidebar-title');

    const spentAP = state.isFinalized ? calculateCampaignSpentAP() : 0;
    const availAP = (state.earnedAP || 0) - spentAP;
    const titleObj = getCharacterTitle(spentAP);

    if (state.isFinalized) {
      if (elCreationWrap) elCreationWrap.style.display = 'none';
      if (elCampaignWrap) elCampaignWrap.style.display = 'flex';
      if (elSidebarTitle) elSidebarTitle.textContent = isEs ? 'Avance de Campaña (XP)' : 'Campaign XP & AP';

      const inputSidebarEarned = document.getElementById('cb-sidebar-input-earned-ap');
      const elSidebarApSum = document.getElementById('cb-val-sidebar-ap-summary');
      const elSidebarRankTitle = document.getElementById('cb-val-sidebar-rank-title');

      if (inputSidebarEarned && document.activeElement !== inputSidebarEarned) {
        inputSidebarEarned.value = state.earnedAP || 0;
      }
      if (elSidebarApSum) {
        elSidebarApSum.textContent = `${availAP} ${isEs ? 'Disp.' : 'Avail'} / ${spentAP} ${isEs ? 'Gastados' : 'Spent'}`;
      }
      if (elSidebarRankTitle) {
        elSidebarRankTitle.textContent = `${titleObj.title} (${isEs ? 'Máx Rango' : 'Max Rank'}: ${titleObj.maxSkillRank})`;
      }
    } else {
      if (elCreationWrap) elCreationWrap.style.display = 'flex';
      if (elCampaignWrap) elCampaignWrap.style.display = 'none';
      if (elSidebarTitle) elSidebarTitle.textContent = isEs ? 'Resumen de Puntos' : 'Point Summary';

      const elAbility = document.getElementById('cb-val-ability-pts');
      const elSkill = document.getElementById('cb-val-skill-pts');
      const elTotalSum = document.getElementById('cb-ability-total-sum');

      if (elAbility) {
        elAbility.textContent = `${abilityPtsSpent} / ${targetAbilityBudget}`;
        elAbility.className = `cb-budget-val ${abilityPtsSpent === targetAbilityBudget ? 'valid' : (abilityPtsSpent > targetAbilityBudget ? 'over-limit' : '')}`;
      }

      if (elTotalSum) {
        elTotalSum.textContent = `${abilityPtsSpent} / ${targetAbilityBudget}`;
        elTotalSum.style.color = abilityPtsSpent === targetAbilityBudget ? '#a6c12e' : (abilityPtsSpent > targetAbilityBudget ? '#ff4d4d' : '#ffa500');
      }

      if (elSkill) {
        elSkill.textContent = `${totalSkillBudget - skillPtsSpent} / ${totalSkillBudget}`;
        elSkill.className = `cb-budget-val ${skillPtsSpent <= totalSkillBudget ? 'valid' : 'over-limit'}`;
      }
    }

    const elBadge = document.getElementById('cb-status-badge');
    const elBadgeText = document.getElementById('cb-status-text');

    if (elBadge && elBadgeText) {
      if (state.isFinalized) {
        elBadge.className = 'cb-status-badge badge-success';
        elBadgeText.textContent = `🛡️ ${isEs ? 'CAMPAÑA' : 'CAMPAIGN'} (${titleObj.title})`;
      } else if (warnings.length === 0 && abilityPtsSpent === targetAbilityBudget) {
        elBadge.className = 'cb-status-badge badge-success';
        elBadgeText.textContent = isEs ? 'VÁLIDO' : 'VALID';
      } else if (warnings.length > 0) {
        elBadge.className = 'cb-status-badge badge-warning';
        elBadgeText.textContent = warnings[0];
      } else {
        elBadge.className = 'cb-status-badge badge-warning';
        elBadgeText.textContent = isEs ? `ASIGNA ${targetAbilityBudget - abilityPtsSpent} PTS` : `ASSIGN ${targetAbilityBudget - abilityPtsSpent} PTS`;
      }
    }
    saveStateToLocalStorage();
  }

  // Render Step Content
  function renderStep(step) {
    state.step = step;
    saveStateToLocalStorage();
    document.querySelectorAll('.cb-step-btn').forEach(btn => {
      const btnStep = parseInt(btn.dataset.step);
      btn.classList.toggle('active', btnStep === step);
      btn.classList.toggle('completed', btnStep < step);
    });

    document.querySelectorAll('.cb-step-content').forEach(content => {
      content.style.display = 'none';
    });

    const activeContent = document.getElementById(`cb-step-${step}`);
    if (activeContent) activeContent.style.display = 'block';

    const btnPrev = document.getElementById('cb-btn-prev');
    const btnNext = document.getElementById('cb-btn-next');
    if (btnPrev) btnPrev.disabled = step === 1;
    if (btnNext) btnNext.style.display = step === 7 ? 'none' : 'inline-flex';

    if (step === 2) renderStep2();
    if (step === 3) renderStep3();
    if (step === 4) renderStep4();
    if (step === 5) renderStep5();
    if (step === 6) renderStep6();
    if (step === 7) renderStep7();

    const stepsWrapper = document.getElementById('cb-steps-wrapper');
    if (stepsWrapper) {
      stepsWrapper.scrollIntoView({ behavior: 'smooth', block: 'start' });
    } else {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  }

  // STEP 2: FACTION (STAR*DRIVE)
  function renderStep2() {
    const factGrid = document.getElementById('cb-faction-grid');
    if (factGrid) {
      factGrid.innerHTML = Object.values(FACTION_DATA).map(fact => `
        <div class="cb-card ${state.faction === fact.id ? 'selected' : ''}" data-faction="${fact.id}">
          <h4 class="cb-card-title">${fact.name}</h4>
          <p class="cb-card-desc">${fact.desc}</p>
          <div class="cb-card-meta">
            <strong>${isEs ? 'Beneficio de Juego' : 'Game Benefit'}:</strong> ${fact.bonus}
          </div>
        </div>
      `).join('');

      factGrid.querySelectorAll('.cb-card').forEach(card => {
        card.addEventListener('click', () => {
          state.faction = card.dataset.faction;
          renderStep2();
          recalculateBudgets();
        });
      });
    }
  }

  // STEP 3: SPECIES, BACKGROUND & PROFESSION
  function renderStep3() {
    // 1. Species Grid
    const specGrid = document.getElementById('cb-species-grid');
    if (specGrid) {
      const limits = getEffectiveSpeciesLimits();
      specGrid.innerHTML = Object.values(SPECIES_DATA).map(spec => `
        <div class="cb-card ${state.species === spec.id ? 'selected' : ''}" data-species="${spec.id}">
          <h4 class="cb-card-title">${spec.name}</h4>
          <p class="cb-card-desc">${spec.desc}</p>
          <div class="cb-card-meta">
            <strong>Limits:</strong> STR ${limits.STR.join('-')}, DEX ${limits.DEX.join('-')}, CON ${limits.CON.join('-')}, INT ${limits.INT.join('-')}, WIL ${limits.WIL.join('-')}, PER ${limits.PER.join('-')}
          </div>
        </div>
      `).join('');

      specGrid.querySelectorAll('.cb-card').forEach(card => {
        card.addEventListener('click', () => {
          state.species = card.dataset.species;
          const lim = getEffectiveSpeciesLimits();
          Object.keys(state.abilities).forEach(stat => {
            const [min, max] = lim[stat];
            if (state.abilities[stat] < min) state.abilities[stat] = min;
            if (state.abilities[stat] > max) state.abilities[stat] = max;
          });
          renderStep3();
          recalculateBudgets();
        });
      });
    }

    // 2. Background Grid (Safe array parsing)
    const bgGrid = document.getElementById('cb-background-grid');
    const bgItems = getBackgroundItems();
    if (bgGrid) {
      if (bgItems.length > 0) {
        bgGrid.innerHTML = bgItems.map(bg => {
          const favList = getBackgroundFavoredSkills(bg);
          return `
            <div class="cb-card ${state.background === bg.name ? 'selected' : ''}" data-bg="${bg.name}">
              <h4 class="cb-card-title">${bg.name}</h4>
              <p class="cb-card-desc">${bg.summary || bg.description || ''}</p>
              ${favList.length > 0 ? `<div class="cb-card-meta"><strong>${isEs ? 'Favorecidas' : 'Favored'}:</strong> ${favList.join(', ')}</div>` : ''}
            </div>
          `;
        }).join('');

        bgGrid.querySelectorAll('.cb-card').forEach(card => {
          card.addEventListener('click', () => {
            state.background = card.dataset.bg;
            renderStep3();
            recalculateBudgets();
          });
        });
      } else {
        bgGrid.innerHTML = `<p class="silver">${isEs ? 'No se encontraron antecedentes.' : 'No backgrounds available.'}</p>`;
      }
    }

    // 3. Profession Grid
    const profGrid = document.getElementById('cb-profession-grid');
    if (profGrid) {
      profGrid.innerHTML = Object.values(PROFESSION_DATA).map(prof => `
        <div class="cb-card ${state.profession === prof.id ? 'selected' : ''}" data-prof="${prof.id}">
          <h4 class="cb-card-title">${prof.name}</h4>
          <p class="cb-card-desc">${prof.desc}</p>
          <div class="cb-card-meta">
            <strong>${isEs ? 'Requisitos' : 'Requirements'}:</strong> ${Object.entries(prof.reqs).map(([k, v]) => `${k} ${v}`).join(', ')}
          </div>
        </div>
      `).join('');

      profGrid.querySelectorAll('.cb-card').forEach(card => {
        card.addEventListener('click', () => {
          state.profession = card.dataset.prof;
          renderStep3();
          recalculateBudgets();
        });
      });
    }
  }

  // STEP 4: ABILITY SCORES
  function renderStep4() {
    const grid = document.getElementById('cb-ability-grid');
    if (!grid) return;

    const limits = getEffectiveSpeciesLimits();
    const prof = PROFESSION_DATA[state.profession];

    grid.innerHTML = Object.keys(state.abilities).map(stat => {
      const baseScore = state.abilities[stat];
      const effScore = getEffectiveAbilityScore(stat);
      const [min, max] = limits[stat];
      const reqMin = prof && prof.reqs[stat] ? prof.reqs[stat] : null;
      let resMod = getResMod(effScore);

      if (state.faction === 'concord' && state.concordResModStat === stat) {
        resMod += 1;
      }

      const modText = resMod >= 0 ? `+${resMod}` : `${resMod}`;

      let bonusBadge = '';
      if (state.species === 'human' && state.faction === 'orion' && stat === 'PER') {
        bonusBadge = `<span class="cb-badge-free" style="margin-left:0.3rem; font-size: 0.7rem;">+1 Orión</span>`;
      } else if (state.species === 'human' && state.faction === 'borealis' && stat === 'INT') {
        bonusBadge = `<span class="cb-badge-free" style="margin-left:0.3rem; font-size: 0.7rem;">+1 Boreal</span>`;
      }

      return `
        <div class="cb-ability-card">
          <div class="cb-ability-header">
            <span class="cb-ability-name">${stat}${bonusBadge}</span>
            <span class="cb-ability-range">[${min} - ${max}]</span>
          </div>

          <div class="cb-ability-controls">
            <button class="cb-btn-score" data-stat="${stat}" data-dir="-1" ${baseScore <= min ? 'disabled' : ''}>-</button>
            <span class="cb-score-display">${effScore}</span>
            <button class="cb-btn-score" data-stat="${stat}" data-dir="1" ${baseScore >= max ? 'disabled' : ''}>+</button>
          </div>

          <div class="cb-res-modifier">
            <span>${isEs ? 'Mod. Resistencia' : 'Resistance Mod'}:</span>
            <span class="cb-res-tag">${modText}</span>
            ${reqMin ? `<span class="cb-req-tag">(Req: ${reqMin}+)</span>` : ''}
          </div>
        </div>
      `;
    }).join('');

    grid.querySelectorAll('.cb-btn-score').forEach(btn => {
      btn.addEventListener('click', () => {
        const stat = btn.dataset.stat;
        const dir = parseInt(btn.dataset.dir, 10);
        const curr = parseInt(state.abilities[stat], 10) || 10;
        state.abilities[stat] = curr + dir;
        saveStateToLocalStorage();
        renderStep4();
        recalculateBudgets();
      });
    });

    const resSummary = document.getElementById('cb-res-summary');
    if (resSummary) {
      resSummary.innerHTML = Object.keys(state.abilities).map(stat => {
        let mod = getResMod(getEffectiveAbilityScore(stat));
        if (state.faction === 'concord' && state.concordResModStat === stat) mod += 1;
        const modText = mod >= 0 ? `+${mod}` : `${mod}`;
        return `
          <div class="cb-res-card">
            <span class="cb-res-card-label">Res ${stat}</span>
            <span class="cb-res-card-val ${mod > 0 ? 'highlight' : ''}">${modText}</span>
          </div>
        `;
      }).join('');
    }

    const derivedSummary = document.getElementById('cb-derived-summary');
    if (derivedSummary) {
      const effDEX = getEffectiveAbilityScore('DEX');
      const effINT = getEffectiveAbilityScore('INT');
      const effCON = getEffectiveAbilityScore('CON');
      const effWIL = getEffectiveAbilityScore('WIL');
      const effSTR = getEffectiveAbilityScore('STR');

      const actionCheck = Math.floor((effDEX + effINT) / 2) + 1;
      const actionsPerRound = getActionsPerRound(effCON + effWIL);
      const mov = getMovementRates(effSTR + effDEX);

      derivedSummary.innerHTML = `
        <div class="cb-derived-card">
          <h4 class="cb-derived-title">${isEs ? 'Iniciativa y Acciones' : 'Initiative & Actions'}</h4>
          <div class="cb-track-box"><span>${isEs ? 'Chequeo de Acción (Iniciativa)' : 'Action Check Score (Initiative)'}</span><span class="cb-track-val">${actionCheck}</span></div>
          <div class="cb-track-box"><span>${isEs ? 'Acciones por Ronda' : 'Actions per Round'}</span><span class="cb-track-val">${actionsPerRound}</span></div>
        </div>
        <div class="cb-derived-card">
          <h4 class="cb-derived-title">${isEs ? 'Velocidad de Movimiento' : 'Movement Rates'}</h4>
          <div class="cb-track-box"><span>Sprint / Run / Walk</span><span class="cb-track-val">${mov.sprint}m / ${mov.run}m / ${mov.walk}m</span></div>
          <div class="cb-track-box"><span>Swim / Glide</span><span class="cb-track-val">${mov.swim}m / ${mov.glide}m</span></div>
        </div>
        <div class="cb-derived-card">
          <h4 class="cb-derived-title">${isEs ? 'Salud y Durabilidad' : 'Health & Durability'}</h4>
          <div class="cb-track-box"><span>Wounds / Stun</span><span class="cb-track-val">${effCON} / ${effCON}</span></div>
          <div class="cb-track-box"><span>Mortal / Fatigue</span><span class="cb-track-val">${Math.ceil(effCON / 2)} / ${Math.ceil(effCON / 2)}</span></div>
        </div>
      `;
    }
  }

  // STEP 5: PERKS & FLAWS
  function renderStep5() {
    const perksContainer = document.getElementById('cb-perks-list');
    const flawsContainer = document.getElementById('cb-flaws-list');

    if (!data.perksFlaws) return;

    const bgItems = getBackgroundItems();
    const currentBg = bgItems.find(b => b.name === state.background || b.id === state.background);
    const bgFlaw = getBackgroundFlaw(currentBg);
    const bgFavoredPerks = getBackgroundFavoredPerks(currentBg);

    const perksList = getPerksList();
    const flawsList = getFlawsList();

    // Ensure background flaw is included in state.flaws if present
    if (bgFlaw && !state.flaws.some(f => {
      const name = typeof f === 'string' ? f : f.name;
      return name.toLowerCase().includes(bgFlaw.toLowerCase()) || bgFlaw.toLowerCase().includes(name.toLowerCase());
    })) {
      state.flaws.push({ name: bgFlaw, level: 1 });
      saveStateToLocalStorage();
    }

    // 1. RENDER FLAWS (Top Section)
    if (flawsContainer) {
      flawsContainer.innerHTML = flawsList.map(f => {
        const isBgFlaw = bgFlaw && (f.name.toLowerCase().includes(bgFlaw.toLowerCase()) || bgFlaw.toLowerCase().includes(f.name.toLowerCase()));
        const stateFlaw = state.flaws.find(x => (typeof x === 'string' ? x : x.name) === f.name);
        const selected = !!stateFlaw || isBgFlaw;
        const currentLevel = isBgFlaw ? 1 : (stateFlaw ? (typeof stateFlaw === 'object' && stateFlaw.level ? stateFlaw.level : 1) : 0);

        const { options } = getFlawBonus(f);

        let levelButtonsHtml = '';
        if (isBgFlaw) {
          levelButtonsHtml = `<span class="cb-badge-free" style="background: rgba(255, 165, 0, 0.25); color: #ffa500; border-color: #ffa500;">🔒 ${isEs ? 'TRASFONDO (BLOQUEADO)' : 'BACKGROUND (LOCKED)'}</span>`;
        } else if (options.length > 1) {
          levelButtonsHtml = `
            <div class="cb-level-btn-group" style="display: flex; gap: 0.3rem; align-items: center; flex-wrap: wrap;">
              ${options.map((optVal, idx) => {
                const lvl = idx + 1;
                const active = currentLevel === lvl;
                return `
                  <button type="button" class="cb-btn-rank ${active ? 'active' : ''}" data-flaw="${f.name}" data-level="${lvl}">
                    Nvl ${lvl} (+${optVal} SP)
                  </button>
                `;
              }).join('')}
            </div>
          `;
        } else {
          const optVal = options[0] || 3;
          levelButtonsHtml = `
            <button type="button" class="cb-btn-rank ${selected ? 'active' : ''}" data-flaw="${f.name}" data-level="1" style="width: auto; padding: 0.2rem 0.6rem;">
              ${selected ? '✓' : '+'} (+${optVal} SP)
            </button>
          `;
        }

        return `
          <div class="cb-card ${selected ? 'selected' : ''} ${isBgFlaw ? 'cb-card-locked' : ''}" style="margin-bottom: 0.75rem; ${isBgFlaw ? 'border-color: #ffa500; background: rgba(255, 165, 0, 0.12);' : ''}">
            <div class="cb-card-header" style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem;">
              <h4 class="cb-card-title" style="font-size: 0.95rem; margin: 0; color: #ffffff;">${f.name}</h4>
              ${levelButtonsHtml}
            </div>
            <p class="cb-card-desc" style="font-size: 0.8rem; margin-top: 0.4rem;">${f.description || ''}</p>
          </div>
        `;
      }).join('');

      flawsContainer.querySelectorAll('.cb-btn-rank').forEach(btn => {
        btn.addEventListener('click', (e) => {
          e.stopPropagation();
          const flawName = btn.dataset.flaw;
          const lvl = parseInt(btn.dataset.level, 10);
          
          const isBg = bgFlaw && (flawName.toLowerCase().includes(bgFlaw.toLowerCase()) || bgFlaw.toLowerCase().includes(flawName.toLowerCase()));
          if (isBg) return;

          const existingIdx = state.flaws.findIndex(x => (typeof x === 'string' ? x : x.name) === flawName);

          if (existingIdx >= 0) {
            const currentObj = state.flaws[existingIdx];
            const currLvl = typeof currentObj === 'object' && currentObj.level ? currentObj.level : 1;

            if (currLvl === lvl) {
              state.flaws.splice(existingIdx, 1);
            } else {
              state.flaws[existingIdx] = { name: flawName, level: lvl };
            }
          } else {
            const userFlawsCount = state.flaws.filter(x => {
              const name = typeof x === 'string' ? x : x.name;
              return !bgFlaw || (!name.toLowerCase().includes(bgFlaw.toLowerCase()) && !bgFlaw.toLowerCase().includes(name.toLowerCase()));
            }).length;

            if (userFlawsCount < 3) {
              state.flaws.push({ name: flawName, level: lvl });
            }
          }

          saveStateToLocalStorage();
          renderStep5();
          recalculateBudgets();
        });
      });
    }

    // 2. RENDER PERKS (Bottom Section)
    if (perksContainer) {
      perksContainer.innerHTML = perksList.map(p => {
        const statePerk = state.perks.find(x => (typeof x === 'string' ? x : x.name) === p.name);
        const selected = !!statePerk;
        const currentLevel = statePerk ? (typeof statePerk === 'object' && statePerk.level ? statePerk.level : 1) : 0;

        const { options, favored } = getPerkCost(p);

        let levelButtonsHtml = '';
        if (options.length > 1) {
          levelButtonsHtml = `
            <div style="display: flex; gap: 0.3rem; align-items: center; flex-wrap: wrap;">
              ${favored ? `<span class="cb-badge-favored">${isEs ? 'FAVORECIDA' : 'FAVORED'}</span>` : ''}
              <div class="cb-level-btn-group" style="display: flex; gap: 0.3rem;">
                ${options.map((optVal, idx) => {
                  const lvl = idx + 1;
                  const active = currentLevel === lvl;
                  const optCost = favored ? Math.max(1, optVal - 1) : optVal;
                  return `
                    <button type="button" class="cb-btn-rank ${active ? 'active' : ''}" data-perk="${p.name}" data-level="${lvl}">
                      Nvl ${lvl} (${optCost} SP)
                    </button>
                  `;
                }).join('')}
              </div>
            </div>
          `;
        } else {
          const optVal = options[0] || 3;
          const optCost = favored ? Math.max(1, optVal - 1) : optVal;
          levelButtonsHtml = `
            <div style="display: flex; gap: 0.3rem; align-items: center;">
              ${favored ? `<span class="cb-badge-favored">${isEs ? 'FAVORECIDA' : 'FAVORED'}</span>` : ''}
              <button type="button" class="cb-btn-rank ${selected ? 'active' : ''}" data-perk="${p.name}" data-level="1" style="width: auto; padding: 0.2rem 0.6rem;">
                ${selected ? '✓' : '+'} (${optCost} SP)
              </button>
            </div>
          `;
        }

        return `
          <div class="cb-card ${selected ? 'selected' : ''}" style="margin-bottom: 0.75rem;">
            <div class="cb-card-header" style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem;">
              <h4 class="cb-card-title" style="font-size: 0.95rem; margin: 0; color: #ffffff;">${p.name}</h4>
              ${levelButtonsHtml}
            </div>
            <p class="cb-card-desc" style="font-size: 0.8rem; margin-top: 0.4rem;">${p.description || ''}</p>
          </div>
        `;
      }).join('');

      perksContainer.querySelectorAll('.cb-btn-rank').forEach(btn => {
        btn.addEventListener('click', (e) => {
          e.stopPropagation();
          const perkName = btn.dataset.perk;
          const lvl = parseInt(btn.dataset.level, 10);

          const existingIdx = state.perks.findIndex(x => (typeof x === 'string' ? x : x.name) === perkName);

          if (existingIdx >= 0) {
            const currentObj = state.perks[existingIdx];
            const currLvl = typeof currentObj === 'object' && currentObj.level ? currentObj.level : 1;

            if (currLvl === lvl) {
              state.perks.splice(existingIdx, 1);
            } else {
              state.perks[existingIdx] = { name: perkName, level: lvl };
            }
          } else {
            if (state.perks.length < 3) {
              state.perks.push({ name: perkName, level: lvl });
            }
          }

          saveStateToLocalStorage();
          renderStep5();
          recalculateBudgets();
        });
      });
    }
  }

  // STEP 6: SKILLS
  function renderStep6() {
    const listEl = document.getElementById('cb-skills-list');
    if (!listEl || !data.skillsTable || !data.skillsTable.items) return;

    const searchTerm = (document.getElementById('cb-skill-search')?.value || '').toLowerCase();
    const catFilter = document.getElementById('cb-skill-category-filter')?.value || 'ALL';
    const favoredOnly = document.getElementById('cb-skill-favored-only')?.checked || false;

    let html = '';

    data.skillsTable.items.forEach(category => {
      if (catFilter !== 'ALL' && category.skill !== catFilter) return;

      category.items.forEach(broadSkill => {
        let isFreeBroad = isSpeciesFreeBroad(broadSkill) || (state.faction === 'voidcorp' && (broadSkill.skill.includes('Business') || broadSkill.skill.includes('Negocios')));
        let broadFavored = isFavored(broadSkill.skill, category.skill);
        let broadBought = state.skills[broadSkill.skill]?.ranks > 0 || isFreeBroad;

        if (favoredOnly && !broadFavored) return;

        let matchesSearch = broadSkill.skill.toLowerCase().includes(searchTerm);
        let childMatches = broadSkill.items && broadSkill.items.some(s => s.skill.toLowerCase().includes(searchTerm));
        if (searchTerm && !matchesSearch && !childMatches) return;

        let discount = 0;
        if (state.faction === 'orlamu' && state.profession === 'mindwalker' && category.skill === 'Psionics') discount += 1;

        let baseBroadCost = broadFavored ? Math.max(1, broadSkill.cost - 1) : broadSkill.cost;
        let actualBroadCost = isFreeBroad ? 0 : Math.max(0, baseBroadCost - discount);
        let broadAbilityVal = state.abilities[broadSkill.attribute] || 10;
        let broadOrd = broadAbilityVal;
        let broadGood = Math.floor(broadOrd / 2);
        let broadAmaz = Math.floor(broadOrd / 4);

        let broadTotalSpent = broadBought ? (isFreeBroad ? 0 : actualBroadCost) : 0;

        html += `
          <div class="cb-skill-row broad ${broadFavored ? 'favored' : ''}">
            <div class="cb-skill-info">
              <span class="cb-skill-title">
                ${broadSkill.skill}
                ${isFreeBroad ? `<span class="cb-badge-free">${isEs ? 'ESPECIE (GRATIS)' : 'SPECIES (FREE)'}</span>` : ''}
                ${broadFavored ? `<span class="cb-badge-favored">${isEs ? 'FAVORECIDA' : 'FAVORED'}</span>` : ''}
              </span>
              <span class="cb-skill-meta">
                <span>[${broadSkill.attribute}: ${broadAbilityVal}]</span>
                <span>${isEs ? 'Objetivo' : 'Target'}: <strong>${broadOrd} / ${broadGood} / ${broadAmaz}</strong></span>
                <span>${isEs ? 'Coste' : 'Cost'}: ${isFreeBroad ? (isEs ? '0 SP (Gratis)' : '0 SP (Free)') : `${actualBroadCost} SP`}</span>
                <span style="color: var(--accent-cyan); font-weight: bold;">${isEs ? 'Total' : 'Total'}: <strong>${broadTotalSpent} SP</strong></span>
              </span>
            </div>
            <div class="cb-rank-controls">
              <span class="cb-skill-total-badge ${broadTotalSpent > 0 ? 'active' : ''}">${broadTotalSpent} SP</span>
              <button class="cb-btn-rank ${broadBought ? 'active' : ''}" data-skill="${broadSkill.skill}" data-is-broad="true" data-cost="${broadSkill.cost}" data-cat="${category.skill}" ${isFreeBroad ? 'disabled title="Free Species Skill"' : ''}>
                ${broadBought ? '✓' : '+'}
              </button>
            </div>
          </div>
        `;

        let hasChildBought = broadSkill.items && broadSkill.items.some(specSkill => state.skills[specSkill.skill]?.ranks > 0);

        if ((broadBought || hasChildBought) && broadSkill.items) {
          broadSkill.items.forEach(specSkill => {
            if (searchTerm && !specSkill.skill.toLowerCase().includes(searchTerm) && !matchesSearch) return;

            let specFavored = isFavored(specSkill.skill, category.skill, broadSkill.skill);
            let currentRanks = state.skills[specSkill.skill]?.ranks || 0;

            let specDiscount = 0;
            if (state.faction === 'rigunmor' && (specSkill.skill.includes('bargain') || specSkill.skill.includes('regatear'))) specDiscount += 1;
            if (state.faction === 'orlamu' && state.profession === 'mindwalker' && category.skill === 'Psionics') specDiscount += 1;

            let baseSpecCost = specFavored ? Math.max(1, specSkill.cost - 1) : specSkill.cost;
            let actualSpecCost = Math.max(0, baseSpecCost - specDiscount);
            let specTotalSpent = actualSpecCost * currentRanks;
            let totalSpecScore = broadAbilityVal + currentRanks;
            let specOrd = totalSpecScore;
            let specGood = Math.floor(specOrd / 2);
            let specAmaz = Math.floor(specOrd / 4);

            html += `
              <div class="cb-skill-row ${specFavored ? 'favored' : ''}" style="padding-left: 2.5rem;">
                <div class="cb-skill-info">
                  <span class="cb-skill-title">
                    › ${specSkill.skill}
                    ${specFavored ? `<span class="cb-badge-favored">${isEs ? 'FAVORECIDA' : 'FAVORED'}</span>` : ''}
                  </span>
                  <span class="cb-skill-meta">
                    <span>${isEs ? 'Rangos' : 'Ranks'}: +${currentRanks}</span>
                    <span>${isEs ? 'Puntuación Total' : 'Total Score'}: <strong>${totalSpecScore}</strong></span>
                    <span>${isEs ? 'Objetivo' : 'Target'}: <strong>${specOrd} / ${specGood} / ${specAmaz}</strong></span>
                    <span style="color: #a6c12e; font-weight: bold;">${getRankBenefitDescription(currentRanks)}</span>
                    <span>${isEs ? 'Precio' : 'Cost'}: ${actualSpecCost} SP/rank</span>
                    <span style="color: var(--accent-cyan); font-weight: bold;">${isEs ? 'Total' : 'Total'}: <strong>${specTotalSpent} SP</strong></span>
                  </span>
                </div>
                <div class="cb-rank-controls">
                  <span class="cb-skill-total-badge ${specTotalSpent > 0 ? 'active' : ''}">${specTotalSpent} SP</span>
                  ${[0, 1, 2, 3].map(r => `
                    <button class="cb-btn-rank ${currentRanks === r ? 'active' : ''}" data-skill="${specSkill.skill}" data-rank="${r}" data-cost="${specSkill.cost}" data-cat="${category.skill}">
                      ${r}
                    </button>
                  `).join('')}
                </div>
              </div>
            `;
          });
        }
      });
    });

    listEl.innerHTML = html;

    listEl.querySelectorAll('.cb-btn-rank').forEach(btn => {
      btn.addEventListener('click', () => {
        const skillName = btn.dataset.skill;
        const isBroad = btn.dataset.isBroad === 'true';
        const cost = parseInt(btn.dataset.cost);
        const cat = btn.dataset.cat;

        if (isBroad) {
          const currentlyBought = state.skills[skillName]?.ranks > 0;
          if (currentlyBought) {
            delete state.skills[skillName];
          } else {
            state.skills[skillName] = { ranks: 1, isBroad: true, standardCost: cost, category: cat };
          }
        } else {
          const rank = parseInt(btn.dataset.rank);
          if (rank === 0) {
            delete state.skills[skillName];
          } else {
            state.skills[skillName] = { ranks: rank, isBroad: false, standardCost: cost, category: cat };
          }
        }

        renderStep6();
        recalculateBudgets();
      });
    });
  }

  // STEP 7: SHEET & EXPORT
  function renderStep7() {
    const container = document.getElementById('cb-character-sheet-container');
    if (!container) return;

    const faction = FACTION_DATA[state.faction];
    const species = SPECIES_DATA[state.species];
    const prof = PROFESSION_DATA[state.profession];
    const actionCheck = Math.floor((getEffectiveAbilityScore('DEX') + getEffectiveAbilityScore('INT')) / 2) + 1;
    const actionsPerRound = getActionsPerRound(getEffectiveAbilityScore('CON') + getEffectiveAbilityScore('WIL'));
    const mov = getMovementRates(getEffectiveAbilityScore('STR') + getEffectiveAbilityScore('DEX'));

    // Build character sheet skill table
    let skillRowsHtml = '';
    const purchasedSkills = state.skills;
    const broadList = [];

    if (data.skillsTable && data.skillsTable.items) {
      data.skillsTable.items.forEach(cat => {
        cat.items.forEach(broad => {
          const isBroadBought = purchasedSkills[broad.skill]?.ranks > 0;
          const hasSpecBought = broad.items && broad.items.some(s => purchasedSkills[s.skill]?.ranks > 0);
          if (isBroadBought || hasSpecBought) {
            broadList.push(broad);
          }
        });
      });
    }

    if (broadList.length === 0) {
      skillRowsHtml = `<tr><td colspan="7" style="text-align:center; padding:1.5rem; color:#8099AC;">${isEs ? 'No se han seleccionado habilidades.' : 'No skills trained yet.'}</td></tr>`;
    } else {
      broadList.forEach(broad => {
        const broadInfo = purchasedSkills[broad.skill];
        const att = broad.attribute || 'INT';
        const abilityScore = getEffectiveAbilityScore(att);
        const broadOrd = abilityScore;
        const broadGood = Math.floor(broadOrd / 2);
        const broadAmaz = Math.floor(broadOrd / 4);

        skillRowsHtml += `
          <tr class="broad-row">
            <td><strong>${broad.skill}</strong></td>
            <td class="tc"><strong>${att}</strong></td>
            <td class="tc"><strong>${abilityScore}</strong></td>
            <td class="tc">${broadInfo ? 'Broad' : '-'}</td>
            <td class="tc"><strong>${broadOrd}</strong></td>
            <td class="tc" style="font-size: 0.78rem; color: #a6c12e;">${isEs ? 'Habilidad General (Base)' : 'Broad Skill (Base)'}</td>
            <td class="tc cb-target-scores">${broadOrd} / ${broadGood} / ${broadAmaz}</td>
          </tr>
        `;

        if (broad.items) {
          broad.items.forEach(spec => {
            if (purchasedSkills[spec.skill] && !purchasedSkills[spec.skill].isBroad) {
              const specInfo = purchasedSkills[spec.skill];
              const ranks = specInfo.ranks || 0;
              const totalScore = abilityScore + ranks;
              const ord = totalScore;
              const good = Math.floor(ord / 2);
              const amaz = Math.floor(ord / 4);

              skillRowsHtml += `
                <tr class="spec-row">
                  <td>› ${spec.skill}</td>
                  <td class="tc">${att}</td>
                  <td class="tc">${abilityScore}</td>
                  <td class="tc">+${ranks}</td>
                  <td class="tc"><strong>${totalScore}</strong></td>
                  <td class="tc" style="font-size: 0.78rem; color: #a6c12e;">${getRankBenefitDescription(ranks)}</td>
                  <td class="tc cb-target-scores">${ord} / ${good} / ${amaz}</td>
                </tr>
              `;
            }
          });
        }
      });
    }

    // Perks and Flaws formatting
    const formattedPerks = [...species.freePerks, ...state.perks].map(p => typeof p === 'string' ? p : `${p.name}${p.level ? ` (Nvl ${p.level})` : ''}`).join(', ');
    const formattedFlaws = state.flaws.map(f => typeof f === 'string' ? f : `${f.name}${f.level ? ` (Nvl ${f.level})` : ''}`).join(', ');

    const spentAP = state.isFinalized ? calculateCampaignSpentAP() : 0;
    const availableAP = (state.earnedAP || 0) - spentAP;
    const titleObj = getCharacterTitle(spentAP);

    let advancementBannerHtml = '';
    if (!state.isFinalized) {
      advancementBannerHtml = `
        <div class="cb-sheet-section mb4" style="background: rgba(10, 61, 84, 0.4); border: 2px solid var(--accent-cyan); text-align: center; padding: 1.25rem;">
          <h3 class="neon-cyan" style="margin-top: 0;">${isEs ? '¿Personaje Listo para la Aventura?' : 'Ready for Campaign Play?'}</h3>
          <p class="silver mb3" style="font-size: 0.85rem;">${isEs ? 'Al finalizar la creación, el personaje pasará al modo de Avance de Campaña a 0 PA (Novato). Podrás otorgar Puntos de Avance (PA) para entrenar habilidades y mejorar características.' : 'Finalizing locks creation baseline at 0 AP (Rookie). You can then award Advancement Points (AP) during campaign play to train skills and improve scores.'}</p>
          <button type="button" class="cb-btn cb-btn-primary" id="cb-btn-finalize-creation">
            <span>🛡️</span> <span>${isEs ? 'Finalizar Creación e Iniciar Avance de Campaña' : 'Finalize Character & Begin Campaign'}</span>
          </button>
        </div>
      `;
    } else {
      advancementBannerHtml = `
        <div class="cb-sheet-section mb4" style="background: rgba(16, 37, 66, 0.7); border: 2px solid #a6c12e; padding: 1.25rem;">
          <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; margin-bottom: 1rem;">
            <div>
              <span class="cb-badge-free" style="background: rgba(166, 193, 46, 0.25); color: #a6c12e; border-color: #a6c12e; font-size: 0.8rem; padding: 0.2rem 0.6rem;">
                🛡️ ${isEs ? 'MODO AVANCE DE CAMPAÑA' : 'CAMPAIGN ADVANCEMENT MODE'}
              </span>
              <h3 class="neon-cyan" style="margin: 0.4rem 0 0 0;">${isEs ? 'Título:' : 'Title:'} ${titleObj.title} (${spentAP} PA ${isEs ? 'Gastados' : 'Spent'})</h3>
              <div class="silver f6" style="margin-top: 0.2rem;">
                ${isEs ? 'Máx. Rango Habilidad:' : 'Max Skill Rank:'} <strong>${titleObj.maxSkillRank}</strong> | ${isEs ? 'Máx. Habilidades Generales:' : 'Max Broad Skills:'} <strong>${titleObj.maxBroad}</strong>
              </div>
            </div>
            <button type="button" class="cb-btn cb-btn-secondary" id="cb-btn-unfinalize" style="font-size: 0.8rem;">
              <span>🔓</span> <span>${isEs ? 'Editar Creación Inicial' : 'Edit Starting Character'}</span>
            </button>
          </div>

          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; background: rgba(0,0,0,0.3); padding: 1rem; border-radius: 6px; align-items: center;" class="mb3">
            <div>
              <label style="display: block; font-size: 0.75rem; color: #8099AC; margin-bottom: 0.3rem;">${isEs ? 'PA Otorgados por DJ' : 'Earned AP (GM Awarded)'}:</label>
              <div style="display: flex; gap: 0.4rem; align-items: center;">
                <input type="number" id="cb-input-earned-ap" class="cb-input" value="${state.earnedAP || 0}" min="0" style="width: 80px; text-align: center; padding: 0.3rem;">
                <button type="button" class="cb-btn-score" id="cb-btn-add-5ap" style="width: auto; padding: 0.3rem 0.6rem; font-size: 0.75rem;">+5 PA</button>
                <button type="button" class="cb-btn-score" id="cb-btn-add-10ap" style="width: auto; padding: 0.3rem 0.6rem; font-size: 0.75rem;">+10 PA</button>
              </div>
            </div>
            <div>
              <span style="display:block; font-size: 0.75rem; color: #8099AC;">${isEs ? 'PA Gastados' : 'Spent AP'}:</span>
              <span style="font-size: 1.3rem; font-family: 'Michroma', sans-serif; color: #a6c12e;">${spentAP} PA</span>
            </div>
            <div>
              <span style="display:block; font-size: 0.75rem; color: #8099AC;">${isEs ? 'PA Disponibles' : 'Available AP'}:</span>
              <span style="font-size: 1.3rem; font-family: 'Michroma', sans-serif; color: ${availableAP >= 0 ? 'var(--accent-cyan)' : '#ff4d4d'};">${availableAP} PA</span>
            </div>
          </div>
        </div>
      `;
    }

    container.innerHTML = `
      <div class="cb-sheet">
        <div class="cb-sheet-header">
          <div>
            <h2 class="cb-sheet-title">${state.bio.name || (isEs ? 'Personaje Sin Nombre' : 'Unnamed Character')}</h2>
            <div class="silver f6 mt1">
              <strong>${faction ? faction.name : ''}</strong> | <strong>${species.name}</strong> | <strong>${prof ? prof.name : ''}</strong> | ${state.bio.concept || ''}
            </div>
          </div>
          <button class="cb-btn cb-btn-primary" onclick="window.print()">
            <span>🖨</span> <span>${isEs ? 'Imprimir Hoja' : 'Print Sheet'}</span>
          </button>
        </div>

        ${advancementBannerHtml}

        <div class="cb-sheet-grid">
          <!-- Primary Ability Scores -->
          <div class="cb-sheet-section">
            <h3 class="cb-sheet-sec-title">${isEs ? 'Características' : 'Ability Scores'}</h3>
            ${Object.keys(state.abilities).map(stat => {
              const effVal = getEffectiveAbilityScore(stat);
              let mod = getResMod(effVal);
              if (state.faction === 'concord' && state.concordResModStat === stat) mod += 1;
              return `
                <div class="cb-track-box">
                  <span><strong>${stat}:</strong> ${effVal}</span>
                  <span class="cb-track-val">Res: ${mod >= 0 ? '+' : ''}${mod}</span>
                </div>
              `;
            }).join('')}
          </div>

          <!-- Combat & Secondary Stats -->
          <div class="cb-sheet-section">
            <h3 class="cb-sheet-sec-title">${isEs ? 'Estadísticas Secundarias' : 'Secondary Stats'}</h3>
            <div class="cb-track-box">
              <span>${isEs ? 'Chequeo de Acción' : 'Action Check Score'}</span>
              <span class="cb-track-val">${actionCheck}</span>
            </div>
            <div class="cb-track-box">
              <span>${isEs ? 'Acciones por Ronda' : 'Actions per Round'}</span>
              <span class="cb-track-val">${actionsPerRound}</span>
            </div>
            
            <h4 class="neon-cyan f6 mt3 mb2">${isEs ? 'Salud y Durabilidad' : 'Durability / Health'}</h4>
            <div class="cb-track-box">
              <span>Wounds / Stun</span>
              <span class="cb-track-val">${getEffectiveAbilityScore('CON')}</span>
            </div>
            <div class="cb-track-box">
              <span>Mortal / Fatigue</span>
              <span class="cb-track-val">${Math.ceil(getEffectiveAbilityScore('CON') / 2)}</span>
            </div>
          </div>

          <!-- Movement Rates -->
          <div class="cb-sheet-section">
            <h3 class="cb-sheet-sec-title">${isEs ? 'Velocidad de Movimiento' : 'Movement Rates'}</h3>
            <div class="cb-track-box"><span>Sprint</span><span class="cb-track-val">${mov.sprint} m</span></div>
            <div class="cb-track-box"><span>Run</span><span class="cb-track-val">${mov.run} m</span></div>
            <div class="cb-track-box"><span>Walk</span><span class="cb-track-val">${mov.walk} m</span></div>
            <div class="cb-track-box"><span>Swim</span><span class="cb-track-val">${mov.swim} m</span></div>
            <div class="cb-track-box"><span>Glide</span><span class="cb-track-val">${mov.glide} m</span></div>
          </div>
        </div>

        <!-- Trained Skills Table (Character Sheet Structure) -->
        <div class="cb-sheet-section mb4">
          <h3 class="cb-sheet-sec-title">${isEs ? 'Habilidades Entrenadas' : 'Trained Skills'}</h3>
          <div style="overflow-x: auto;">
            <table class="cb-sheet-skill-table">
              <thead>
                <tr>
                  <th>${isEs ? 'Habilidad' : 'Skill Name'}</th>
                  <th class="tc">${isEs ? 'Atrib.' : 'Att'}</th>
                  <th class="tc">${isEs ? 'Base' : 'Base'}</th>
                  <th class="tc">${isEs ? 'Rangos' : 'Ranks'}</th>
                  <th class="tc">${isEs ? 'Puntuación Total' : 'Total Score'}</th>
                  <th class="tc">${isEs ? 'Beneficios de Rango' : 'Rank Benefits'}</th>
                  <th class="tc">${isEs ? 'Objetivo (Ord / Bu / As)' : 'Target (Ord / Good / Amaz)'}</th>
                </tr>
              </thead>
              <tbody>
                ${skillRowsHtml}
              </tbody>
            </table>
          </div>
        </div>

        <!-- Perks, Flaws & Faction Summary -->
        <div class="cb-sheet-section">
          <h3 class="cb-sheet-sec-title">${isEs ? 'Beneficios de Facción, Ventajas y Defectos' : 'Faction Benefits, Perks & Flaws'}</h3>
          <p><strong>${isEs ? 'Facción' : 'Faction'}:</strong> ${faction ? faction.name : ''}</p>
          <p><em>${faction ? faction.bonus : ''}</em></p>
          <p class="mt2"><strong>Perks:</strong> ${formattedPerks || (isEs ? 'Ninguna' : 'None')}</p>
          <p><strong>Flaws:</strong> ${formattedFlaws || (isEs ? 'Ninguno' : 'None')}</p>
        </div>
      </div>
    `;

    // Attach listeners for campaign advancement
    document.getElementById('cb-btn-finalize-creation')?.addEventListener('click', () => {
      state.isFinalized = true;
      saveStateToLocalStorage();
      renderStep7();
      recalculateBudgets();
    });

    document.getElementById('cb-btn-unfinalize')?.addEventListener('click', () => {
      if (confirm(isEs ? '¿Volver al modo de edición de creación?' : 'Return to character creation mode?')) {
        state.isFinalized = false;
        saveStateToLocalStorage();
        renderStep7();
        recalculateBudgets();
      }
    });

    const inputEarned = document.getElementById('cb-input-earned-ap');
    inputEarned?.addEventListener('change', e => {
      state.earnedAP = Math.max(0, parseInt(e.target.value, 10) || 0);
      saveStateToLocalStorage();
      renderStep7();
      recalculateBudgets();
    });

    document.getElementById('cb-btn-add-5ap')?.addEventListener('click', () => {
      state.earnedAP = (state.earnedAP || 0) + 5;
      saveStateToLocalStorage();
      renderStep7();
      recalculateBudgets();
    });

    document.getElementById('cb-btn-add-10ap')?.addEventListener('click', () => {
      state.earnedAP = (state.earnedAP || 0) + 10;
      saveStateToLocalStorage();
      renderStep7();
      recalculateBudgets();
    });
  }

  // Sidebar XP / Advancement Event Listeners
  const inputSidebarEarned = document.getElementById('cb-sidebar-input-earned-ap');
  inputSidebarEarned?.addEventListener('change', e => {
    state.earnedAP = Math.max(0, parseInt(e.target.value, 10) || 0);
    saveStateToLocalStorage();
    recalculateBudgets();
    if (state.step === 7) renderStep7();
  });

  document.getElementById('cb-sidebar-btn-add-1ap')?.addEventListener('click', () => {
    state.earnedAP = (state.earnedAP || 0) + 1;
    saveStateToLocalStorage();
    recalculateBudgets();
    if (state.step === 7) renderStep7();
  });

  document.getElementById('cb-sidebar-btn-add-5ap')?.addEventListener('click', () => {
    state.earnedAP = (state.earnedAP || 0) + 5;
    saveStateToLocalStorage();
    recalculateBudgets();
    if (state.step === 7) renderStep7();
  });

  document.getElementById('cb-sidebar-btn-add-10ap')?.addEventListener('click', () => {
    state.earnedAP = (state.earnedAP || 0) + 10;
    saveStateToLocalStorage();
    recalculateBudgets();
    if (state.step === 7) renderStep7();
  });

  // Attach Event Listeners
  document.getElementById('cb-input-name')?.addEventListener('input', e => { state.bio.name = e.target.value; saveStateToLocalStorage(); });
  document.getElementById('cb-input-player')?.addEventListener('input', e => { state.bio.player = e.target.value; saveStateToLocalStorage(); });
  document.getElementById('cb-input-concept')?.addEventListener('input', e => { state.bio.concept = e.target.value; saveStateToLocalStorage(); });
  document.getElementById('cb-input-motivation')?.addEventListener('input', e => { state.bio.motivation = e.target.value; saveStateToLocalStorage(); });
  document.getElementById('cb-input-attitude')?.addEventListener('input', e => { state.bio.attitude = e.target.value; saveStateToLocalStorage(); });
  document.getElementById('cb-input-traits')?.addEventListener('input', e => { state.bio.traits = e.target.value; saveStateToLocalStorage(); });

  document.getElementById('cb-skill-search')?.addEventListener('input', renderStep5);
  document.getElementById('cb-skill-category-filter')?.addEventListener('change', renderStep5);
  document.getElementById('cb-skill-favored-only')?.addEventListener('change', renderStep5);

  document.querySelectorAll('.cb-step-btn').forEach(btn => {
    btn.addEventListener('click', () => renderStep(parseInt(btn.dataset.step)));
  });

  document.getElementById('cb-btn-prev')?.addEventListener('click', () => {
    if (state.step > 1) renderStep(state.step - 1);
  });

  document.getElementById('cb-btn-next')?.addEventListener('click', () => {
    if (state.step < 7) renderStep(state.step + 1);
  });

  // Export JSON
  document.getElementById('cb-btn-export-json')?.addEventListener('click', () => {
    const jsonStr = JSON.stringify(state, null, 2);
    const blob = new Blob([jsonStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${state.bio.name || 'character'}_alternity.json`;
    a.click();
    URL.revokeObjectURL(url);
  });

  // Import JSON
  const importInput = document.getElementById('cb-input-import-json');
  document.getElementById('cb-btn-import-json')?.addEventListener('click', () => importInput?.click());

  importInput?.addEventListener('change', e => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = evt => {
      try {
        const loadedState = JSON.parse(evt.target.result);
        Object.assign(state, loadedState);
        saveStateToLocalStorage();
        renderStep(state.step || 1);
        recalculateBudgets();
        alert(isEs ? '¡Personaje cargado con éxito!' : 'Character loaded successfully!');
      } catch (err) {
        alert(isEs ? 'Error al leer el archivo JSON' : 'Invalid JSON file');
      }
    };
    reader.readAsText(file);
  });

  // Reset Button
  document.getElementById('cb-btn-reset')?.addEventListener('click', () => {
    if (confirm(isEs ? '¿Estás seguro de reiniciar la creación?' : 'Reset character creation?')) {
      try { localStorage.removeItem(STORAGE_KEY); } catch(e){}
      state.step = 1;
      state.bio = { name: '', player: '', concept: '', motivation: '', attitude: '', traits: '' };
      state.faction = 'concord';
      state.species = 'human';
      state.background = null;
      state.profession = 'combat-spec';
      state.abilities = { STR: 10, DEX: 10, CON: 10, INT: 10, WIL: 10, PER: 10 };
      state.skills = {};
      state.perks = [];
      state.flaws = [];

      ['cb-input-name', 'cb-input-player', 'cb-input-concept', 'cb-input-motivation', 'cb-input-attitude', 'cb-input-traits'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.value = '';
      });

      renderStep(1);
      recalculateBudgets();
    }
  });

  // Initial Initialization
  loadStateFromLocalStorage();
  renderStep(state.step || 1);
  recalculateBudgets();
});

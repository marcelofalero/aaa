/**
 * Stardrive RPG Character Engine (Headless Data Plane Library)
 * UMD module for Node.js scripts, CLI validation, unit tests, and browser UI.
 */
(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define([], factory);
  } else if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.CharacterEngine = factory();
  }
}(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  // Canonical Species Ability Bounds
  const SPECIES_LIMITS = {
    human:    { STR: [4, 14], DEX: [4, 14], CON: [4, 14], INT: [4, 14], WIL: [4, 14], PER: [4, 14] },
    fraal:    { STR: [3, 12], DEX: [4, 14], CON: [3, 12], INT: [7, 17], WIL: [7, 17], PER: [5, 15] },
    mechalus: { STR: [5, 15], DEX: [4, 14], CON: [5, 15], INT: [7, 17], WIL: [3, 12], PER: [3, 12] },
    sesheyan: { STR: [3, 12], DEX: [5, 15], CON: [4, 14], INT: [3, 12], WIL: [5, 15], PER: [3, 12] },
    tsa:      { STR: [3, 12], DEX: [7, 17], CON: [3, 12], INT: [5, 15], WIL: [4, 14], PER: [5, 15] },
    weren:    { STR: [7, 17], DEX: [3, 12], CON: [7, 17], INT: [3, 12], WIL: [3, 12], PER: [3, 12] }
  };

  // Canonical Species Free Broads Slugs
  const SPECIES_FREE_BROAD_SLUGS = {
    human: ['athletics', 'vehicle-operation', 'stamina', 'knowledge', 'awareness', 'interaction'],
    fraal: ['awareness', 'resolve', 'vehicle-operation', 'knowledge', 'interaction', 'telepathy'],
    mechalus: ['athletics', 'vehicle-operation', 'stamina', 'knowledge', 'awareness', 'computer-science'],
    sesheyan: ['melee-combat', 'acrobatics', 'stamina', 'knowledge', 'awareness', 'interaction'],
    tsa: ['athletics', 'covert-ops', 'stamina', 'knowledge', 'awareness', 'interaction'],
    weren: ['athletics', 'melee-combat', 'stamina', 'knowledge', 'awareness', 'interaction']
  };

  // Rank Tiers & Caps
  const RANK_TIERS = [
    { id: 'legend',   minAP: 300, maxSkillRank: 12, maxBroad: 13, ranksOverRookie: 4 },
    { id: 'exemplar', minAP: 200, maxSkillRank: 12, maxBroad: 11, ranksOverRookie: 3 },
    { id: 'veteran',  minAP: 100, maxSkillRank: 10, maxBroad: 9,  ranksOverRookie: 2 },
    { id: 'seasoned', minAP: 50,  maxSkillRank: 8,  maxBroad: 7,  ranksOverRookie: 1 },
    { id: 'rookie',   minAP: 0,   maxSkillRank: 5,  maxBroad: 5,  ranksOverRookie: 0 }
  ];

  // Free Perk Lookup
  const FREE_PERKS = {
    cybernetic_interface: ['mechalus', 'nariac']
  };

  // Profession Favored Tables (Matching validate_character.py)
  const PROFESSION_DATA = {
    'combat-spec': {
      favoredCategories: [],
      favoredBroad: ['athletics', 'armor-operation', 'tactics', 'heavy-weapons', 'melee-combat', 'modern-ranged-weapons']
    },
    'free-agent': {
      favoredCategories: [],
      favoredBroad: ['covert-ops', 'deception', 'stealth', 'drive', 'vehicle-operation', 'acrobatics', 'culture']
    },
    'tech-op': {
      favoredCategories: [],
      favoredBroad: ['computer-science', 'technical-sciences', 'physical-science', 'system-operation', 'navigation', 'repair']
    },
    'mindwalker': {
      favoredCategories: [],
      favoredBroad: ['awareness', 'resolve', 'telepathy', 'telekinesis', 'biokinesis', 'esp', 'psychoportation']
    }
  };

  // Helper: Normalize skill identifier
  function normalizeId(input) {
    if (!input) return '';
    return input.toString().trim().toLowerCase().replace(/[\s_]+/g, '-');
  }

  const isNode = typeof process !== 'undefined' && process.versions && process.versions.node;
  let fs, path, defaultSkillsTable = null;

  if (isNode) {
    try {
      fs = require('fs');
      path = require('path');
      const tablePath = path.join(__dirname, '../../data/skills-table.json');
      if (fs.existsSync(tablePath)) {
        defaultSkillsTable = JSON.parse(fs.readFileSync(tablePath, 'utf8'));
      }
    } catch (e) {}
  }

  const CATEGORY_CANONICAL_MAP = {
    'combate': 'combat', 'combat': 'combat', 'combat-skills': 'combat',
    'técnica': 'technical', 'tecnica': 'technical', 'technical': 'technical', 'technical-skills': 'technical',
    'social': 'social', 'social-skills': 'social',
    'otros': 'other', 'other': 'other', 'other-skills': 'other',
    'psiónica': 'psionics', 'psionica': 'psionics', 'psionics': 'psionics', 'psionic-disciplines': 'psionics'
  };

  function normalizeCategory(cat) {
    if (!cat) return 'other';
    const c = normalizeId(cat);
    return CATEGORY_CANONICAL_MAP[c] || c;
  }

  class CharacterEngine {
    constructor(initialState = {}, skillsTable = null) {
      this.skillsTable = skillsTable || defaultSkillsTable || (typeof window !== 'undefined' && window.AAA_CHARACTER_DATA ? window.AAA_CHARACTER_DATA.skillsTable : null);
      this.buildSkillIndex();
      this.state = this.createDefaultState(initialState);
    }

    buildSkillIndex() {
      this.broadIndex = {};
      this.specialtyIndex = {};
      if (!this.skillsTable || !this.skillsTable.items) return;

      this.skillsTable.items.forEach(cat => {
        const catId = normalizeCategory(cat.id || cat.category || cat.skill);
        (cat.items || []).forEach(broad => {
          const bId = normalizeId(broad.id || broad.skill);
          const bName = normalizeId(broad.skill || broad.id);
          const bObj = {
            id: bId,
            skill: broad.skill,
            category: catId,
            cost: broad.cost || 3
          };
          this.broadIndex[bId] = bObj;
          this.broadIndex[bName] = bObj;

          (broad.items || []).forEach(spec => {
            const sId = normalizeId(spec.id || spec.skill);
            const sName = normalizeId(spec.skill || spec.id);
            const sObj = {
              id: sId,
              skill: spec.skill,
              category: catId,
              parentBroad: bId,
              cost: spec.cost || 3
            };
            this.specialtyIndex[sId] = sObj;
            this.specialtyIndex[sName] = sObj;
          });
        });
      });
    }

    isFavored(skillId, catId, parentBroadId = null, profession = this.state.profession) {
      const profKey = normalizeId(profession) || 'free-agent';
      const prof = PROFESSION_DATA[profKey] || PROFESSION_DATA['free-agent'];
      const ns = normalizeId(skillId);
      const cat = normalizeCategory(catId);
      const np = parentBroadId ? normalizeId(parentBroadId) : null;

      if (prof.favoredCategories.includes(cat)) return true;
      if (prof.favoredBroad.includes(ns)) return true;
      if (np && prof.favoredBroad.includes(np)) return true;

      // Check species free broads
      const species = normalizeId(this.state.species);
      if (SPECIES_FREE_BROAD_SLUGS[species]) {
        if (SPECIES_FREE_BROAD_SLUGS[species].includes(ns)) return true;
        if (np && SPECIES_FREE_BROAD_SLUGS[species].includes(np)) return true;
      }
      
      // Check background favored skills
      const bgFavored = this.state.backgroundFavoredSkills || [];
      if (bgFavored.includes(ns)) return true;
      if (np && bgFavored.includes(np)) return true;

      return false;
    }

    createDefaultState(override = {}) {
      return Object.assign({
        step: 1,
        bio: {
          name: '',
          player: '',
          concept: '',
          motivation: '',
          attitude: '',
          traits: '',
          gender: '',
          age: '',
          height: '',
          weight: '',
          hair: '',
          eyes: ''
        },
        faction: 'austrin_ontis',
        species: 'human',
        background: '',
        profession: 'free-agent',
        abilities: { STR: 10, DEX: 10, CON: 10, INT: 10, WIL: 10, PER: 10 },
        skills: {},
        perks: [],
        flaws: [],
        isFinalized: false,
        earnedAP: 75,
        advancementSkills: {},
        advancementAbilities: {},
        advancementPerks: [],
        removedFlaws: [],
        equipment: '',
        weapons: '',
        armor: '',
        credits: 2500,
        notes: ''
      }, override);
    }

    /**
     * Resolves species ability limits including faction modifiers
     */
    getAbilityLimits(species = this.state.species, faction = this.state.faction) {
      const sp = normalizeId(species) || 'human';
      const fact = normalizeId(faction);
      const base = JSON.parse(JSON.stringify(SPECIES_LIMITS[sp] || SPECIES_LIMITS['human']));

      if (sp === 'human') {
        if (fact === 'thuldan') {
          base.STR[1] = 15;
          base.CON[1] = 15;
        } else if (fact === 'borealis') {
          base.INT[1] = 15;
        } else if (fact === 'orion') {
          base.PER[1] = 15;
        }
      }
      return base;
    }

    /**
     * Calculates total ability budget (Base 60 + Sol bonus + Perks)
     */
    getAbilityBudget() {
      let budget = 60;
      if (normalizeId(this.state.faction) === 'union_of_sol') budget += 2;

      // Rank Title ability upgrades (Seasoned +1, Veteran +2, Exemplar +3, Legend +4)
      const rankTier = this.getRankTier();
      budget += rankTier ? (rankTier.ranksOverRookie || 0) : 0;

      // Heightened Ability perks grant +3 ability points per level
      if (Array.isArray(this.state.perks)) {
        this.state.perks.forEach(p => {
          const pName = typeof p === 'string' ? p : (p.name || p.id || '');
          if (pName.toLowerCase().includes('heightened ability')) {
            const level = (typeof p === 'object' && p.level) ? p.level : 1;
            budget += level * 3;
          }
        });
      }
      return budget;
    }

    /**
     * Validates ability scores against species & faction bounds
     */
    validateAbilities() {
      const limits = this.getAbilityLimits();
      const errors = [];
      const species = normalizeId(this.state.species);
      const faction = normalizeId(this.state.faction);
      const advAbilities = this.state.advancementAbilities || {};

      for (const [stat, range] of Object.entries(limits)) {
        const [minVal, maxVal] = range;
        const baseVal = (this.state.abilities && this.state.abilities[stat]) || 10;
        const bonusVal = (species === 'human' && ((faction === 'borealis' && stat === 'INT') || (faction === 'orion' && stat === 'PER'))) ? 1 : 0;
        const advVal = advAbilities[stat] || 0;
        const totalVal = baseVal + bonusVal + advVal;

        if (totalVal < minVal) {
          errors.push(`Ability Score Violation (${stat}): Total score ${totalVal} is below species minimum of ${minVal}.`);
        } else if (totalVal > maxVal) {
          errors.push(`Ability Score Violation (${stat}): Total score ${totalVal} exceeds species maximum of ${maxVal}.`);
        }
      }

      return { isValid: errors.length === 0, errors };
    }

    /**
     * Resolves canonical free broad skills for species
     */
    getSpeciesFreeBroads(species = this.state.species) {
      const sp = normalizeId(species) || 'human';
      return SPECIES_FREE_BROAD_SLUGS[sp] || SPECIES_FREE_BROAD_SLUGS['human'];
    }

    /**
     * Calculates Creation (SP/BP) unit cost for a skill
     */
    getCreationSkillCost(skillId, isBroad = false) {
      const ns = normalizeId(skillId);
      const profession = this.state.profession;
      if (isBroad) {
        const bInfo = this.broadIndex[ns] || { cost: 3, category: 'other' };
        const fav = this.isFavored(ns, bInfo.category, null, profession);
        return fav ? Math.max(1, (bInfo.cost || 3) - 1) : (bInfo.cost || 3);
      } else {
        const sInfo = this.specialtyIndex[ns] || { cost: 3, category: 'other', parentBroad: '' };
        const fav = this.isFavored(ns, sInfo.category, sInfo.parentBroad, profession);
        return fav ? Math.max(1, (sInfo.cost || 3) - 1) : (sInfo.cost || 3);
      }
    }

    /**
     * Calculates Campaign Advancement (AP) cost for a skill rank
     */
    getAdvancementSkillCost(skillId, targetRank, isBroad = false) {
      const ns = normalizeId(skillId);
      const profession = this.state.profession;

      if (isBroad) {
        const bInfo = this.broadIndex[ns] || { cost: 3, category: 'other' };
        const fav = this.isFavored(ns, bInfo.category, null, profession);
        return fav ? Math.max(1, (bInfo.cost || 3) - 1) : (bInfo.cost || 3);
      } else {
        const sInfo = this.specialtyIndex[ns] || { cost: 3, category: 'other', parentBroad: '' };
        const fav = this.isFavored(ns, sInfo.category, sInfo.parentBroad, profession);
        let baseCost = fav ? Math.max(1, (sInfo.cost || 3) - 1) : (sInfo.cost || 3);

        if (targetRank >= 11) baseCost += 6;
        else if (targetRank >= 9) baseCost += 4;
        else if (targetRank >= 6) baseCost += 2;

        return baseCost;
      }
    }

    /**
     * Resolves Rank Title Tier object for total AP
     */
    getRankTier(totalAP = this.state.earnedAP) {
      return RANK_TIERS.find(t => totalAP >= t.minAP) || RANK_TIERS[RANK_TIERS.length - 1];
    }

    /**
     * Complete Character Validation Engine
     */
    /**
     * Complete Character Validation Engine matching Python validator rules
     */
    validate() {
      const errors = [];
      const warnings = [];
      const info = [];

      // 1. Ability Scores
      const abRes = this.validateAbilities();
      errors.push(...abRes.errors);

      // 2. Perks & Flaws Limits & SP Modifications
      const chosenPerks = (this.state.perks || []).filter(p => {
        const name = typeof p === 'string' ? p : (p.name || '');
        return !name.toLowerCase().includes('cybernetic interface') && !name.toLowerCase().includes('innate psionics');
      });
      const chosenFlaws = this.state.flaws || [];

      if (chosenPerks.length > 3) {
        errors.push(`Perks Limit Violation: Has ${chosenPerks.length} chosen creation perks (Max allowed is 3).`);
      }
      if (chosenFlaws.length > 3) {
        errors.push(`Flaws Limit Violation: Has ${chosenFlaws.length} chosen creation flaws (Max allowed is 3).`);
      }

      let perkSPCost = 0;
      chosenPerks.forEach(p => {
        if (typeof p === 'object') {
          perkSPCost += p.cost || p.finalCost || ((p.level || 1) * 3);
        } else {
          perkSPCost += 3;
        }
      });

      let flawSPBonus = 0;
      chosenFlaws.forEach(f => {
        if (typeof f === 'object') {
          flawSPBonus += f.bonus || f.rawBonus || ((f.level || 1) * 3);
        } else {
          flawSPBonus += 3;
        }
      });

      const species = normalizeId(this.state.species);
      const faction = normalizeId(this.state.faction);
      const profession = normalizeId(this.state.profession);
      const speciesFreeBroads = SPECIES_FREE_BROAD_SLUGS[species] || [];
      const advSkills = this.state.advancementSkills || {};
      const skills = this.state.skills || {};

      const baseSP = (faction === 'rigunmor' && this.state.bonusPerkOrPointsChoice === 'points') ? 76 : 70;
      const totalSPBudget = baseSP;

      // 3. Skills Validation & BP Calculation
      let creationSPSpent = perkSPCost - flawSPBonus;
      let broadCount = 0;

      for (const [sId, item] of Object.entries(skills)) {
        const ns = normalizeId(sId);
        const totalRanks = item.ranks || 0;
        if (totalRanks <= 0) continue;

        const campRanks = advSkills[sId] || 0;
        const creationRanks = Math.max(0, totalRanks - campRanks);

        const isBroad = ns in this.broadIndex;
        const isSpecialty = ns in this.specialtyIndex;

        if (!isBroad && !isSpecialty) continue;

        const isFreeBroad = speciesFreeBroads.includes(ns) || (faction === 'voidcorp' && ns === 'business');

        if (totalRanks > 12) {
          errors.push(`Skill '${sId}' rank ${totalRanks} exceeds absolute MAX rank cap of 12!`);
        }

        if (isBroad) {
          if (!isFreeBroad && creationRanks > 0) {
            const bInfo = this.broadIndex[ns] || { cost: 3, category: 'other' };
            const fav = this.isFavored(ns, bInfo.category, null, profession);
            const cost = fav ? Math.max(1, (bInfo.cost || 3) - 1) : (bInfo.cost || 3);
            creationSPSpent += cost;
            broadCount++;
          }
        } else {
          const sInfo = this.specialtyIndex[ns] || { cost: 3, category: 'other', parentBroad: '' };
          const parentBroad = sInfo.parentBroad;
          if (parentBroad && (!skills[parentBroad] && !skills[sInfo.id])) {
            const pItem = skills[parentBroad] || Object.values(skills).find(sk => normalizeId(sk.id || sk.name) === parentBroad);
            if (!pItem || (pItem.ranks || 0) <= 0) {
              errors.push(`Specialty skill '${sId}' trained but parent broad '${parentBroad}' is missing!`);
            }
          }

          if (creationRanks > 3) {
            errors.push(`Specialty skill '${sId}' exceeds MAX 3 Creation Ranks! Found ${creationRanks} creation ranks.`);
          }

          if (creationRanks > 0) {
            const fav = this.isFavored(ns, sInfo.category, parentBroad, profession);
            const unitCost = fav ? Math.max(1, (sInfo.cost || 3) - 1) : (sInfo.cost || 3);
            creationSPSpent += unitCost * creationRanks;
          }
        }
      }

      if (broadCount > 5) {
        errors.push(`Broad Skill Cap Violation: Has ${broadCount} broad skills at creation (Max allowed is 5).`);
      }

      const remainingBP = totalSPBudget - creationSPSpent;
      if (this.state.isFinalized && remainingBP > 0) {
        errors.push(`Unspent Build Points (BP) Violation: Found ${remainingBP} unspent BP! All BP must be spent when entering campaign mode.`);
      } else if (creationSPSpent > totalSPBudget) {
        errors.push(`Build Points Budget Exceeded: Spent ${creationSPSpent} BP out of ${totalSPBudget} budget.`);
      } else {
        info.push(`Creation Budget (BP): ${creationSPSpent} / ${totalSPBudget} BP spent (${remainingBP} remaining)`);
      }

      // 4. Campaign AP balance check
      let campaignAPSpent = 0;
      for (const [sId, advRanks] of Object.entries(advSkills)) {
        const totalRanks = skills[sId] ? skills[sId].ranks : 0;
        const creationRanks = Math.max(0, totalRanks - advRanks);
        const isBroad = skills[sId] ? (skills[sId].isBroad !== undefined ? skills[sId].isBroad : skills[sId].type === 'broad') : false;

        for (let r = 1; r <= advRanks; r++) {
          campaignAPSpent += this.getAdvancementSkillCost(sId, creationRanks + r, isBroad);
        }
      }

      if (Array.isArray(this.state.advancementPerks)) {
        this.state.advancementPerks.forEach(p => {
          campaignAPSpent += p.apCost || p.cost || 0;
        });
      }

      if (Array.isArray(this.state.removedFlaws)) {
        this.state.removedFlaws.forEach(f => {
          campaignAPSpent += f.apCost || 0;
        });
      }

      if (this.state.earnedAP !== campaignAPSpent) {
        warnings.push(`Campaign AP mismatch: Spent ${campaignAPSpent} AP vs Earned ${this.state.earnedAP} AP.`);
      } else {
        info.push(`Campaign Advancement: ${campaignAPSpent} / ${this.state.earnedAP} AP spent (Parity OK)`);
      }

      return {
        isValid: errors.length === 0,
        errors,
        warnings,
        info,
        creationSPSpent,
        campaignAPSpent,
        rankTier: this.getRankTier()
      };
    }

    /**
     * Serializes character state to clean JSON object
     */
    toJSON() {
      return JSON.parse(JSON.stringify(this.state));
    }

    /**
     * Loads and normalizes raw JSON save state
     */
    fromJSON(jsonObj) {
      if (typeof jsonObj === 'string') {
        jsonObj = JSON.parse(jsonObj);
      }
      this.state = this.createDefaultState(jsonObj);
      return this;
    }
  }

  return CharacterEngine;
}));

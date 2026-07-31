const { test, expect } = require('@playwright/test');

test.describe('Character Builder Core Logic', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to the character builder page (assuming localhost:1313 is the dev server)
    // We can also just mock the HTML and script if the server is not running, 
    // but typically playwright tests in this repo run against a specific URL.
    await page.goto('http://localhost:1313/es/character-builder/');
    
    // Wait for the JS to expose the test API
    await page.waitForFunction(() => window.__CB_TEST_API__ !== undefined);
  });

  test('isFavored applies faction discounts correctly', async ({ page }) => {
    const isFavored = await page.evaluate(() => {
      const api = window.__CB_TEST_API__;
      
      // Setup mock state
      api.state.faction = 'austrin_ontis';
      api.state.profession = 'combat-spec';
      
      return api.isFavored('heavy-weapons', 'combat');
    });
    
    expect(isFavored).toBe(true);
  });

  test('isFavored handles profession favored categories', async ({ page }) => {
    const isFavored = await page.evaluate(() => {
      const api = window.__CB_TEST_API__;
      
      api.state.faction = 'union_of_sol';
      api.state.profession = 'tech-op'; // Tech Op favors Technical
      
      return api.isFavored('computer-science', 'technical');
    });
    
    expect(isFavored).toBe(true);
  });

  test('getAdvancementSkillCost calculates base and favored costs accurately', async ({ page }) => {
    const costResults = await page.evaluate(() => {
      const api = window.__CB_TEST_API__;
      
      // Setup mock state
      api.state.faction = 'union_of_sol';
      api.state.profession = 'combat-spec';
      
      // Add mock skill to data if needed, or rely on actual data loaded in page
      return {
        // Combat Spec favors 'combat' category, so athletics (cost 3) is favored
        favoredCost: api.getAdvancementSkillCost('athletics', 1, false),
        baseCost: api.getAdvancementSkillCost('athletics', 1, true),
      };
    });
    
    // Athletics is cost 3. Favored brings it to 2.
    expect(costResults.favoredCost).toBe(2);
    expect(costResults.baseCost).toBe(3);
  });

  test('calculateCampaignSpentAP tallies correct AP', async ({ page }) => {
    const spentAP = await page.evaluate(() => {
      const api = window.__CB_TEST_API__;
      
      // Setup a fresh state
      api.state.faction = 'union_of_sol';
      api.state.profession = 'combat-spec';
      api.state.advancementAbilities = { STR: 1 }; // 10 AP
      
      // Mock some skills. Athletics is broad, cost 3, favored -> 2 AP
      api.state.skills = {
        'athletics': { ranks: 0, isBroad: true, standardCost: 3, category: 'combat' }
      };
      
      api.state.advancementSkills = {
        'athletics': 1 // 1 rank * 2 AP = 2 AP
      };
      
      api.state.advancementPerks = [
        { name: 'Great Stamina', level: 1, baseApCost: 3, apCost: 3 } // 3 AP
      ];
      
      return api.calculateCampaignSpentAP(false);
    });
    
    // 10 (ability) + 2 (skill) + 3 (perk) = 15 AP
    expect(spentAP).toBe(15);
  });
});

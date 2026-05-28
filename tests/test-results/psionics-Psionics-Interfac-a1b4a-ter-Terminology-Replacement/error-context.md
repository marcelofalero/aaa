# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: psionics.spec.js >> Psionics Interface Automated Tests >> Step 3: Verify "character" Terminology Replacement
- Location: psionics.spec.js:50:5

# Error details

```
Error: page.goto: net::ERR_CONNECTION_REFUSED at http://localhost:1313/psionics/
Call log:
  - navigating to "http://localhost:1313/psionics/", waiting until "load"

```

# Test source

```ts
  1  | const { test, expect } = require('@playwright/test');
  2  | 
  3  | test.describe('Psionics Interface Automated Tests', () => {
  4  |     test.beforeEach(async ({ page }) => {
> 5  |         await page.goto('http://localhost:1313/psionics/');
     |                    ^ Error: page.goto: net::ERR_CONNECTION_REFUSED at http://localhost:1313/psionics/
  6  |     });
  7  | 
  8  |     test('Step 1: Verify correctly updated Attributes (Data Fixes)', async ({ page }) => {
  9  |         // Biokinesis check (CON)
  10 |         const biokinesisRow = page.locator('tr.level-2:has-text("Biokinesis")');
  11 |         await expect(biokinesisRow.locator('.cell-attribute')).toContainText('CON');
  12 | 
  13 |         // ESP check (INT)
  14 |         const espRow = page.locator('tr.level-2:has-text("ESP")');
  15 |         await expect(espRow.locator('.cell-attribute')).toContainText('INT');
  16 | 
  17 |         // Telepathy check (PER)
  18 |         const telepathyRow = page.locator('tr.level-2:has-text("Telepathy")');
  19 |         await expect(telepathyRow.locator('.cell-attribute')).toContainText('PER');
  20 | 
  21 |         // Psychoportation rename verification
  22 |         const psychoportRow = page.locator('tr.level-2:has-text("Psychoportation")');
  23 |         await expect(psychoportRow).toBeVisible();
  24 |     });
  25 | 
  26 |     test('Step 2: Verify "Trained Only" Visual Indicators (UI/UX)', async ({ page }) => {
  27 |         // Expand Biokinesis to see its powers
  28 |         const biokinesisRow = page.locator('tr.level-2:has-text("Biokinesis")');
  29 |         await biokinesisRow.click();
  30 | 
  31 |         // Heal is Trained Only
  32 |         const healRow = page.locator('tr.level-3:has-text("Heal")');
  33 |         await expect(healRow).toHaveClass(/trained-only/);
  34 | 
  35 |         // Verify Neon Blue color
  36 |         const color = await healRow.locator('td').first().evaluate(el => window.getComputedStyle(el).color);
  37 |         expect(color).toBe('rgb(0, 206, 255)');
  38 | 
  39 |         // Bio-Toxin is NOT Trained Only (checking YAML/JSON - it was set to False)
  40 |         // Wait! Let's check Bio-Toxin. I'll search for it.
  41 |         const toxinRow = page.locator('tr.level-3:has-text("Bio-Toxin")');
  42 |         if (await toxinRow.isVisible()) {
  43 |             await expect(toxinRow).not.toHaveClass(/trained-only/);
  44 |             const toxinColor = await toxinRow.locator('td').first().evaluate(el => window.getComputedStyle(el).color);
  45 |             // Default color is roughly var(--table-text-light)
  46 |             expect(toxinColor).not.toBe('rgb(0, 206, 255)');
  47 |         }
  48 |     });
  49 | 
  50 |     test('Step 3: Verify "character" Terminology Replacement', async ({ page }) => {
  51 |         const bodyContent = await page.innerText('body');
  52 |         const lowercaseBody = bodyContent.toLowerCase();
  53 | 
  54 |         // Should use "character" but not "hero" (outside established names maybe?)
  55 |         // Note: we can't completely ban "hero" if it's in a brand name, 
  56 |         // but here it was in descriptions like "A hero can..."
  57 |         expect(lowercaseBody).toContain('character');
  58 |         expect(lowercaseBody).not.toContain('hero can');
  59 |         expect(lowercaseBody).not.toContain('a hero');
  60 | 
  61 |         // Check for specific "challenging obstacles" replacement if it exists on page
  62 |         if (lowercaseBody.includes('obstacles')) {
  63 |             expect(lowercaseBody).toContain('challenging obstacles');
  64 |             expect(lowercaseBody).not.toContain('heroic obstacles');
  65 |         }
  66 |     });
  67 | 
  68 |     test('Step 4: Verify Search Functionality in Table', async ({ page }) => {
  69 |         const searchInput = page.locator('.nested-table-search').first();
  70 |         await searchInput.fill('Telekinesis');
  71 |         
  72 |         // Only Telekinesis should be visible (and Categories)
  73 |         const teleRow = page.locator('tr.level-2:has-text("Telekinesis")');
  74 |         await expect(teleRow).toBeVisible();
  75 |         
  76 |         const biokinesisRow = page.locator('tr.level-2:has-text("Biokinesis")');
  77 |         await expect(biokinesisRow).not.toBeVisible();
  78 |     });
  79 | });
  80 | 
```
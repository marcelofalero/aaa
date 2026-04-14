const { test, expect } = require('@playwright/test');

test.describe('Psionics Interface Automated Tests', () => {
    test.beforeEach(async ({ page }) => {
        await page.goto('http://localhost:1313/core-mechanics/psionics/');
    });

    test('Step 1: Verify correctly updated Attributes (Data Fixes)', async ({ page }) => {
        // Biokinesis check (CON)
        const biokinesisRow = page.locator('tr.level-2:has-text("Biokinesis")');
        await expect(biokinesisRow.locator('.cell-attribute')).toContainText('CON');

        // ESP check (INT)
        const espRow = page.locator('tr.level-2:has-text("ESP")');
        await expect(espRow.locator('.cell-attribute')).toContainText('INT');

        // Telepathy check (PER)
        const telepathyRow = page.locator('tr.level-2:has-text("Telepathy")');
        await expect(telepathyRow.locator('.cell-attribute')).toContainText('PER');

        // Psychoportation rename verification
        const psychoportRow = page.locator('tr.level-2:has-text("Psychoportation")');
        await expect(psychoportRow).toBeVisible();
    });

    test('Step 2: Verify "Trained Only" Visual Indicators (UI/UX)', async ({ page }) => {
        // Expand Biokinesis to see its powers
        const biokinesisRow = page.locator('tr.level-2:has-text("Biokinesis")');
        await biokinesisRow.click();

        // Heal is Trained Only
        const healRow = page.locator('tr.level-3:has-text("Heal")');
        await expect(healRow).toHaveClass(/trained-only/);

        // Verify Neon Blue color
        const color = await healRow.locator('td').first().evaluate(el => window.getComputedStyle(el).color);
        expect(color).toBe('rgb(0, 206, 255)');

        // Bio-Toxin is NOT Trained Only (checking YAML/JSON - it was set to False)
        // Wait! Let's check Bio-Toxin. I'll search for it.
        const toxinRow = page.locator('tr.level-3:has-text("Bio-Toxin")');
        if (await toxinRow.isVisible()) {
            await expect(toxinRow).not.toHaveClass(/trained-only/);
            const toxinColor = await toxinRow.locator('td').first().evaluate(el => window.getComputedStyle(el).color);
            // Default color is roughly var(--table-text-light)
            expect(toxinColor).not.toBe('rgb(0, 206, 255)');
        }
    });

    test('Step 3: Verify "character" Terminology Replacement', async ({ page }) => {
        const bodyContent = await page.innerText('body');
        const lowercaseBody = bodyContent.toLowerCase();

        // Should use "character" but not "hero" (outside established names maybe?)
        // Note: we can't completely ban "hero" if it's in a brand name, 
        // but here it was in descriptions like "A hero can..."
        expect(lowercaseBody).toContain('character');
        expect(lowercaseBody).not.toContain('hero can');
        expect(lowercaseBody).not.toContain('a hero');

        // Check for specific "challenging obstacles" replacement if it exists on page
        if (lowercaseBody.includes('obstacles')) {
            expect(lowercaseBody).toContain('challenging obstacles');
            expect(lowercaseBody).not.toContain('heroic obstacles');
        }
    });

    test('Step 4: Verify Search Functionality in Table', async ({ page }) => {
        const searchInput = page.locator('.nested-table-search').first();
        await searchInput.fill('Telekinesis');
        
        // Only Telekinesis should be visible (and Categories)
        const teleRow = page.locator('tr.level-2:has-text("Telekinesis")');
        await expect(teleRow).toBeVisible();
        
        const biokinesisRow = page.locator('tr.level-2:has-text("Biokinesis")');
        await expect(biokinesisRow).not.toBeVisible();
    });
});

const { test, expect } = require('@playwright/test');

test('debug psionics', async ({ page }) => {
    await page.goto('http://localhost:1313/core-mechanics/psionics/');
    
    // Check attributes
    const biokinesisRow = page.locator('tr.level-2:has-text("Biokinesis")');
    const bAttr = await biokinesisRow.locator('.cell-attribute').innerText();
    console.log(`Biokinesis Attribute: "${bAttr}"`);
    
    // Expand
    await biokinesisRow.click();
    
    // Check heal
    const healRow = page.locator('tr.level-3:has-text("Heal")');
    const hClass = await healRow.getAttribute('class');
    console.log(`Heal Class: "${hClass}"`);
    
    const hColor = await healRow.locator('td').first().evaluate(el => window.getComputedStyle(el).color);
    console.log(`Heal Color: "${hColor}"`);
    
    // Check descriptions on page
    const bodyContent = await page.innerText('body');
    console.log(`Body includes "character": ${bodyContent.toLowerCase().includes('character')}`);
    console.log(`Body includes "hero": ${bodyContent.toLowerCase().includes('hero')}`);
});

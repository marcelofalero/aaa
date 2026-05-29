const { chromium } = require('@playwright/test');
const path = require('path');
const fs = require('fs');

(async () => {
    const campaignId = '21281760';
    const profilePath = path.resolve(__dirname, '../.chrome-profile');
    
    console.log(`[EXPLORE] Launching Chrome profile from: ${profilePath}`);
    const context = await chromium.launchPersistentContext(profilePath, {
        headless: false,
        viewport: { width: 1280, height: 800 },
        ignoreDefaultArgs: ['--enable-automation'],
        args: ['--disable-blink-features=AutomationControlled']
    });

    const page = context.pages()[0] || await context.newPage();
    const editorUrl = `https://app.roll20.net/editor/setcampaign/${campaignId}`;
    
    console.log(`[EXPLORE] Navigating to VTT: ${editorUrl}`);
    await page.goto(editorUrl, { waitUntil: 'domcontentloaded' });
    
    // Wait for the VTT chat input to be active (means VTT is fully initialized)
    console.log('[EXPLORE] Waiting for VTT loading...');
    await page.waitForSelector('#textchat-input textarea', { timeout: 60000 });
    console.log('[EXPLORE] VTT successfully loaded!');
    
    // Wait 4 seconds for websocket and assets to settle
    await page.waitForTimeout(4000);
    
    // Take a screenshot of loaded state
    await page.screenshot({ path: path.join(__dirname, 'explore_vtt_success.png') });
    
    // Click the Collections (Decks) Tab
    console.log('[EXPLORE] Finding and clicking Decks tab...');
    const decksTabBtn = page.locator('a[href="#deckstab"]');
    await decksTabBtn.click();
    await page.waitForTimeout(1000);
    
    // Extract HTML content of the #deckstab pane
    console.log('[EXPLORE] Extracting #deckstab HTML...');
    const deckstabHtml = await page.locator('#deckstab').innerHTML();
    fs.writeFileSync(path.join(__dirname, 'deckstab_structure.html'), deckstabHtml);
    console.log('[EXPLORE] Successfully saved HTML structure to scratch/deckstab_structure.html');
    
    // Take another screenshot showing the Decks tab
    await page.screenshot({ path: path.join(__dirname, 'explore_vtt_decks.png') });
    
    await context.close();
    console.log('[EXPLORE] Done!');
})();

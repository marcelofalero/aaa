const { chromium } = require('@playwright/test');
const path = require('path');
const fs = require('fs');

(async () => {
    const campaignId = '21281760';
    const profilePath = path.resolve(__dirname, '../.chrome-profile');
    
    console.log(`[DECK BUILDER] Launching Chrome profile from: ${profilePath}`);
    const context = await chromium.launchPersistentContext(profilePath, {
        headless: false,
        viewport: { width: 1280, height: 800 },
        ignoreDefaultArgs: ['--enable-automation'],
        args: ['--disable-blink-features=AutomationControlled']
    });

    const page = context.pages()[0] || await context.newPage();
    const editorUrl = `https://app.roll20.net/editor/setcampaign/${campaignId}`;
    
    console.log(`[DECK BUILDER] Navigating to VTT: ${editorUrl}`);
    await page.goto(editorUrl, { waitUntil: 'domcontentloaded' });
    
    // Check if we are on the login page or a redirect happened
    await page.waitForTimeout(3000);
    const isLoginPage = page.url().includes('login') || await page.locator('input[name="email"]').count() > 0;
    
    if (isLoginPage) {
        console.log('\n========================================================================');
        console.log('🔒 [ACTION REQUIRED] Please log into your Roll20 account in the browser window.');
        console.log('Solve any Cloudflare/Captcha challenges if prompted.');
        console.log('The script will automatically resume once you are logged in and the VTT loads.');
        console.log('========================================================================\n');
        // Wait up to 5 minutes for login to complete and VTT to load
        await page.waitForSelector('#textchat-input textarea', { timeout: 300000 });
        console.log('[DECK BUILDER] Login successful! Resuming automated deck build...');
    } else {
        console.log('[DECK BUILDER] Waiting for VTT to initialize...');
        await page.waitForSelector('#textchat-input textarea', { timeout: 60000 });
    }
    
    console.log('[DECK BUILDER] VTT loaded successfully!');
    await page.waitForTimeout(4000); // Allow websocket connections to stabilize
    
    // Open the Collections (Decks) Tab
    console.log('[DECK BUILDER] Opening Collections tab...');
    await page.locator('a[href="#deckstables"]').click();
    await page.waitForTimeout(2000);
    
    // 1. Clean up old deck if it exists to prevent duplicates
    console.log('[DECK BUILDER] Checking for existing "Alternity Phases" deck...');
    const existingDeckRow = page.locator('table#existingdecks tr.deck', { hasText: 'Alternity Phases' }).first();
    if (await existingDeckRow.count() > 0) {
        console.log('[DECK BUILDER] Found existing deck. Deleting to recreate with updated assets...');
        await existingDeckRow.locator('td.name').click();
        await page.waitForTimeout(2500);
        
        // Click the Delete Deck button
        const deleteBtn = page.locator('.ui-dialog button.deletedeck').first();
        if (await deleteBtn.count() > 0) {
            await deleteBtn.click();
            await page.waitForTimeout(1500);
            
            // Confirm deletion in dialog
            const confirmBtn = page.locator('.ui-dialog-buttonpane button:has-text("Confirm"), .ui-dialog-buttonpane button:has-text("Delete Deck"), button:has-text("Yes"), button:has-text("Delete")').first();
            if (await confirmBtn.count() > 0) {
                await confirmBtn.click();
                console.log('[DECK BUILDER] Old deck deleted successfully.');
                await page.waitForTimeout(2500);
            }
        }
    }
    
    // 2. Add New Deck
    console.log('[DECK BUILDER] Adding a new deck...');
    await page.locator('button#adddeck').click();
    await page.waitForTimeout(2500);
    
    // Click on the newly created "New Deck" row to open settings
    console.log('[DECK BUILDER] Opening new deck settings...');
    const newDeckRow = page.locator('table#existingdecks tr.deck', { hasText: 'New Deck' }).first();
    await newDeckRow.locator('td.name').click();
    await page.waitForTimeout(2500);
    
    // 3. Rename and configure Deck Settings
    console.log('[DECK BUILDER] Configuring deck options...');
    const deckDialog = page.locator('.ui-dialog:not(.initiativedialog)').first();
    
    // Fill Name
    await deckDialog.locator('input.name').fill('Alternity Phases');
    
    // Upload Card Back
    console.log('[DECK BUILDER] Uploading card back image...');
    const backFileInput = deckDialog.locator('input[type="file"]').first();
    await backFileInput.setInputFiles(path.resolve(__dirname, '../roll20_charsheet/initiative_cards/card_back.png'));
    await page.waitForTimeout(6000); // Allow S3 upload to finish
    
    // Check checkboxes
    await deckDialog.locator('input.showplayers').setChecked(true);
    await deckDialog.locator('input.playerscandraw').setChecked(true);
    await deckDialog.locator('input.infinitecards').setChecked(true);
    
    // Select "Always a random card" radio button if present
    const randomRadio = deckDialog.locator('input[type="radio"][value="random"]');
    if (await randomRadio.count() > 0) {
        await randomRadio.setChecked(true);
    }
    
    // Save main settings
    console.log('[DECK BUILDER] Saving main deck settings...');
    const saveBtn = page.locator('.ui-dialog:not(.initiativedialog) button:has-text("Save Changes"), .ui-dialog:not(.initiativedialog) .ui-dialog-buttonpane button').first();
    await saveBtn.click();
    await page.waitForTimeout(3000);
    
    // 4. Add Card Faces
    console.log('[DECK BUILDER] Adding card faces...');
    const phases = [
        { name: 'Amazing', file: 'amazing.png' },
        { name: 'Good', file: 'good.png' },
        { name: 'Ordinary', file: 'ordinary.png' },
        { name: 'Marginal', file: 'marginal.png' }
    ];
    
    for (const phase of phases) {
        // Reopen deck settings to add card
        console.log(`\n[DECK BUILDER] Reopening "Alternity Phases" settings for card: "${phase.name}"...`);
        const activeDeckRow = page.locator('table#existingdecks tr.deck', { hasText: 'Alternity Phases' }).first();
        await activeDeckRow.locator('td.name').click();
        await page.waitForTimeout(2500);
        
        // Click Add Card button in the main deck dialog
        const activeDialog = page.locator('.ui-dialog:not(.initiativedialog)').first();
        await activeDialog.locator('button.addcard').click();
        await page.waitForTimeout(2500);
        
        // Target the newly opened Card dialog (the last visible non-initiativedialog)
        const cardDialog = page.locator('.ui-dialog:not(.initiativedialog)').last();
        
        // Set Card Name
        await cardDialog.locator('input.name').fill(phase.name);
        
        // Upload Card Face
        console.log(`[DECK BUILDER] Uploading ${phase.file} face...`);
        const cardFileInput = cardDialog.locator('input[type="file"]').first();
        await cardFileInput.setInputFiles(path.resolve(__dirname, `../roll20_charsheet/initiative_cards/${phase.file}`));
        await page.waitForTimeout(6000); // Allow upload to complete
        
        // Save Card Dialog
        console.log(`[DECK BUILDER] Saving card "${phase.name}"...`);
        const cardSaveBtn = cardDialog.locator('button:has-text("Save Changes"), .ui-dialog-buttonpane button').first();
        await cardSaveBtn.click();
        await page.waitForTimeout(3000);
        
        // Close parent Deck Settings dialog
        console.log(`[DECK BUILDER] Closing deck editor dialog...`);
        const deckCloseBtn = page.locator('.ui-dialog:not(.initiativedialog)').first().locator('button:has-text("Save Changes"), .ui-dialog-buttonpane button').first();
        await deckCloseBtn.click();
        await page.waitForTimeout(2000);
    }
    
    // 5. Show Deck on tabletop
    console.log('[DECK BUILDER] Showing the deck on the VTT tabletop...');
    const activeDeckRowFinal = page.locator('table#existingdecks tr.deck', { hasText: 'Alternity Phases' }).first();
    const showDeckBtn = activeDeckRowFinal.locator('button.toggledeck');
    if (await showDeckBtn.count() > 0) {
        const btnText = await showDeckBtn.innerText();
        if (btnText.includes('Show')) {
            await showDeckBtn.click();
            console.log('[DECK BUILDER] Deck is now visible on tabletop!');
        } else {
            console.log('[DECK BUILDER] Deck was already shown.');
        }
    }
    
    await page.waitForTimeout(3000);
    await context.close();
    console.log('\n🎉 [DECK BUILDER] SUCCESS! The "Alternity Phases" deck has been completely created, configured, and uploaded to your campaign VTT!');
})();

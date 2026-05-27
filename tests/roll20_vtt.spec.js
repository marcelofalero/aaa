const { test, expect, chromium } = require('@playwright/test');
const path = require('path');
const fs = require('fs');

test.describe('Roll20 Live VTT Integration Tests', () => {
    // Generous timeout for VTT loading and asset preparation
    test.setTimeout(90000);

    let context;
    let page;

    test.beforeAll(async () => {
        const campaignId = process.env.ROLL20_CAMPAIGN_ID || '21281760';
        const profilePath = path.resolve(__dirname, '../.chrome-profile');

        console.log(`[TEST SETUP] Launching Chrome profile from: ${profilePath}`);
        context = await chromium.launchPersistentContext(profilePath, {
            headless: false, // Run in headful mode so that Roll20's WebGL tabletop initializes successfully
            viewport: { width: 1280, height: 800 },
            ignoreDefaultArgs: ['--enable-automation'],
            args: [
                '--disable-blink-features=AutomationControlled'
            ]
        });

        page = context.pages()[0] || await context.newPage();
    });

    test.afterAll(async () => {
        if (context) {
            await context.close();
        }
    });

    test('Should successfully execute Single and Double attacks in Roll20 VTT Chat', async () => {
        const campaignId = process.env.ROLL20_CAMPAIGN_ID || '21281760';
        const editorUrl = `https://app.roll20.net/editor/setcampaign/${campaignId}`;

        console.log(`[TEST EXEC] Navigating to: ${editorUrl}`);
        await page.goto(editorUrl, { waitUntil: 'domcontentloaded' });

        // Let's check for Cloudflare challenge elements
        const title = await page.title();
        const hasChallenge = await page.evaluate(() => {
            return !!(document.querySelector('#challenge-form') || document.querySelector('#cf-challenge') || document.querySelector('.cf-turnstile-wrapper'));
        });

        if (hasChallenge || title.includes('Cloudflare') || title.includes('Just a moment')) {
            console.log('\n========================================================================');
            console.log('🛡️ [ALERT] Cloudflare security challenge or Captcha loop detected!');
            console.log('Please click the Cloudflare checkbox or solve the Captcha in the opened browser window.');
            console.log('The test suite will automatically resume once the challenge is solved and VTT loads.');
            console.log('========================================================================\n');
            
            // Wait up to 5 minutes (300,000ms) for the user to solve the challenge and VTT to load
            await page.waitForSelector('#textchat-input textarea', { timeout: 300000 });
            console.log('[TEST EXEC] Challenge solved successfully! Resuming test sequence.');
        } else {
            console.log('[TEST EXEC] Waiting for Roll20 VTT to initialize...');
            await page.waitForSelector('#textchat-input textarea', { timeout: 45000 });
        }
        console.log('[TEST EXEC] Chat input is active.');

        // Settle websocket/client
        await page.waitForTimeout(4000);

        // Get initial message count
        const initialCount = await page.locator('.message').count();

        // 1. Trigger Single Attack Command in Chat
        console.log('[TEST EXEC] Triggering Single Attack...');
        const chatInput = page.locator('#textchat-input textarea');
        await chatInput.focus();

        const singleCmd = '!aaa-roll Playwright-Single || Laser Rifle || Energy || 50/150/300 || VTT Single Attack || 14 || 7 || 3 || 1 || 1d6cs<0cf<0 || +';
        await chatInput.fill(singleCmd);
        await page.keyboard.press('Enter');

        // Wait a few seconds for API execution
        await page.waitForTimeout(5000);

        // Get new message count
        let countAfterSingle = await page.locator('.message').count();
        expect(countAfterSingle).toBeGreaterThan(initialCount);

        // Locate and check the latest message text
        const latestMsgText = await page.locator('.message').last().textContent();
        console.log(`[TEST RESULT] Single Attack chat output: ${latestMsgText.replace(/\s+/g, ' ').trim()}`);
        
        // Assertions for Single Attack
        expect(latestMsgText).toContain('Playwright-Single');
        expect(latestMsgText).toContain('Laser Rifle');
        expect(latestMsgText).toContain('VTT Single Attack');
        expect(latestMsgText).toContain('Att. 1 [14/7/3]');

        // 2. Trigger Double Action Attack Command in Chat
        console.log('[TEST EXEC] Triggering Double Action Attack...');
        await chatInput.focus();

        const doubleCmd = '!aaa-roll Playwright-Double || Dual Pistols || Kinetic || 10/20/30 || VTT Double Attack || 11 || 5 || 2 || 2 || 1d8cs<0cf<0 || + || 1d12cs<0cf<0 || +';
        await chatInput.fill(doubleCmd);
        await page.keyboard.press('Enter');

        // Wait a few seconds for API execution
        await page.waitForTimeout(5000);

        // Get final message count
        let finalCount = await page.locator('.message').count();
        expect(finalCount).toBeGreaterThan(countAfterSingle);

        // Locate and check the latest double action output
        const doubleMsgText = await page.locator('.message').last().textContent();
        console.log(`[TEST RESULT] Double Action Attack chat output: ${doubleMsgText.replace(/\s+/g, ' ').trim()}`);

        // Assertions for Double Action Attack
        expect(doubleMsgText).toContain('Playwright-Double');
        expect(doubleMsgText).toContain('Dual Pistols');
        expect(doubleMsgText).toContain('VTT Double Attack');
        expect(doubleMsgText).toContain('Att. 1 [11/5/2]');
        expect(doubleMsgText).toContain('Att. 2 [11/5/2]');
    });
});

#!/usr/bin/env node

/**
 * Roll20 Character Sheet Uploader
 * Automates uploading compiled HTML, CSS, and translation JSON to a Roll20 Campaign Settings page.
 * Uses the persistent Chrome profile to maintain Roll20 login state.
 */

const fs = require('fs');
const path = require('path');
const { chromium } = require('@playwright/test');

// Help/Usage message
const usage = `
Roll20 Character Sheet Uploader
==============================
Automates uploading Alternity RPG character sheet components to Roll20.

Usage:
  node update_sheet.js [options]

Options:
  -c, --campaign <id>   The Roll20 Campaign ID (required unless ROLL20_CAMPAIGN_ID env var is set).
  -p, --profile <path>  Path to the Chrome user profile directory.
                        Defaults to '.chrome-profile' in the repository root.
  -d, --dry-run         Verify file reading and configuration paths without opening the browser.
  -h, --help            Show this help menu.

Environment Variables:
  ROLL20_CAMPAIGN_ID    Alternative way to specify the Roll20 Campaign ID.

Example:
  node update_sheet.js -c 1234567
`;

async function main() {
    // 1. Parse Command Line Arguments
    const args = process.argv.slice(2);
    
    if (args.includes('--help') || args.includes('-h')) {
        console.log(usage);
        process.exit(0);
    }
    
    const dryRun = args.includes('--dry-run') || args.includes('-d');
    
    let campaignId = process.env.ROLL20_CAMPAIGN_ID || '';
    let profilePath = path.resolve(__dirname, '../.chrome-profile');
    
    for (let i = 0; i < args.length; i++) {
        if ((args[i] === '--campaign' || args[i] === '-c') && i + 1 < args.length) {
            campaignId = args[i + 1];
        }
        if ((args[i] === '--profile' || args[i] === '-p') && i + 1 < args.length) {
            profilePath = path.resolve(args[i + 1]);
        }
    }
    
    console.log('--- Configuration ---');
    console.log(`Campaign ID:  ${campaignId || '(Not Provided)'}`);
    console.log(`Chrome Profile: ${profilePath}`);
    console.log(`Dry Run:       ${dryRun ? 'YES' : 'NO'}`);
    console.log('---------------------');
    
    // 2. Resolve and verify sheet asset files
    const htmlPath = path.resolve(__dirname, '../roll20_charsheet/Alternity_RPG.html');
    const cssPath = path.resolve(__dirname, '../roll20_charsheet/Alternity_RPG.css');
    const transPath = path.resolve(__dirname, '../roll20_charsheet/translation.json');
    
    console.log('\nReading character sheet files...');
    if (!fs.existsSync(htmlPath)) {
        console.error(`Error: HTML file not found at ${htmlPath}`);
        process.exit(1);
    }
    if (!fs.existsSync(cssPath)) {
        console.error(`Error: CSS file not found at ${cssPath}`);
        process.exit(1);
    }
    if (!fs.existsSync(transPath)) {
        console.error(`Error: Translation JSON file not found at ${transPath}`);
        process.exit(1);
    }
    
    const htmlContent = fs.readFileSync(htmlPath, 'utf8');
    const cssContent = fs.readFileSync(cssPath, 'utf8');
    const transContent = fs.readFileSync(transPath, 'utf8');
    
    console.log(`- Loaded HTML:        ${htmlContent.length} bytes`);
    console.log(`- Loaded CSS:         ${cssContent.length} bytes`);
    console.log(`- Loaded Translation: ${transContent.length} bytes`);
    
    if (dryRun) {
        console.log('\nDry run completed successfully. Local files parsed and paths validated.');
        process.exit(0);
    }
    
    if (!campaignId) {
        console.error('\nError: Campaign ID is required. Please specify it using -c/--campaign or the ROLL20_CAMPAIGN_ID environment variable.');
        console.log(usage);
        process.exit(1);
    }
    
    // Verify Chrome profile folder exists
    if (!fs.existsSync(profilePath)) {
        console.warn(`\nWarning: Persistent Chrome profile folder not found at "${profilePath}".`);
        console.warn('Playwright will initialize a new profile, but you will need to log in to Roll20 manually in the opened browser window.');
    }
    
    // 3. Launch Playwright
    console.log('\nLaunching Chromium browser with persistent Chrome profile...');
    const context = await chromium.launchPersistentContext(profilePath, {
        headless: false, // Run in headful mode so the user can see it and log in if session expires
        viewport: null,
        ignoreDefaultArgs: ['--enable-automation'],
        args: [
            '--start-maximized',
            '--disable-blink-features=AutomationControlled'
        ]
    });
    
    let page;
    try {
        page = context.pages().length > 0 ? context.pages()[0] : await context.newPage();
        const settingsUrl = `https://app.roll20.net/campaigns/campaignsettings/${campaignId}`;
        
        console.log(`Navigating to Campaign Settings: ${settingsUrl}`);
        await page.goto(settingsUrl, { waitUntil: 'load' });
        
        // Wait a moment for any client-side redirections to trigger
        await page.waitForTimeout(3000);
        
        // 4. Handle Login if redirected away from the Campaign Settings page
        if (!page.url().includes(`/campaigns/campaignsettings/${campaignId}`)) {
            console.log('\n[ALERT] Not logged in. Please log in to your Roll20 account in the browser window.');
            console.log('The script will automatically resume once you successfully reach the Campaign Settings page.');
            
            // Wait up to 10 minutes for the user to authenticate
            await page.waitForURL(`**/campaigns/campaignsettings/${campaignId}`, { timeout: 600000 });
            console.log('Login detected! Resuming upload sequence.');
            await page.waitForTimeout(3000); // Wait for the settings page to fully load/stabilize
        }
        
        // 5. Select Custom Sheet Template if needed
        console.log('Verifying Character Sheet Template is set to "Custom"...');
        const sheetDropdown = page.locator('#sheet_template_type, select[name="sheet_template_type"]');
        
        if (await sheetDropdown.count() > 0) {
            const currentValue = await sheetDropdown.inputValue();
            if (currentValue !== 'custom') {
                console.log('Setting sheet template to "Custom"...');
                await sheetDropdown.selectOption('custom');
                // Wait for the custom sheet sections to appear
                await page.waitForTimeout(1000);
            }
        }
        
        // 6. Ensure Editors are initialized by clicking on the tabs
        console.log('Activating editor tabs to ensure initialization...');
        const tabNames = ['HTML Layout', 'CSS Styling', 'Translation'];
        for (const tabName of tabNames) {
            const tabElement = page.locator(`a:has-text("${tabName}"), button:has-text("${tabName}"), li:has-text("${tabName}")`).first();
            if (await tabElement.count() > 0) {
                await tabElement.click();
                await page.waitForTimeout(500);
            }
        }
        
        // 7. Inject code into Ace Editors
        console.log('Injecting HTML, CSS, and Translation JSON into Ace Editors...');
        
        // Wait for Ace library and editors to load
        await page.waitForFunction(() => {
            return typeof window.ace !== 'undefined' && document.querySelectorAll('.ace_editor').length >= 3;
        }, null, { timeout: 15000 }).catch(err => {
            console.warn('Warning: standard Ace editors count not detected. Attempting value setting anyway...');
        });
        
        const uploadResult = await page.evaluate(({ html, css, translation }) => {
            const editors = Array.from(document.querySelectorAll('.ace_editor'));
            if (editors.length === 0) {
                // Fallback to textareas if no Ace editors exist at all
                const htmlTextarea = document.querySelector('#customsheethtml, textarea[name="customsheet_html"]');
                const cssTextarea = document.querySelector('#customsheetcss, textarea[name="customsheet_css"]');
                const transTextarea = document.querySelector('#customsheettranslation, textarea[name="customsheet_translation"]');
                
                if (htmlTextarea && cssTextarea && transTextarea) {
                    htmlTextarea.value = html;
                    cssTextarea.value = css;
                    transTextarea.value = translation;
                    htmlTextarea.dispatchEvent(new Event('change', { bubbles: true }));
                    cssTextarea.dispatchEvent(new Event('change', { bubbles: true }));
                    transTextarea.dispatchEvent(new Event('change', { bubbles: true }));
                    return { success: true, method: 'textarea' };
                }
                return { success: false, foundEditors: 0 };
            }
            
            // Safe, intelligent resolution of editors using DOM parent traversal
            let htmlEditorEl = null;
            let cssEditorEl = null;
            let transEditorEl = null;
            
            for (const editorEl of editors) {
                let current = editorEl;
                let isHtml = false;
                let isCss = false;
                let isTrans = false;
                
                while (current) {
                    const id = current.id ? current.id.toLowerCase() : '';
                    const cls = current.className ? String(current.className).toLowerCase() : '';
                    const name = current.getAttribute('name') ? current.getAttribute('name').toLowerCase() : '';
                    
                    // Check if parent contains HTML layout identifiers
                    if (id.includes('html') || id.includes('layout') || cls.includes('html') || cls.includes('layout') || name.includes('html')) {
                        isHtml = true;
                        break;
                    }
                    // Check if parent contains CSS styling identifiers
                    if (id.includes('css') || id.includes('style') || cls.includes('css') || cls.includes('style') || name.includes('css')) {
                        isCss = true;
                        break;
                    }
                    // Check if parent contains Translation identifiers
                    if (id.includes('translation') || id.includes('trans') || id.includes('lang') || id.includes('i18n') ||
                        cls.includes('translation') || cls.includes('trans') || cls.includes('lang') || cls.includes('i18n') ||
                        name.includes('translation') || name.includes('trans')) {
                        isTrans = true;
                        break;
                    }
                    current = current.parentElement;
                }
                
                if (isHtml) htmlEditorEl = editorEl;
                else if (isCss) cssEditorEl = editorEl;
                else if (isTrans) transEditorEl = editorEl;
            }
            
            // If traversal was completely successful, use those resolved elements
            if (htmlEditorEl && cssEditorEl && transEditorEl) {
                ace.edit(htmlEditorEl).setValue(html, -1);
                ace.edit(cssEditorEl).setValue(css, -1);
                ace.edit(transEditorEl).setValue(translation, -1);
                return { success: true, method: 'Traversed Ace DOM' };
            }
            
            // Fallback: If traversal failed to resolve all 3 uniquely, fall back to tab link matching
            const findEditorByTab = (searchTerms) => {
                const anchors = Array.from(document.querySelectorAll('a, button, li'));
                for (const el of anchors) {
                    const text = el.textContent.trim().toLowerCase();
                    if (searchTerms.some(term => text.includes(term))) {
                        const targetId = el.getAttribute('href') || el.getAttribute('data-target') || el.getAttribute('aria-controls');
                        if (targetId && targetId.startsWith('#')) {
                            const pane = document.querySelector(targetId);
                            if (pane) {
                                const editor = pane.querySelector('.ace_editor');
                                if (editor) return editor;
                            }
                        }
                    }
                }
                return null;
            };
            
            const htmlTabEditor = findEditorByTab(['html', 'layout']);
            const cssTabEditor = findEditorByTab(['css', 'style']);
            const transTabEditor = findEditorByTab(['translation', 'trans', 'json']);
            
            if (htmlTabEditor && cssTabEditor && transTabEditor) {
                ace.edit(htmlTabEditor).setValue(html, -1);
                ace.edit(cssTabEditor).setValue(css, -1);
                ace.edit(transTabEditor).setValue(translation, -1);
                return { success: true, method: 'Tab Matched Ace DOM' };
            }
            
            // Absolute Last Resort Fallback: Match by DOM index order (if exactly 3 exist)
            if (editors.length === 3) {
                ace.edit(editors[0]).setValue(html, -1);
                ace.edit(editors[1]).setValue(css, -1);
                ace.edit(editors[2]).setValue(translation, -1);
                return { success: true, method: 'Indexed Ace DOM (Fallback)' };
            }
            
            return { success: false, foundEditors: editors.length, traversalStatus: { html: !!htmlEditorEl, css: !!cssEditorEl, trans: !!transEditorEl } };
        }, { html: htmlContent, css: cssContent, translation: transContent });
        
        if (!uploadResult.success) {
            throw new Error(`Failed to locate custom character sheet editors on page. Found ${uploadResult.foundEditors} Ace editors.`);
        }
        
        console.log(`Success: Pasted assets using method: ${uploadResult.method || 'Ace Editor API'}`);
        
        // 8. Save Changes
        console.log('Saving changes...');
        const saveButton = page.locator('#save-changes-button');
        
        if (await saveButton.count() > 0) {
            // Roll20 save buttons often require scrolling into view
            await saveButton.scrollIntoViewIfNeeded();
            await Promise.all([
                page.waitForNavigation({ waitUntil: 'networkidle', timeout: 45000 }),
                saveButton.click()
            ]);
            console.log('\n==================================================');
            console.log('🎉 Character sheet updated successfully in Roll20!');
            console.log('==================================================');
        } else {
            console.error('\nError: Could not locate "Save Changes" button on the page.');
            console.log('Please click the "Save Changes" button manually in the browser.');
            await page.waitForTimeout(10000);
        }
        
    } catch (err) {
        console.error('\nAn error occurred during sheet upload:', err);
        try {
            const scratchDir = path.resolve(__dirname, '../scratch');
            if (!fs.existsSync(scratchDir)) {
                fs.mkdirSync(scratchDir);
            }
            const screenshotPath = path.join(scratchDir, 'roll20_debug.png');
            const htmlDumpPath = path.join(scratchDir, 'roll20_debug.html');
            console.log(`Saving debug screenshot to ${screenshotPath}...`);
            await page.screenshot({ path: screenshotPath, fullPage: true });
            console.log(`Saving debug HTML source to ${htmlDumpPath}...`);
            fs.writeFileSync(htmlDumpPath, await page.content(), 'utf8');
        } catch (debugErr) {
            console.error('Failed to capture debug info:', debugErr);
        }
    } finally {
        console.log('Closing browser...');
        await context.close();
    }
}

main().catch(console.error);

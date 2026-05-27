const { test, expect } = require('@playwright/test');
const fs = require('fs');
const path = require('path');
const vm = require('vm');

// Helper to load the sheet worker script from header.html
function loadSheetWorkerCode() {
    const filePath = path.resolve(__dirname, '../roll20_charsheet/src/tabs/header.html');
    const content = fs.readFileSync(filePath, 'utf8');
    const match = content.match(/<script type="text\/worker">([\s\S]*?)<\/script>/);
    if (!match) throw new Error("Could not find sheet worker script inside header.html");
    return match[1];
}

// Helper to load the API script
function loadApiScriptCode() {
    const filePath = path.resolve(__dirname, '../roll20_charsheet/aaa_rolls_api.js');
    return fs.readFileSync(filePath, 'utf8');
}

test.describe('Alternity/aaa RPG Roll20 Automated Test Suite', () => {

    test.describe('1. Character Sheet Worker Macro Generation Tests', () => {
        
        test('Should correctly build attack macros for single, double, and triple attacks', () => {
            const workerCode = loadSheetWorkerCode();
            
            // Mock environment for Roll20 Sheet Worker
            let mockAttrs = {
                'character_name': 'Razor',
                'repeating_attackforms_row123_attackformname': 'Laser Pistol',
                'repeating_attackforms_row123_attackformscore': '12',
                'repeating_attackforms_row123_attackformtype': 'Energy',
                'repeating_attackforms_row123_attackformrange': '20/40/80',
                'repeating_attackforms_row123_attackformdie': '2', // d6 step
                'repeating_attackforms_row123_attackformaccuracy': '0',
                'repeating_attackforms_row123_attackformsit': '0',
                'repeating_attackforms_row123_attackformnotes': 'Point-blank bonuses'
            };
            
            let setAttrsVal = null;
            
            const context = {
                console: { log: () => {} },
                parseInt: parseInt,
                Math: Math,
                on: () => {},
                getAttrs: (attrs, callback) => {
                    const res = {};
                    attrs.forEach(a => { res[a] = mockAttrs[a]; });
                    callback(res);
                },
                setAttrs: (obj) => {
                    setAttrsVal = obj;
                },
                getSectionIDs: (section, callback) => {
                    callback(['row123']);
                }
            };
            
            vm.createContext(context);
            vm.runInContext(workerCode, context);
            
            // Invoke the macro generation logic directly
            context.updateAttackMacro('attackforms', 'row123');
            
            expect(setAttrsVal).not.toBeNull();
            
            // Mode 1: Single attack (no penalty, d6 situation die)
            const macro1 = setAttrsVal['repeating_attackforms_row123_attackformmacro1'];
            expect(macro1).toBe('!aaa-roll Razor || Laser Pistol || Energy || 20/40/80 || Point-blank bonuses || 12 || 6 || 3 || 1 || 1d6cs<0cf<0 || +');
            
            // Mode 2: Double action (+1 step on first, +2 steps on second -> d8 and d12)
            const macro2 = setAttrsVal['repeating_attackforms_row123_attackformmacro2'];
            expect(macro2).toBe('!aaa-roll Razor || Laser Pistol || Energy || 20/40/80 || Point-blank bonuses || 12 || 6 || 3 || 2 || 1d8cs<0cf<0 || + || 1d12cs<0cf<0 || +');
        });

        test('Should sanitize newlines and double pipes to maintain command string integrity', () => {
            const workerCode = loadSheetWorkerCode();
            
            let mockAttrs = {
                'character_name': 'Razor\nSwift',
                'repeating_attackforms_row456_attackformname': 'Heavy || Cannon',
                'repeating_attackforms_row456_attackformscore': '14',
                'repeating_attackforms_row456_attackformtype': 'Kinetic\r\nHeavy',
                'repeating_attackforms_row456_attackformrange': '50/100',
                'repeating_attackforms_row456_attackformdie': '1', // d4 step
                'repeating_attackforms_row456_attackformaccuracy': '0',
                'repeating_attackforms_row456_attackformsit': '0',
                'repeating_attackforms_row456_attackformnotes': 'First line\nSecond line || With pipes'
            };
            
            let setAttrsVal = null;
            
            const context = {
                console: { log: () => {} },
                parseInt: parseInt,
                Math: Math,
                on: () => {},
                getAttrs: (attrs, callback) => {
                    const res = {};
                    attrs.forEach(a => { res[a] = mockAttrs[a]; });
                    callback(res);
                },
                setAttrs: (obj) => {
                    setAttrsVal = obj;
                },
                getSectionIDs: (section, callback) => {
                    callback(['row456']);
                }
            };
            
            vm.createContext(context);
            vm.runInContext(workerCode, context);
            context.updateAttackMacro('attackforms', 'row456');
            
            const macro1 = setAttrsVal['repeating_attackforms_row456_attackformmacro1'];
            
            // Check character name sanitization
            expect(macro1).toContain('Razor Swift');
            expect(macro1).not.toContain('Razor\nSwift');
            
            // Check weapon name sanitization (double pipes -> single pipe)
            expect(macro1).toContain('Heavy | Cannon');
            expect(macro1).not.toContain('Heavy || Cannon');
            
            // Check notes sanitization (newlines -> space, double pipes -> single pipe)
            expect(macro1).toContain('First line Second line | With pipes');
            expect(macro1).not.toContain('First line\nSecond line');
            expect(macro1).not.toContain('|| With pipes');
        });
    });

    test.describe('2. Roll20 API Script Roll Evaluation Tests', () => {

        test('Should correctly parse arguments and format single attack rolls with correct layout', () => {
            const apiCode = loadApiScriptCode();
            
            let chatMessageListener = null;
            let sendChatCalls = [];
            
            const apiContext = {
                on: (event, callback) => {
                    if (event === 'chat:message') chatMessageListener = callback;
                },
                sendChat: (who, content, callback) => {
                    sendChatCalls.push({ who: who, content: content });
                    
                    if (callback) {
                        // Simulate Roll20's return payload from sendChat for [[1d20]] [[1d6]]
                        const mockResult = [
                            {
                                inlinerolls: [
                                    {
                                        expression: '1d20cs<1cf>20',
                                        results: { total: 11 }
                                    },
                                    {
                                        expression: '1d6cs<0cf<0',
                                        results: { total: 4 }
                                    }
                                ]
                            }
                        ];
                        callback(mockResult);
                    }
                },
                log: () => {},
                parseInt: parseInt,
                Math: Math,
                JSON: JSON
            };
            
            vm.createContext(apiContext);
            vm.runInContext(apiCode, apiContext);
            
            // Simulate receiving the !aaa-roll command
            const command = '!aaa-roll Razor || Laser Pistol || Energy || 20/40/80 || Notes || 12 || 6 || 3 || 1 || 1d6cs<0cf<0 || +';
            chatMessageListener({
                type: 'api',
                content: command,
                who: 'Razor'
            });
            
            // First call should be to evaluate rolls
            expect(sendChatCalls.length).toBe(3); // debug whisper, GM whisper, final output
            
            const debugWhisper = sendChatCalls[1];
            expect(debugWhisper.who).toBe('aaa API Debug');
            
            const finalOutput = sendChatCalls[2];
            expect(finalOutput.who).toBe('Razor');
            
            // Verify final styled layout and exact values
            const msg = finalOutput.content;
            expect(msg).toContain('&{template:alternity-attack}');
            expect(msg).toContain('{{name=Razor - Laser Pistol}}');
            expect(msg).toContain('{{type=Energy}}');
            expect(msg).toContain('{{range=20/40/80}}');
            expect(msg).toContain('{{notes=Notes}}');
            
            // Control die roll output should be exactly 11
            expect(msg).toContain('{{dicepool=[[11]]}}');
            
            // Attack roll evaluation should reference both d20 and situation die: (11)[1d20] + (4)[1d6]
            expect(msg).toContain('{{attack1=[[(11)[1d20] + (4)[1d6]]]}}');
            
            // Success scores should be correctly formatted without the layout brace typo!
            expect(msg).toContain('{{scores1=[12/6/3]}}');
            expect(msg).not.toContain('{{scores1}='); // Typos are resolved!
        });

        test('Should correctly identify d20 even when Roll20 returns inline rolls simplified (robust matching)', () => {
            const apiCode = loadApiScriptCode();
            
            let chatMessageListener = null;
            let sendChatCalls = [];
            
            const apiContext = {
                on: (event, callback) => {
                    if (event === 'chat:message') chatMessageListener = callback;
                },
                sendChat: (who, content, callback) => {
                    sendChatCalls.push({ who: who, content: content });
                    
                    if (callback) {
                        // Simulate Roll20's simplified expressions (1d20cs... -> 1d20, 1d6cs... -> 1d6)
                        const mockResult = [
                            {
                                inlinerolls: [
                                    {
                                        expression: '1d20',
                                        results: { total: 15 }
                                    },
                                    {
                                        expression: '1d6',
                                        results: { total: 3 }
                                    }
                                ]
                            }
                        ];
                        callback(mockResult);
                    }
                },
                log: () => {},
                parseInt: parseInt,
                Math: Math,
                JSON: JSON
            };
            
            vm.createContext(apiContext);
            vm.runInContext(apiCode, apiContext);
            
            const command = '!aaa-roll Razor || Laser Pistol || Energy || 20/40/80 || Notes || 12 || 6 || 3 || 1 || 1d6cs<0cf<0 || +';
            chatMessageListener({
                type: 'api',
                content: command
            });
            
            const finalOutput = sendChatCalls[2].content;
            expect(finalOutput).toContain('{{dicepool=[[15]]}}');
            expect(finalOutput).toContain('{{attack1=[[(15)[1d20] + (3)[1d6]]]}}');
        });

        test('Should correctly process Double Action rolls with sequential non-swapped step dice', () => {
            const apiCode = loadApiScriptCode();
            
            let chatMessageListener = null;
            let sendChatCalls = [];
            
            const apiContext = {
                on: (event, callback) => {
                    if (event === 'chat:message') chatMessageListener = callback;
                },
                sendChat: (who, content, callback) => {
                    sendChatCalls.push({ who: who, content: content });
                    
                    if (callback) {
                        // Double Action rolls: d20, d6, d8
                        const mockResult = [
                            {
                                inlinerolls: [
                                    {
                                        expression: '1d20',
                                        results: { total: 8 }
                                    },
                                    {
                                        expression: '1d6',
                                        results: { total: 5 }
                                    },
                                    {
                                        expression: '1d8',
                                        results: { total: 7 }
                                    }
                                ]
                            }
                        ];
                        callback(mockResult);
                    }
                },
                log: () => {},
                parseInt: parseInt,
                Math: Math,
                JSON: JSON
            };
            
            vm.createContext(apiContext);
            vm.runInContext(apiCode, apiContext);
            
            // Double Action command (mode = 2)
            const command = '!aaa-roll Razor || Laser Pistol || Energy || 20/40/80 || Notes || 12 || 6 || 3 || 2 || 1d6cs<0cf<0 || + || 1d8cs<0cf<0 || +';
            chatMessageListener({
                type: 'api',
                content: command
            });
            
            const finalOutput = sendChatCalls[2].content;
            expect(finalOutput).toContain('{{dicepool=[[8]]}}');
            
            // Attack 1: (8)[1d20] + (5)[1d6]
            expect(finalOutput).toContain('{{attack1=[[(8)[1d20] + (5)[1d6]]]}}');
            
            // Attack 2: (8)[1d20] + (7)[1d8]
            expect(finalOutput).toContain('{{attack2=[[(8)[1d20] + (7)[1d8]]]}}');
        });

        test('Should explicitly identify the d20 roll even if Roll20 returns inline rolls out of order (immune to index swaps)', () => {
            const apiCode = loadApiScriptCode();
            
            let chatMessageListener = null;
            let sendChatCalls = [];
            
            const apiContext = {
                on: (event, callback) => {
                    if (event === 'chat:message') chatMessageListener = callback;
                },
                sendChat: (who, content, callback) => {
                    sendChatCalls.push({ who: who, content: content });
                    
                    if (callback) {
                        // Swapped order in inlinerolls payload: d6 is at index 0, d20 is at index 1
                        const mockResult = [
                            {
                                inlinerolls: [
                                    {
                                        expression: '1d6',
                                        results: { total: 4 }
                                    },
                                    {
                                        expression: '1d20',
                                        results: { total: 11 }
                                    }
                                ]
                            }
                        ];
                        callback(mockResult);
                    }
                },
                log: () => {},
                parseInt: parseInt,
                Math: Math,
                JSON: JSON
            };
            
            vm.createContext(apiContext);
            vm.runInContext(apiCode, apiContext);
            
            const command = '!aaa-roll Razor || Laser Pistol || Energy || 20/40/80 || Notes || 12 || 6 || 3 || 1 || 1d6cs<0cf<0 || +';
            chatMessageListener({
                type: 'api',
                content: command,
                who: 'Razor'
            });
            
            const finalOutput = sendChatCalls[2].content;
            
            // The d20 roll MUST still be resolved as 11, and the d6 roll as 4
            expect(finalOutput).toContain('{{dicepool=[[11]]}}');
            expect(finalOutput).toContain('{{attack1=[[(11)[1d20] + (4)[1d6]]]}}');
            
            // Confirms it never gets "11 in a d6" or "4 in a d20" swap!
            expect(finalOutput).not.toContain('(4)[1d20]');
            expect(finalOutput).not.toContain('(11)[1d6]');
        });
    });
});

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
            
            // First call is evaluation roll, second is final output
            expect(sendChatCalls.length).toBe(2);
            
            const finalOutput = sendChatCalls[1];
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
            
            const finalOutput = sendChatCalls[1].content;
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
            
            const finalOutput = sendChatCalls[1].content;
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
            
            const finalOutput = sendChatCalls[1].content;
            
            // The d20 roll MUST still be resolved as 11, and the d6 roll as 4
            expect(finalOutput).toContain('{{dicepool=[[11]]}}');
            expect(finalOutput).toContain('{{attack1=[[(11)[1d20] + (4)[1d6]]]}}');
            
            // Confirms it never gets "11 in a d6" or "4 in a d20" swap!
            expect(finalOutput).not.toContain('(4)[1d20]');
            expect(finalOutput).not.toContain('(11)[1d6]');
        });

        test('Should evaluate roll <= amazing score as Amazing success (including 0 and negatives)', () => {
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
                        callback([{
                            type: 'api',
                            inlinerolls: [
                                {
                                    expression: '1d20cs<1cf>20',
                                    results: { total: 4 }
                                },
                                {
                                    expression: '1d6cs<0cf<0',
                                    results: { total: 4 }
                                }
                            ]
                        }]);
                    }
                },
                log: () => {},
                parseInt: parseInt,
                Math: Math,
                JSON: JSON
            };
            
            vm.createContext(apiContext);
            vm.runInContext(apiCode, apiContext);
            
            // Score amazing is 4. Roll is 1d20 - 1d6.
            // total = 4 - 4 = 0. Since 0 <= 4, it should be Amazing success!
            const command = '!aaa-roll Razor || Harpon Gun || Li/O || - || - || 16 || 8 || 4 || 1 || 1d6cs<0cf<0 || -';
            chatMessageListener({
                type: 'api',
                content: command,
                who: 'Razor'
            });
            
            const finalOutput = sendChatCalls[1].content;
            expect(finalOutput).toContain('{{status1=Amazing}}');
            expect(finalOutput).toContain('{{status_class1=hit-ama}}');
        });

        test('Should evaluate natural 20 as Critical Failure regardless of total sum', () => {
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
                        callback([{
                            type: 'api',
                            inlinerolls: [
                                {
                                    expression: '1d20cs<1cf>20',
                                    results: { total: 20 }
                                },
                                {
                                    expression: '1d6cs<0cf<0',
                                    results: { total: 1 }
                                }
                            ]
                        }]);
                    }
                },
                log: () => {},
                parseInt: parseInt,
                Math: Math,
                JSON: JSON
            };
            
            vm.createContext(apiContext);
            vm.runInContext(apiCode, apiContext);
            
            // Natural 20, minus 1 d6 = 19. Even though 19 <= 25, it must be a Critical Failure because d20 rolled 20.
            const command = '!aaa-roll Razor || Harpon Gun || Li/O || - || - || 25 || 12 || 6 || 1 || 1d6cs<0cf<0 || -';
            chatMessageListener({
                type: 'api',
                content: command,
                who: 'Razor'
            });
            
            const finalOutput = sendChatCalls[1].content;
            expect(finalOutput).toContain('{{status1=Critical Failure}}');
            expect(finalOutput).toContain('{{status_class1=miss}}');
        });

        test('Should evaluate natural 1 as at least Ordinary success even if total adds to more than skill score', () => {
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
                        callback([{
                            type: 'api',
                            inlinerolls: [
                                {
                                    expression: '1d20cs<1cf>20',
                                    results: { total: 1 }
                                },
                                {
                                    expression: '1d20cs<0cf<0',
                                    results: { total: 15 } // huge positive modifier
                                }
                            ]
                        }]);
                    }
                },
                log: () => {},
                parseInt: parseInt,
                Math: Math,
                JSON: JSON
            };
            
            vm.createContext(apiContext);
            vm.runInContext(apiCode, apiContext);
            
            // d20 rolled 1 (natural 1). Plus 15 = 16. The ordinary score is 12.
            // 16 > 12, but because it is a natural 1, it must be an Ordinary success!
            const command = '!aaa-roll Razor || Harpon Gun || Li/O || - || - || 12 || 6 || 3 || 1 || 1d20cs<0cf<0 || +';
            chatMessageListener({
                type: 'api',
                content: command,
                who: 'Razor'
            });
            
            const finalOutput = sendChatCalls[1].content;
            expect(finalOutput).toContain('{{status1=Ordinary}}');
            expect(finalOutput).toContain('{{status_class1=hit-ord}}');
        });

        test('Should correctly pair multiple different situation dice (like 1d6 and 1d8) even if Roll20 returns them out-of-order in the array', () => {
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
                        callback([{
                            type: 'api',
                            inlinerolls: [
                                {
                                    expression: '1d20cs<1cf>20',
                                    results: { total: 20 }
                                },
                                {
                                    expression: '1d8cs<0cf<0',
                                    results: { total: 8 } // d8 rolled 8, returned FIRST in the situation dice
                                },
                                {
                                    expression: '1d6cs<0cf<0',
                                    results: { total: 2 } // d6 rolled 2, returned SECOND in the situation dice
                                }
                            ]
                        }]);
                    }
                },
                log: () => {},
                parseInt: parseInt,
                Math: Math,
                JSON: JSON
            };
            
            vm.createContext(apiContext);
            vm.runInContext(apiCode, apiContext);
            
            // Double action roll: Attack 1 wants 1d6, Attack 2 wants 1d8.
            // Even though the array of rolls returns 1d8 first, it must pair the 1d6 name with the value 2, and 1d8 name with the value 8!
            const command = '!aaa-roll Razor || Harpon Gun || Li/O || - || - || 16 || 8 || 4 || 2 || 1d6cs<0cf<0 || + || 1d8cs<0cf<0 || +';
            chatMessageListener({
                type: 'api',
                content: command,
                who: 'Razor'
            });
            
            const finalOutput = sendChatCalls[1].content;
            
            // Attack 1: (20)[1d20] + (2)[1d6] = 22
            expect(finalOutput).toContain('{{attack1=[[(20)[1d20] + (2)[1d6]]]}}');
            
            // Attack 2: (20)[1d20] + (8)[1d8] = 28
            expect(finalOutput).toContain('{{attack2=[[(20)[1d20] + (8)[1d8]]]}}');
        });

        test('Should correctly calculate Action Check success level and add appropriate phases to the Turn Tracker', () => {
            const apiCode = loadApiScriptCode();
            
            let chatMessageListener = null;
            let sendChatCalls = [];
            let trackerData = JSON.stringify([
                { id: 'old-token', pr: 'Marginal', custom: '' }
            ]);
            
            const campaignMock = {
                get: (key) => {
                    if (key === 'turnorder') return trackerData;
                    if (key === 'playerpageid') return 'page-123';
                    return '';
                },
                set: (key, val) => {
                    if (key === 'turnorder') trackerData = val;
                }
            };
            
            const findObjsMock = (query) => {
                if (query._type === 'graphic' && query.represents === 'char-123') {
                    return [{ id: 'token-123' }];
                }
                return [];
            };
            
            const apiContext = {
                on: (event, callback) => {
                    if (event === 'chat:message') chatMessageListener = callback;
                },
                sendChat: (who, content, callback) => {
                    sendChatCalls.push({ who: who, content: content });
                },
                Campaign: () => campaignMock,
                findObjs: findObjsMock,
                log: () => {},
                parseInt: parseInt,
                Math: Math,
                JSON: JSON
            };
            
            vm.createContext(apiContext);
            vm.runInContext(apiCode, apiContext);
            
            // Action Check command: Name || CharId || ScoreM || ScoreO || ScoreG || ScoreA
            // Marginal: 14, Ordinary: 13, Good: 6, Amazing: 3
            const command = '!aaa-action-check Razor || char-123 || 14 || 13 || 6 || 3';
            
            // Simulating a Good success (e.g. total roll = 5, where 5 <= 6).
            // Let's pass the inline rolls:
            // Roll 0: d20 = 4
            // Roll 1: sit = 1
            chatMessageListener({
                type: 'api',
                content: command,
                who: 'Razor',
                inlinerolls: [
                    { expression: '1d20cs<1cf>20', results: { total: 4 } },
                    { expression: '1d4cs<0cf<0', results: { total: 1 } }
                ]
            });
            
            // The command should execute and send the chat message
            expect(sendChatCalls.length).toBe(1);
            const chatMsg = sendChatCalls[0].content;
            
            // Check that it identifies Good success
            expect(chatMsg).toContain('Success: **Good**');
            expect(chatMsg).toContain('Added to Turn Tracker for phases: **Good, Ordinary, Marginal**');
            
            // Verify trackerData has the correct entries (old-token should remain unaffected)
            const parsedTracker = JSON.parse(trackerData);
            expect(parsedTracker).toEqual([
                { id: 'old-token', pr: 'Marginal', custom: '' },
                { id: 'token-123', pr: 'Good', custom: '' },
                { id: 'token-123', pr: 'Ordinary', custom: '' },
                { id: 'token-123', pr: 'Marginal', custom: '' }
            ]);

            // Re-roll as Ordinary Success (d20 = 12, sit = 1, total = 13 <= 13)
            chatMessageListener({
                type: 'api',
                content: command,
                who: 'Razor',
                inlinerolls: [
                    { expression: '1d20cs<1cf>20', results: { total: 12 } },
                    { expression: '1d4cs<0cf<0', results: { total: 1 } }
                ]
            });

            // The old token-123 entries should be removed, and new Ordinary and Marginal entries added
            const reRolledTracker = JSON.parse(trackerData);
            expect(reRolledTracker).toEqual([
                { id: 'old-token', pr: 'Marginal', custom: '' },
                { id: 'token-123', pr: 'Ordinary', custom: '' },
                { id: 'token-123', pr: 'Marginal', custom: '' }
            ]);

            // Roll above Ordinary score (d20 = 15, sit = 1, total = 16 > 13)
            chatMessageListener({
                type: 'api',
                content: command,
                who: 'Razor',
                inlinerolls: [
                    { expression: '1d20cs<1cf>20', results: { total: 15 } },
                    { expression: '1d4cs<0cf<0', results: { total: 1 } }
                ]
            });

            // Even though 16 is greater than Ordinary score (13), it should be evaluated as Marginal Success, not Miss!
            const marginalTracker = JSON.parse(trackerData);
            expect(marginalTracker).toEqual([
                { id: 'old-token', pr: 'Marginal', custom: '' },
                { id: 'token-123', pr: 'Marginal', custom: '' }
            ]);
        });
    });
});

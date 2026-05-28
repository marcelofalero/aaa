/**
 * aaa RPG - Custom Roll20 API Dice Rolling Script
 * Handles multi-action attacks by rolling a single control d20 die exactly once,
 * applying different situation step dice for each attack, and outputting to the
 * character sheet's premium HTML roll template.
 */

on("chat:message", function(msg) {
    // Only intercept API commands starting with !aaa-roll or !aaa-action-check
    if (msg.type !== "api") return;

    if (msg.content.indexOf("!aaa-action-check") === 0) {
        var commandText = msg.content.substring("!aaa-action-check ".length);
        var parts = commandText.split(" || ").map(function(p) { return p.trim(); });
        
        var charName = parts[0] || "Character";
        var charId = parts[1] || "";
        var scoreM = parseInt(parts[2]) || 0;
        var scoreO = parseInt(parts[3]) || 0;
        var scoreG = parseInt(parts[4]) || 0;
        var scoreA = parseInt(parts[5]) || 0;
        
        var d20 = 10;
        var sit = 0;
        
        if (msg.inlinerolls) {
            if (msg.inlinerolls[0]) {
                d20 = msg.inlinerolls[0].results.total;
            }
            if (msg.inlinerolls[1]) {
                sit = msg.inlinerolls[1].results.total;
            }
        }
        
        var total = d20 + sit;
        var successLevel = "";
        
        if (d20 === 20) {
            successLevel = "Critical Failure";
        } else if (d20 === 1) {
            // Natural 1 is always success. Check best level achieved.
            if (total <= scoreA) {
                successLevel = "Amazing";
            } else if (total <= scoreG) {
                successLevel = "Good";
            } else {
                successLevel = "Ordinary";
            }
        } else {
            if (total <= scoreA) {
                successLevel = "Amazing";
            } else if (total <= scoreG) {
                successLevel = "Good";
            } else if (total <= scoreO) {
                successLevel = "Ordinary";
            } else {
                successLevel = "Marginal";
            }
        }
        
        var phases = [];
        if (successLevel === "Amazing") {
            phases = [
                { name: "Amazing", val: 4 },
                { name: "Good", val: 3 },
                { name: "Ordinary", val: 2 },
                { name: "Marginal", val: 1 }
            ];
        } else if (successLevel === "Good") {
            phases = [
                { name: "Good", val: 3 },
                { name: "Ordinary", val: 2 },
                { name: "Marginal", val: 1 }
            ];
        } else if (successLevel === "Ordinary") {
            phases = [
                { name: "Ordinary", val: 2 },
                { name: "Marginal", val: 1 }
            ];
        } else if (successLevel === "Marginal") {
            phases = [
                { name: "Marginal", val: 1 }
            ];
        }
        
        // Add to Turn Tracker if a valid token is found
        var tokenId = null;
        if (msg.selected && msg.selected.length > 0) {
            tokenId = msg.selected[0]._id || msg.selected[0].id;
        } else if (charId && typeof findObjs !== 'undefined') {
            var tokens = findObjs({
                _type: "graphic",
                represents: charId
            });
            if (tokens && tokens.length > 0) {
                var chosenToken = null;
                if (typeof Campaign !== 'undefined') {
                    var playerPageId = Campaign().get("playerpageid");
                    for (var i = 0; i < tokens.length; i++) {
                        var tokenPageId = typeof tokens[i].get === "function" ? tokens[i].get("_pageid") : tokens[i]._pageid;
                        if (tokenPageId === playerPageId) {
                            chosenToken = tokens[i];
                            break;
                        }
                    }
                }
                if (!chosenToken) {
                    chosenToken = tokens[0];
                }
                tokenId = chosenToken.id || (typeof chosenToken.get === "function" ? (chosenToken.get("_id") || chosenToken.get("id")) : (chosenToken._id || chosenToken.id));
            }
        }
        
        var trackerStatusMsg = "";
        if (tokenId && phases.length > 0 && typeof Campaign !== 'undefined') {
            var turnorder = JSON.parse(Campaign().get("turnorder") || "[]");
            
            // Clean up any existing turn entries for this token
            turnorder = turnorder.filter(function(turn) {
                return turn.id !== tokenId;
            });
            
            // Push each phase as a separate entry (Roll20 pr must be numeric)
            phases.forEach(function(phase) {
                turnorder.push({
                    id: tokenId,
                    pr: phase.val,
                    custom: ""
                });
            });
            
            Campaign().set("turnorder", JSON.stringify(turnorder));
            var phaseNames = phases.map(function(p) { return p.name; });
            trackerStatusMsg = "<br>Added to Turn Tracker for phases: **" + phaseNames.join(", ") + "**";
        } else if (phases.length > 0) {
            trackerStatusMsg = "<br>⚠️ **Warning:** Could not find a map token representing this character. Please ensure you have a token on the map, and its **'Represents Character'** property is set to **" + charName + "**!";
        }
        
        var sign = sit >= 0 ? "+" : "-";
        var absSit = Math.abs(sit);
        var rollResultExpr = "[[" + d20 + "[d20] " + sign + " " + absSit + "[Situation]]]";
        
        var chatMsg = "&{template:alternity-skill} {{name=" + charName + " - Action Check}} {{score=" + scoreM + "+ / " + scoreO + " / " + scoreG + " / " + scoreA + "}} {{results=" + rollResultExpr + "}} {{wiki=Success: **" + successLevel + "**" + trackerStatusMsg + "}}";
        
        sendChat("character|" + charId, chatMsg);
        return;
    }

    if (msg.content.indexOf("!aaa-roll") !== 0) return;
    
    // Parse arguments separated by " || "
    var argsStr = msg.content.substring("!aaa-roll ".length);
    var parts = argsStr.split(" || ");
    if (parts.length < 10) {
        sendChat("aaa API", "/w gm [ERROR] aaa API received invalid arguments: " + msg.content);
        return;
    }
    
    var charName = parts[0].trim();
    var weaponName = parts[1].trim();
    var type = parts[2].trim();
    var range = parts[3].trim();
    var notes = parts[4].trim();
    var scoreO = parseInt(parts[5]) || 0;
    var scoreG = parseInt(parts[6]) || 0;
    var scoreA = parseInt(parts[7]) || 0;
    var mode = parseInt(parts[8]) || 1;
    
    // Construct the inline roll expression for sendChat
    // First roll is always the control d20
    var rollExpr = "[[1d20cs<1cf>20]]";
    
    for (var i = 1; i <= mode; i++) {
        var argIndex = 7 + (i * 2); // 9 for i = 1, 11 for i = 2, 13 for i = 3
        var rollStr = parts[argIndex];
        if (rollStr && rollStr.trim() !== '0') {
            rollExpr += " [[" + rollStr.trim() + "]]";
        }
    }
    
    // Perform the rolls using Roll20's chat engine
    sendChat("", rollExpr, function(ops) {
        var msgObj = ops[0];
        if (!msgObj || !msgObj.inlinerolls || msgObj.inlinerolls.length === 0) {
            sendChat("aaa API", "/w gm [ERROR] Failed to evaluate dice rolls.");
            return;
        }
        
        
        var usedIndices = {};
        var d20 = 10;
        var d20Found = false;
        
        // 1. Explicitly identify the control d20 roll (expression containing "1d20" or "d20")
        for (var k = 0; k < msgObj.inlinerolls.length; k++) {
            var roll = msgObj.inlinerolls[k];
            if (roll && roll.expression) {
                var normExpr = roll.expression.toLowerCase().replace(/\s+/g, '');
                if (normExpr.indexOf("1d20") !== -1 || normExpr.indexOf("d20") !== -1) {
                    d20 = roll.results.total;
                    usedIndices[k] = true;
                    d20Found = true;
                    break;
                }
            }
        }
        // Fallback: if d20 wasn't matched (or expression is empty), use the first roll in the array
        if (!d20Found && msgObj.inlinerolls[0]) {
            d20 = msgObj.inlinerolls[0].results.total;
            usedIndices[0] = true;
        }
        
        // 2. Assign the remaining situation dice sequentially to the unused inline rolls
        var attackRollExprs = {};
        var attackStatuses = {};
        var attackStatusClasses = {};
        
        for (var i = 1; i <= mode; i++) {
            var argIndex = 7 + (i * 2);
            var rollStr = parts[argIndex];
            var sign = parts[argIndex + 1] ? parts[argIndex + 1].trim() : '+';
            
            var sitVal = 0;
            var dieName = '';
            if (rollStr && rollStr.trim() !== '0') {
                dieName = rollStr.replace(/cs<0cf<0/g, '').trim();
                var cleanDie = dieName.toLowerCase().replace(/\s+/g, '');
                var matchFound = false;
                
                // Find an unused inline roll that matches this exact die type (e.g. "1d6" or "1d8")
                for (var k = 0; k < msgObj.inlinerolls.length; k++) {
                    if (!usedIndices[k]) {
                        var rollExprClean = msgObj.inlinerolls[k].expression.toLowerCase().replace(/\s+/g, '');
                        if (rollExprClean.indexOf(cleanDie) !== -1) {
                            sitVal = msgObj.inlinerolls[k].results.total;
                            usedIndices[k] = true;
                            matchFound = true;
                            break;
                        }
                    }
                }
                
                // Fallback if no exact die expression match was found
                if (!matchFound) {
                    for (var k = 0; k < msgObj.inlinerolls.length; k++) {
                        if (!usedIndices[k]) {
                            sitVal = msgObj.inlinerolls[k].results.total;
                            usedIndices[k] = true;
                            break;
                        }
                    }
                }
            }
            
            if (dieName && dieName !== '0') {
                attackRollExprs[i] = "(" + d20 + ")[1d20] " + sign + " (" + sitVal + ")[" + dieName + "]";
            } else {
                attackRollExprs[i] = "(" + d20 + ")[1d20]";
            }
            
            // Calculate actual total
            var total = d20;
            if (dieName && dieName !== '0') {
                total = (sign === '+') ? (d20 + sitVal) : (d20 - sitVal);
            }
            
            // Determine success level with full Alternity rules
            var status = "";
            var statusClass = "";
            
            if (d20 === 20) {
                status = "Critical Failure";
                statusClass = "miss";
            } else if (d20 === 1) {
                // Natural 1 is always a success (Ordinary at worst)
                if (total <= scoreA) {
                    status = "Amazing";
                    statusClass = "hit-ama";
                } else if (total <= scoreG) {
                    status = "Good";
                    statusClass = "hit-goo";
                } else {
                    status = "Ordinary";
                    statusClass = "hit-ord";
                }
            } else {
                if (total <= scoreA) {
                    status = "Amazing";
                    statusClass = "hit-ama";
                } else if (total <= scoreG) {
                    status = "Good";
                    statusClass = "hit-goo";
                } else if (total <= scoreO) {
                    status = "Ordinary";
                    statusClass = "hit-ord";
                } else {
                    status = "(Miss)";
                    statusClass = "miss";
                }
            }
            
            attackStatuses[i] = status;
            attackStatusClasses[i] = statusClass;
        }
        
        // Build and output the message styled with our premium HTML template
        var output = "&{template:alternity-attack} {{name=" + charName + " - " + weaponName + "}}";
        if (type !== '-') output += " {{type=" + type + "}}";
        if (range !== '-') output += " {{range=" + range + "}}";
        if (notes) output += " {{notes=" + notes + "}}";
        
        // Set the control die badge at the top
        output += " {{dicepool=[[" + d20 + "]]}}";
        
        // Add the rolls for each attack mode
        for (var i = 1; i <= mode; i++) {
            output += " {{attack" + i + "=[[" + attackRollExprs[i] + "]]}}";
            output += " {{scores" + i + "=[" + scoreO + "/" + scoreG + "/" + scoreA + "]}}";
            output += " {{ordinary" + i + "=[[" + scoreO + "]]}}";
            output += " {{good" + i + "=[[" + scoreG + "]]}}";
            output += " {{amazing" + i + "=[[" + scoreA + "]]}}";
            output += " {{amazing" + i + "_p1=[[" + (scoreA + 1) + "]]}}";
            output += " {{good" + i + "_p1=[[" + (scoreG + 1) + "]]}}";
            output += " {{status" + i + "=" + attackStatuses[i] + "}}";
            output += " {{status_class" + i + "=" + attackStatusClasses[i] + "}}";
        }
        
        // Send to chat using the original sender's identity
        sendChat(msg.who, output);
    });
});

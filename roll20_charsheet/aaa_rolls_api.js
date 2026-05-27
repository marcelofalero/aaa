/**
 * aaa RPG - Custom Roll20 API Dice Rolling Script
 * Handles multi-action attacks by rolling a single control d20 die exactly once,
 * applying different situation step dice for each attack, and outputting to the
 * character sheet's premium HTML roll template.
 */

on("chat:message", function(msg) {
    // Only intercept API commands starting with !aaa-roll
    if (msg.type !== "api") return;
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
        
        // Whispering debug info to GM
        sendChat("aaa API Debug", "/w gm [DEBUG] rollExpr: " + rollExpr + " | inlinerolls: " + JSON.stringify(msgObj.inlinerolls) + " | parts: " + JSON.stringify(parts));
        
        var usedIndices = {};
        var d20 = 10;
        
        // 1. Explicitly identify the control d20 roll (expression containing "1d20" or "d20")
        for (var k = 0; k < msgObj.inlinerolls.length; k++) {
            var roll = msgObj.inlinerolls[k];
            if (roll && roll.expression) {
                var normExpr = roll.expression.toLowerCase().replace(/\s+/g, '');
                if (normExpr.indexOf("1d20") !== -1 || normExpr.indexOf("d20") !== -1) {
                    d20 = roll.results.total;
                    usedIndices[k] = true;
                    break;
                }
            }
        }
        // Fallback: if d20 wasn't matched (or expression is empty), use the first roll in the array
        if (!usedIndices[0] && msgObj.inlinerolls[0]) {
            d20 = msgObj.inlinerolls[0].results.total;
            usedIndices[0] = true;
        }
        
        // 2. Assign the remaining situation dice sequentially to the unused inline rolls
        var attackRollExprs = {};
        for (var i = 1; i <= mode; i++) {
            var argIndex = 7 + (i * 2);
            var rollStr = parts[argIndex];
            var sign = parts[argIndex + 1] ? parts[argIndex + 1].trim() : '+';
            
            var sitVal = 0;
            var dieName = '';
            if (rollStr && rollStr.trim() !== '0') {
                dieName = rollStr.replace(/cs<0cf<0/g, '').trim();
                
                // Retrieve the next unused inline roll from the evaluated array
                for (var k = 0; k < msgObj.inlinerolls.length; k++) {
                    if (!usedIndices[k]) {
                        sitVal = msgObj.inlinerolls[k].results.total;
                        usedIndices[k] = true;
                        break;
                    }
                }
            }
            
            if (dieName && dieName !== '0') {
                attackRollExprs[i] = "(" + d20 + ")[1d20] " + sign + " (" + sitVal + ")[" + dieName + "]";
            } else {
                attackRollExprs[i] = "(" + d20 + ")[1d20]";
            }
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
        }
        
        // Send to chat using the original sender's identity
        sendChat(msg.who, output);
    });
});

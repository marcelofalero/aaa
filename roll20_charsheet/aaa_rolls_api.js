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
    // First roll is always the control d20 (index 0)
    var rollExpr = "[[1d20cs<1cf>20]]";
    var rollMap = []; // Map from attack index to its situation die's inline roll index
    var currentRollIndex = 1;
    
    for (var i = 1; i <= mode; i++) {
        var argIndex = 7 + (i * 2); // 9 for i = 1, 11 for i = 2, 13 for i = 3
        var rollStr = parts[argIndex];
        if (rollStr && rollStr.trim() !== '0') {
            rollExpr += " [[" + rollStr.trim() + "]]";
            rollMap[i] = currentRollIndex;
            currentRollIndex++;
        } else {
            rollMap[i] = -1; // No situation roll needed for this attack
        }
    }
    
    // Perform the rolls using Roll20's chat engine
    sendChat("", rollExpr, function(ops) {
        var msgObj = ops[0];
        if (!msgObj || !msgObj.inlinerolls || msgObj.inlinerolls.length === 0) {
            sendChat("aaa API", "/w gm [ERROR] Failed to evaluate dice rolls.");
            return;
        }
        
        // Extract the control d20 roll result (first inline roll)
        var d20 = msgObj.inlinerolls[0].results.total;
        
        // Calculate the results of all attacks as formulaic inline rolls
        var attackRollExprs = {};
        for (var i = 1; i <= mode; i++) {
            var argIndex = 7 + (i * 2);
            var rollStr = parts[argIndex];
            var sign = parts[argIndex + 1] ? parts[argIndex + 1].trim() : '+';
            
            var sitVal = 0;
            var dieName = '';
            if (rollStr && rollStr.trim() !== '0') {
                dieName = rollStr.replace(/cs<0cf<0/g, '').trim();
                var rollIdx = rollMap[i];
                if (rollIdx !== -1 && msgObj.inlinerolls[rollIdx]) {
                    sitVal = msgObj.inlinerolls[rollIdx].results.total;
                }
            }
            
            if (dieName && dieName !== '0') {
                attackRollExprs[i] = d20 + "[d20] " + sign + " " + sitVal + "[" + dieName + "]";
            } else {
                attackRollExprs[i] = d20 + "[d20]";
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
            output += " {{scores" + i + "}=[" + scoreO + "/" + scoreG + "/" + scoreA + "]}}";
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

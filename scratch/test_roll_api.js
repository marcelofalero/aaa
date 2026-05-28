function simulateRollAPI(msgContent) {
    console.log("Input command: " + msgContent);
    // Parse arguments separated by " || "
    var argsStr = msgContent.substring("!aaa-roll ".length);
    var parts = argsStr.split(" || ");
    
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
    
    console.log("Generated rollExpr: " + rollExpr);
    console.log("Generated rollMap: " + JSON.stringify(rollMap));
    
    // Simulate inline rolls results from Roll20
    // Let's say d20 rolls 12.
    // And for each situation roll, let's say they roll 3, 5, etc.
    var mockInlineRolls = [
        { results: { total: 12 }, expression: "1d20cs<1cf>20" }
    ];
    for (var i = 1; i < currentRollIndex; i++) {
        // Mock a roll value
        mockInlineRolls.push({ results: { total: i * 2 + 1 }, expression: "mockSituation" });
    }
    
    console.log("Mock inlinerolls: " + JSON.stringify(mockInlineRolls));
    
    var msgObj = { inlinerolls: mockInlineRolls };
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
            attackRollExprs[i] = "(" + d20 + ")[1d20] " + sign + " (" + sitVal + ")[" + dieName + "]";
        } else {
            attackRollExprs[i] = "(" + d20 + ")[1d20]";
        }
        
        console.log("Attack " + i + " result expr: " + attackRollExprs[i]);
    }
}

console.log("=== Test Mode 1 with 1d4 ===");
simulateRollAPI("!aaa-roll Character || Weapon || - || - ||  || 10 || 5 || 2 || 1 || 1d4cs<0cf<0 || +");

console.log("\n=== Test Mode 2 with 0 and 1d6 ===");
simulateRollAPI("!aaa-roll Character || Weapon || - || - ||  || 10 || 5 || 2 || 2 || 0 || + || 1d6cs<0cf<0 || +");

console.log("\n=== Test Mode 2 with 1d4 and 1d6 ===");
simulateRollAPI("!aaa-roll Character || Weapon || - || - ||  || 10 || 5 || 2 || 2 || 1d4cs<0cf<0 || + || 1d6cs<0cf<0 || +");

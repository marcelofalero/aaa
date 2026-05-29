function simulateRobustRollAPI(msgContent, mockInlineRolls) {
    console.log("\nInput command: " + msgContent);
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
    
    console.log("Mock inlinerolls: " + JSON.stringify(mockInlineRolls));
    
    var msgObj = { inlinerolls: mockInlineRolls };
    
    function normalizeExpr(expr) {
        if (!expr) return "";
        return expr.toLowerCase().replace(/\s+/g, "").trim();
    }
    
    var usedIndices = {};
    var d20 = 10;
    
    // Find d20 roll
    for (var k = 0; k < msgObj.inlinerolls.length; k++) {
        var roll = msgObj.inlinerolls[k];
        if (roll.expression && normalizeExpr(roll.expression).indexOf("1d20") === 0) {
            d20 = roll.results.total;
            usedIndices[k] = true;
            break;
        }
    }
    
    function findRollValue(expression) {
        var normTarget = normalizeExpr(expression);
        for (var k = 0; k < msgObj.inlinerolls.length; k++) {
            if (usedIndices[k]) continue;
            var roll = msgObj.inlinerolls[k];
            if (roll.expression && normalizeExpr(roll.expression) === normTarget) {
                usedIndices[k] = true;
                return roll.results.total;
            }
        }
        // Fallback: return first unused roll
        for (var k = 0; k < msgObj.inlinerolls.length; k++) {
            if (!usedIndices[k]) {
                usedIndices[k] = true;
                return msgObj.inlinerolls[k].results.total;
            }
        }
        return 0;
    }
    
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
            sitVal = findRollValue(rollStr.trim());
        }
        
        if (dieName && dieName !== '0') {
            attackRollExprs[i] = "(" + d20 + ")[1d20] " + sign + " (" + sitVal + ")[" + dieName + "]";
        } else {
            attackRollExprs[i] = "(" + d20 + ")[1d20]";
        }
        
        console.log("Attack " + i + " result expr: " + attackRollExprs[i]);
    }
}

// Case 1: In order
console.log("--- TEST 1: IN ORDER ---");
simulateRobustRollAPI(
    "!aaa-roll Character || Weapon || - || - ||  || 10 || 5 || 2 || 1 || 1d4cs<0cf<0 || +",
    [
        { results: { total: 12 }, expression: "1d20cs<1cf>20" },
        { results: { total: 3 }, expression: "1d4cs<0cf<0" }
    ]
);

// Case 2: Swapped (out of order)
console.log("\n--- TEST 2: SWAPPED/OUT OF ORDER ---");
simulateRobustRollAPI(
    "!aaa-roll Character || Weapon || - || - ||  || 10 || 5 || 2 || 1 || 1d4cs<0cf<0 || +",
    [
        { results: { total: 3 }, expression: "1d4cs<0cf<0" },
        { results: { total: 12 }, expression: "1d20cs<1cf>20" }
    ]
);

// Case 3: Mode 2 with one roll
console.log("\n--- TEST 3: MODE 2, ONE ROLL ---");
simulateRobustRollAPI(
    "!aaa-roll Character || Weapon || - || - ||  || 10 || 5 || 2 || 2 || 0 || + || 1d6cs<0cf<0 || +",
    [
        { results: { total: 4 }, expression: "1d6cs<0cf<0" },
        { results: { total: 15 }, expression: "1d20cs<1cf>20" }
    ]
);

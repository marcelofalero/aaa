#!/usr/bin/env node
/**
 * Character JSON Rulebook Validator (Headless JS Engine Wrapper)
 *
 * Uses `CharacterEngine.js` as the single source of truth for character
 * validation and budget calculations.
 */

const fs = require('fs');
const path = require('path');
const CharacterEngine = require('../../site/static/js/character-engine.js');

const ROOT_DIR = path.resolve(__dirname, '../../');

function validateFile(filePath) {
  if (!fs.existsSync(filePath)) {
    return {
      isValid: false,
      errors: [`File not found: ${filePath}`],
      warnings: [],
      info: []
    };
  }

  try {
    const rawData = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    const engine = new CharacterEngine();
    engine.fromJSON(rawData);
    return engine.validate();
  } catch (e) {
    return {
      isValid: false,
      errors: [`JSON Parse Error: ${e.message}`],
      warnings: [],
      info: []
    };
  }
}

function main() {
  const args = process.argv.slice(2);
  const verbose = args.includes('-v') || args.includes('--verbose');
  const cleanArgs = args.filter(a => a !== '-v' && a !== '--verbose');

  let targetPath = path.join(ROOT_DIR, 'premade_characters');
  if (cleanArgs.length > 0) {
    targetPath = path.resolve(process.cwd(), cleanArgs[0]);
  }

  let files = [];
  if (fs.existsSync(targetPath)) {
    const stat = fs.statSync(targetPath);
    if (stat.isDirectory()) {
      files = fs.readdirSync(targetPath)
        .filter(f => f.endsWith('.json'))
        .map(f => path.join(targetPath, f));
    } else if (stat.isFile()) {
      files = [targetPath];
    }
  } else {
    console.error(`Path does not exist: ${targetPath}`);
    process.exit(1);
  }

  files.sort();

  console.log("==========================================================================");
  console.log("           CHARACTER BUILDER JSON RULEBOOK VALIDATOR REPORT               ");
  console.log("==========================================================================");

  let passedCount = 0;
  let failedCount = 0;

  files.forEach(file => {
    const relPath = path.relative(ROOT_DIR, file) || file;
    const report = validateFile(file);

    const status = report.isValid ? "✅ PASS" : "❌ FAIL";
    console.log(`\n[${status}] ${relPath}`);

    (report.info || []).forEach(item => {
      console.log(`  ℹ️  ${item}`);
    });
    (report.warnings || []).forEach(w => {
      console.log(`  ⚠️  WARNING: ${w}`);
    });
    (report.errors || []).forEach(e => {
      console.log(`  🚨 ERROR: ${e}`);
    });

    if (report.isValid) passedCount++;
    else failedCount++;
  });

  console.log("\n--------------------------------------------------------------------------");
  console.log(`SUMMARY: Total Checked: ${files.length} | Passed: ${passedCount} | Failed: ${failedCount}`);
  console.log("==========================================================================");

  if (failedCount > 0) {
    process.exit(1);
  }
}

main();

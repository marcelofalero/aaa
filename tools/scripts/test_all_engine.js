#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const CharacterEngine = require('../../site/static/js/character-engine.js');

const premadesDir = path.join(__dirname, '../../premade_characters');
const files = fs.readdirSync(premadesDir).filter(f => f.endsWith('.json'));

console.log(`Checking ${files.length} character files using headless CharacterEngine:\n`);

let passCount = 0;
const engine = new CharacterEngine();

files.forEach(file => {
  const filepath = path.join(premadesDir, file);
  const rawData = JSON.parse(fs.readFileSync(filepath, 'utf8'));
  engine.fromJSON(rawData);
  const report = engine.validate();

  if (report.isValid) {
    passCount++;
    console.log(`[✅ PASS] ${file} (${report.creationSPSpent} BP, ${report.campaignAPSpent} AP)`);
  } else {
    console.log(`[❌ FAIL] ${file}: ${report.errors.join(' | ')}`);
  }
});

console.log(`\nSummary: ${passCount} / ${files.length} passed.`);

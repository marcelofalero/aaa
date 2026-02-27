const fs = require('fs');
const html = fs.readFileSync('public/equipment/weapons/index.html', 'utf8');
if (html.includes('TableOfContents')) {
  console.log('FOUND TOC');
} else {
  console.log('NO TOC');
}

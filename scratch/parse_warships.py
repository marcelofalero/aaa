import os
import re

def clean_paragraph(p_lines):
    # Join lines with space and clean up double spaces
    text = " ".join(p_lines)
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Replace terminology as mandated: hero -> character, heroes -> characters
    # Respect word boundaries and capitalization
    text = re.sub(r'\bheroes\b', 'characters', text)
    text = re.sub(r'\bHeroes\b', 'Characters', text)
    text = re.sub(r'\bhero\b', 'character', text)
    text = re.sub(r'\bHero\b', 'Character', text)
    text = re.sub(r'\bhero\'s\b', 'character\'s', text)
    text = re.sub(r'\bHero\'s\b', 'Character\'s', text)
    text = re.sub(r'\bheroes\'\b', 'characters\'', text)
    text = re.sub(r'\bHeroes\'\b', 'Characters\'', text)
    
    return text

def parse_section(lines, title, desc, weight):
    parsed_blocks = []
    current_p = []
    
    in_table = False
    table_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip empty lines but treat them as paragraph boundaries
        if not line:
            if current_p:
                parsed_blocks.append(clean_paragraph(current_p))
                current_p = []
            i += 1
            continue
            
        # Remove page break symbols and page numbers
        line = line.replace('\x0c', '')
        if re.match(r'^\d+$', line):
            i += 1
            continue
            
        # Skip page headers / footers
        if line == "WARSHIPS" or line.startswith("BY R ICHARD BAKER") or line.startswith("DEFINITIONS") or line.startswith("INTRODUCTION"):
            i += 1
            continue
            
        # Detect headings
        # Headers are usually in all caps
        if line.isupper() and len(line) > 3 and not line.startswith("TABLE") and not line.startswith("DIAGRAM") and not re.match(r'^[A-Z\s\-\–\d\.\,\:\;\!\?\(\)]+$', line) is None:
            # First clean any paragraph we are currently building
            if current_p:
                parsed_blocks.append(clean_paragraph(current_p))
                current_p = []
            
            # Format heading nicely (Title Case)
            heading_title = line.title()
            # Replace roman numerals or step numbers properly
            heading_title = re.sub(r'\bPl\b', 'PL', heading_title)
            heading_title = re.sub(r'\bFtl\b', 'FTL', heading_title)
            heading_title = re.sub(r'\b3D\b', '3D', heading_title)
            heading_title = re.sub(r'\bMc\b', 'MC', heading_title)
            
            # Check if it looks like a major chapter header or a subheader
            if heading_title.startswith("Chapter"):
                parsed_blocks.append(f"# {heading_title}")
            else:
                parsed_blocks.append(f"## {heading_title}")
                
            i += 1
            continue
            
        # Detect list items
        if line.startswith('•') or line.startswith('⊗') or line.startswith('▶') or (line.startswith('-') and len(line) > 1):
            if current_p:
                parsed_blocks.append(clean_paragraph(current_p))
                current_p = []
            
            # Clean list item text
            item_text = clean_paragraph([line])
            parsed_blocks.append(item_text)
            i += 1
            continue
            
        # Regular text line
        current_p.append(line)
        i += 1
        
    if current_p:
        parsed_blocks.append(clean_paragraph(current_p))
        
    # Build the final markdown content
    markdown_lines = []
    markdown_lines.append("+++")
    markdown_lines.append(f'title = "{title}"')
    markdown_lines.append(f'description = "{desc}"')
    markdown_lines.append(f"weight = {weight}")
    markdown_lines.append("+++")
    markdown_lines.append("")
    
    for block in parsed_blocks:
        markdown_lines.append(block)
        markdown_lines.append("")
        
    return "\n".join(markdown_lines)

def main():
    with open('/home/dimble/projects/aaa/scratch/warships.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    # Line ranges (0-indexed, so subtract 1 from 1-based line numbers)
    sections = [
        {"file": "site/content/warships/_index.md", "title": "Warships", "desc": "Capital ship combat and construction rules.", "weight": 10, "start": 182, "end": 504},
        {"file": "site/content/warships/basic-combat.md", "title": "Basic Combat", "desc": "Cinematic starship combat rules for capital ships.", "weight": 20, "start": 504, "end": 1438},
        {"file": "site/content/warships/advanced-combat.md", "title": "Advanced Combat", "desc": "Detailed subsystem and vector movement rules.", "weight": 30, "start": 1438, "end": 2868},
        {"file": "site/content/warships/narrative-combat.md", "title": "Narrative Combat", "desc": "Rules for characters serving aboard capital ships during combat.", "weight": 40, "start": 2868, "end": 3718},
        {"file": "site/content/warships/flight-dynamics.md", "title": "Flight Dynamics", "desc": "Scientific principles of space flight and relativistic speeds.", "weight": 50, "start": 3718, "end": 4379},
        {"file": "site/content/warships/ship-construction.md", "title": "Ship Construction", "desc": "A step-by-step system for designing custom starships.", "weight": 60, "start": 4379, "end": 12680},
        {"file": "site/content/warships/stations-and-bases.md", "title": "Stations and Bases", "desc": "Rules for constructing and operating orbital space stations.", "weight": 70, "start": 12680, "end": len(lines)}
    ]
    
    os.makedirs('site/content/warships', exist_ok=True)
    
    for sec in sections:
        sec_lines = lines[sec["start"]:sec["end"]]
        md_content = parse_section(sec_lines, sec["title"], sec["desc"], sec["weight"])
        
        with open(sec["file"], 'w', encoding='utf-8') as f_out:
            f_out.write(md_content)
        print(f"Created {sec['file']}")

if __name__ == '__main__':
    main()

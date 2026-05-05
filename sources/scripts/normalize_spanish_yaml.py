import yaml
import re
from ruamel.yaml import YAML

# Using ruamel.yaml to preserve formatting as much as possible
ryaml = YAML()
ryaml.preserve_quotes = True
ryaml.width = 1000
ryaml.indent(mapping=2, sequence=4, offset=2)

SKILLS_YAML = 'sources/data_sources/skills.yaml'

def normalize_spanish_text(text):
    if not text:
        return text
    
    # 1. Terminology replacements (Case insensitive for some)
    replacements = [
        (r'\bhero\b', 'personaje'),
        (r'\bHero\b', 'Personaje'),
        (r'\bheroes\b', 'personajes'),
        (r'\bHeroes\b', 'Personajes'),
        (r'\bRank\b', 'Rango'),
        (r'\brank\b', 'rango'),
        (r'\bStep\b', 'Paso'),
        (r'\bstep\b', 'paso'),
        (r'\bpenalty\b', 'penalización'),
        (r'\bPenalty\b', 'Penalización'),
        (r'\bbonus\b', 'bonificador'),
        (r'\bBonus\b', 'Bonificador'),
        (r'\bGamemaster\b', 'Director de Juego'),
        (r'\bGM\b', 'DJ'),
    ]
    
    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text)

    # 2. Header normalization
    text = re.sub(r'### Rank Progression', '### Beneficios de Rango', text)
    text = re.sub(r'### Rango Progression', '### Beneficios de Rango', text)
    text = re.sub(r'\*\*Rank Progression\*\*', '### Beneficios de Rango', text)
    text = re.sub(r'\*\*Rango Progression\*\*', '### Beneficios de Rango', text)
    text = re.sub(r'### Results', '### Resultados', text)
    
    # 3. Icon normalization
    # Replace (Rank X) or [Rank X] with [Rango X]
    text = re.sub(r'\[Rango (\d+)\]', r'Rango \1', text) # Remove brackets temporarily for standardization
    text = re.sub(r'\(Rango (\d+)\)', r'Rango \1', text)
    
    # Re-apply standardized format: ▶ **Rango X [Title]:**
    # This is tricky because the title might be English or Spanish.
    # Pattern: ▶ **Rango X (Title):** or ▶ **Rango X [Title]:**
    text = re.sub(r'▶ \*\*Rango (\d+) [\(\[]?([^\]\)]+)[\)\]]?:\*\*', r'▶ **Rango \1 [\2]:**', text)
    text = re.sub(r'⊗ \*\*Rango (\d+) [\(\[]?([^\]\)]+)[\)\]]?:\*\*', r'⊗ **Rango \1 [\2]:**', text)
    
    # 4. Clean up separators and extra lines
    text = re.sub(r'^---+\s*$', '', text, flags=re.MULTILINE)
    
    # 5. Fix double spaces or formatting glitches from previous runs
    text = text.replace('  ', ' ')
    
    return text.strip()

def process_node(node):
    if isinstance(node, dict):
        if 'localized' in node:
            for loc in node['localized']:
                if 'es' in loc:
                    loc['es']['description'] = normalize_spanish_text(loc['es'].get('description', ''))
        
        for key, value in node.items():
            process_node(value)
    elif isinstance(node, list):
        for item in node:
            process_node(item)

def main():
    print(f"Loading {SKILLS_YAML}...")
    with open(SKILLS_YAML, 'r', encoding='utf-8') as f:
        data = ryaml.load(f)
    
    print("Normalizing Spanish translations...")
    process_node(data)
    
    print(f"Saving to {SKILLS_YAML}...")
    with open(SKILLS_YAML, 'w', encoding='utf-8') as f:
        ryaml.dump(data, f)
    
    print("Done!")

if __name__ == "__main__":
    main()

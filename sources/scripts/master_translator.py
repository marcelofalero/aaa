import os
import re
import yaml
import time
from ruamel.yaml import YAML
from deep_translator import GoogleTranslator

# Config
SKILLS_YAML = 'sources/data_sources/skills.yaml'
MAPPING_MD = 'site/content/notes/terminology-mapping.md'
OUTPUT_YAML = 'sources/data_sources/skills.yaml'

ryaml = YAML()
ryaml.preserve_quotes = True
ryaml.width = 1000
ryaml.indent(mapping=2, sequence=4, offset=2)

def load_mapping():
    mapping = {}
    if not os.path.exists(MAPPING_MD):
        print(f"Warning: {MAPPING_MD} not found.")
        return mapping
    
    with open(MAPPING_MD, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple regex to extract table rows: | English | Spanish |
    matches = re.findall(r'\|\s*(.*?)\s*\|\s*(.*?)\s*\|', content)
    for en, es in matches:
        en_clean = en.strip().strip('*').strip('_')
        es_clean = es.strip().strip('*').strip('_')
        if en_clean and es_clean and en_clean != 'English' and en_clean != ':---' and en_clean != '...':
            mapping[en_clean] = es_clean
    return mapping

def apply_mapping(text, mapping):
    if not text: return ''
    # Sort by length descending to avoid partial matches (e.g., 'Skill' vs 'Skill Points')
    sorted_terms = sorted(mapping.keys(), key=len, reverse=True)
    for en in sorted_terms:
        es = mapping[en]
        # Use word boundaries for safety, case insensitive
        pattern = re.compile(r'\b' + re.escape(en) + r'\b', re.IGNORECASE)
        # We try to preserve case if possible, but for simplicity we use the mapped value
        text = pattern.sub(es, text)
    return text

def translate_text(text, translator):
    if not text or len(text.strip()) == 0:
        return text
    
    # Split by paragraphs to handle length limits and preserve structure
    paragraphs = text.split('\n\n')
    translated_paragraphs = []
    
    for p in paragraphs:
        if not p.strip():
            translated_paragraphs.append('')
            continue
            
        # Skip translation for headers/markdown structure if they are just symbols
        if p.strip().startswith('###') or p.strip().startswith('▶') or p.strip().startswith('⊗'):
            # But we might want to translate the title inside [brackets]
            # For now, let's just translate the whole thing and then we'll fix headers
            pass
            
        try:
            # GoogleTranslator handles up to 5000 chars, but smaller chunks are safer
            if len(p) > 4500:
                # Very rare in this dataset, but just in case
                p = p[:4500]
            
            translated = translator.translate(p)
            if translated is None:
                print(f"Warning: Translation returned None for paragraph. Falling back to original.")
                translated_paragraphs.append(p)
            else:
                translated_paragraphs.append(str(translated))
            # Small delay to be polite to the API
            time.sleep(0.1)
        except Exception as e:
            print(f"Error translating paragraph: {e}")
            translated_paragraphs.append(p) # Fallback to original
            
    return '\n\n'.join(translated_paragraphs)

def normalize_formatting(text):
    # Fix common machine translation artifacts in Markdown
    text = re.sub(r'###\s+', '### ', text)
    text = re.sub(r'#\s+', '# ', text)
    # Fix icons if the translator messed them up
    text = text.replace('▶', '▶').replace('⊗', '⊗')
    # Standardize Rank Benefits format
    text = re.sub(r'(▶|⊗)\s+\*\*Rango\s+(\d+)\s+\[(.*?)\]:\*\*', r'\1 **Rango \2 [\3]:**', text)
    return text

def process_node(node, translator, mapping, processed_count):
    if isinstance(node, dict):
        if 'localized' in node:
            en_desc = ""
            en_name = ""
            es_loc = None
            
            for loc in node['localized']:
                if 'en' in loc:
                    en_desc = loc['en'].get('description', '')
                    en_name = loc['en'].get('name', '')
                if 'es' in loc:
                    es_loc = loc['es']
            
            if en_desc and es_loc:
                # Check if it's already translated (simplistic check: contains mostly Spanish)
                # But user wants "deterministic" pass, so we'll re-translate
                print(f"Translating: {en_name}...")
                
                # 1. Translate
                translated = translate_text(en_desc, translator)
                
                # 2. Apply Terminology Mapping
                final_text = apply_mapping(translated, mapping)
                
                # 3. Normalize Formatting
                final_text = normalize_formatting(final_text)
                
                es_loc['description'] = final_text
                
                # Also translate name if needed
                if en_name and ('name' not in es_loc or not es_loc['name']):
                    es_loc['name'] = translator.translate(en_name)
                
                processed_count[0] += 1
        
        for key, value in node.items():
            if key != 'localized': # Avoid double processing
                process_node(value, translator, mapping, processed_count)
                
    elif isinstance(node, list):
        for item in node:
            process_node(item, translator, mapping, processed_count)

def main():
    print("Loading mapping...")
    mapping = load_mapping()
    print(f"Loaded {len(mapping)} terminology rules.")
    
    print(f"Loading {SKILLS_YAML}...")
    with open(SKILLS_YAML, 'r', encoding='utf-8') as f:
        data = ryaml.load(f)
    
    translator = GoogleTranslator(source='en', target='es')
    processed_count = [0]
    
    print("Starting translation process (this may take a few minutes)...")
    process_node(data, translator, mapping, processed_count)
    
    print(f"Processed {processed_count[0]} skills/specialties.")
    
    print(f"Saving to {OUTPUT_YAML}...")
    with open(OUTPUT_YAML, 'w', encoding='utf-8') as f:
        ryaml.dump(data, f)
    
    print("Done! All Spanish translations have been updated and mapped.")

if __name__ == "__main__":
    main()

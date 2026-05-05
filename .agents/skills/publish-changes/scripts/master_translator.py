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
    # Sort by length descending to avoid partial matches
    sorted_terms = sorted(mapping.keys(), key=len, reverse=True)
    for en in sorted_terms:
        es = mapping[en]
        pattern = re.compile(r'\b' + re.escape(en) + r'\b', re.IGNORECASE)
        text = pattern.sub(es, text)
    return text

def translate_text(text, translator):
    if not text or len(text.strip()) == 0:
        return text
    
    paragraphs = text.split('\n\n')
    translated_paragraphs = []
    
    for p in paragraphs:
        if not p.strip():
            translated_paragraphs.append('')
            continue
            
        try:
            if len(p) > 4500:
                p = p[:4500]
            
            translated = translator.translate(p)
            if translated is None:
                translated_paragraphs.append(p)
            else:
                translated_paragraphs.append(str(translated))
            time.sleep(0.1)
        except Exception as e:
            print(f"Error translating paragraph: {e}")
            translated_paragraphs.append(p)
            
    return '\n\n'.join(translated_paragraphs)

def normalize_formatting(text):
    text = re.sub(r'###\s+', '### ', text)
    text = re.sub(r'#\s+', '# ', text)
    # Standardize icons and rank headers
    text = text.replace('▶', '▶').replace('⊗', '⊗')
    # Use the new format from origin/main: Rank X (Title)
    text = re.sub(r'(▶|⊗)\s+\*\*Rango\s+(\d+)\s+\[(.*?)\]:\*\*', r'\1 **Rango \2 (\3):**', text)
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
                print(f"Translating: {en_name}...")
                translated = translate_text(en_desc, translator)
                final_text = apply_mapping(translated, mapping)
                final_text = normalize_formatting(final_text)
                es_loc['description'] = final_text
                if en_name and ('name' not in es_loc or not es_loc['name']):
                    es_loc['name'] = translator.translate(en_name)
                processed_count[0] += 1
        
        for key, value in node.items():
            if key != 'localized':
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
    
    print("Starting translation process...")
    process_node(data, translator, mapping, processed_count)
    
    print(f"Processed {processed_count[0]} entries.")
    
    print(f"Saving to {OUTPUT_YAML}...")
    with open(OUTPUT_YAML, 'w', encoding='utf-8') as f:
        ryaml.dump(data, f)
    
    print("Done!")

if __name__ == "__main__":
    main()

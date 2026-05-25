import os
import re
import yaml
import time
import sys
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString
from deep_translator import GoogleTranslator
from pathlib import Path

def find_project_root():
    current = Path.cwd().resolve()
    for parent in [current] + list(current.parents):
        if (parent / '.project_root').exists():
            return parent
    return Path.cwd().resolve()

os.chdir(find_project_root())

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

def protect_blocks(text):
    if not text or not isinstance(text, str): return text, []
    
    placeholders = []
    def store_block(match):
        placeholders.append(match.group(0))
        return f"@BLOCK_PLACEHOLDER_{len(placeholders)-1}@"
    
    # Protect Markdown URLs and Hugo shortcodes
    block_pattern = r'(\]\s*\([\s\S]*?\)|{{<[\s\S]*?>}})'
    text_with_placeholders = re.sub(block_pattern, store_block, text, flags=re.DOTALL)
    return text_with_placeholders, placeholders

def restore_blocks(text, placeholders):
    if not text or not isinstance(text, str): return text
    for i, block in enumerate(placeholders):
        text = text.replace(f"@BLOCK_PLACEHOLDER_{i}@", block)
    return text

def protect_terms(text, mapping):
    if not text or not isinstance(text, str): return text, {}
    
    placeholders = {}
    # Sort terms by length descending to avoid partial matches
    sorted_en_terms = sorted(mapping.keys(), key=len, reverse=True)
    counter = 0
    
    for en in sorted_en_terms:
        is_short = len(en) <= 3
        flags = 0 if is_short else re.IGNORECASE
        
        # Word boundary check
        pattern = f"\\b{re.escape(en)}\\b"
        
        if re.search(pattern, text, flags=flags):
            placeholder = f"ZTERM{counter}Z"
            placeholders[placeholder] = mapping[en]
            text = re.sub(pattern, placeholder, text, flags=flags)
            counter += 1
            
    return text, placeholders

def restore_terms(text, placeholders):
    if not text or not isinstance(text, str): return text
    for placeholder, es_term in placeholders.items():
        text = text.replace(placeholder, es_term)
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
            
            # If Spanish block is missing but English exists, create it
            if not es_loc and (en_desc or en_name):
                es_loc = {}
                node['localized'].append({'es': es_loc})
            
            if en_desc and es_loc:
                # Always translate if es description is significantly shorter than English
                # or if the user forces it
                current_es_desc = es_loc.get('description', '')
                if not current_es_desc or len(current_es_desc) < len(en_desc) * 0.8 or '--force' in sys.argv:
                    print(f"Translating description: {en_name or 'unnamed'}...")
                    
                    # 1. Protect Markdown links and Hugo shortcodes
                    text_no_blocks, blocks = protect_blocks(en_desc)
                    
                    # 2. Protect specific terms from mapping
                    protected_text, term_placeholders = protect_terms(text_no_blocks, mapping)
                    
                    # 3. Translate the remaining text
                    translated = translate_text(protected_text, translator)
                    
                    # 4. Restore terms and blocks
                    restored_terms = restore_terms(translated, term_placeholders)
                    final_text = restore_blocks(restored_terms, blocks)
                    
                    final_text = normalize_formatting(final_text)
                    es_loc['description'] = LiteralScalarString(final_text)
                
                if en_name and ('name' not in es_loc or not es_loc['name']):
                    print(f"Translating name: {en_name}...")
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
    
    yaml_files = [
        'sources/data_sources/skills.yaml',
        'sources/data_sources/psionics.yaml'
    ]
    
    translator = GoogleTranslator(source='en', target='es')
    
    for yaml_path in yaml_files:
        if not os.path.exists(yaml_path):
            print(f"Warning: {yaml_path} not found.")
            continue
            
        print(f"Loading {yaml_path}...")
        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = ryaml.load(f)
            
        processed_count = [0]
        print(f"Starting translation process for {yaml_path}...")
        process_node(data, translator, mapping, processed_count)
        print(f"Processed {processed_count[0]} entries.")
        
        print(f"Saving to {yaml_path}...")
        with open(yaml_path, 'w', encoding='utf-8') as f:
            ryaml.dump(data, f)
            
    print("Done!")

if __name__ == "__main__":
    main()

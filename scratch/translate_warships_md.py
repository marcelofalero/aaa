import os
import re
import time
import sys
from deep_translator import GoogleTranslator

MAPPING_MD = 'site/content/notes/terminology-mapping.md'

def load_mapping():
    mapping = {}
    if not os.path.exists(MAPPING_MD):
        print(f"Warning: {MAPPING_MD} not found.")
        return mapping
    
    with open(MAPPING_MD, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract table rows: | English | Spanish |
    matches = re.findall(r'\|\s*(.*?)\s*\|\s*(.*?)\s*\|', content)
    for en, es in matches:
        en_clean = en.strip().strip('*').strip('_')
        es_clean = es.strip().strip('*').strip('_')
        if en_clean and es_clean and en_clean != 'English' and en_clean != ':---' and en_clean != '...':
            # Skip simple things that might cause issues or overlap
            if len(en_clean) > 2:
                mapping[en_clean] = es_clean
    return mapping

def protect_blocks(text):
    if not text or not isinstance(text, str): return text, []
    
    placeholders = []
    def store_block(match):
        placeholders.append(match.group(0))
        return f"@BLOCK_PLACEHOLDER_{len(placeholders)-1}@"
    
    # Protect Markdown links and Hugo shortcodes
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
    sorted_en_terms = sorted(mapping.keys(), key=len, reverse=True)
    counter = 0
    
    for en in sorted_en_terms:
        # Avoid matching extremely short/common sub-words without boundaries
        pattern = f"\\b{re.escape(en)}\\b"
        
        if re.search(pattern, text, flags=re.IGNORECASE):
            placeholder = f"ZTERM{counter}Z"
            # Keep track of the exact translation
            placeholders[placeholder] = mapping[en]
            text = re.sub(pattern, placeholder, text, flags=re.IGNORECASE)
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
    
    try:
        # Safety limit for Google Translate single query
        if len(text) > 4500:
            text = text[:4500]
        
        translated = translator.translate(text)
        if translated is None:
            return text
        return str(translated)
    except Exception as e:
        print(f"Error translating paragraph: {e}")
        return text

def normalize_formatting(text):
    text = re.sub(r'###\s+', '### ', text)
    text = re.sub(r'##\s+', '## ', text)
    text = re.sub(r'#\s+', '# ', text)
    # Standardize icons and rank headers
    text = text.replace('▶', '▶').replace('⊗', '⊗')
    # Rank X (Title) -> Rango X (Title)
    text = re.sub(r'(▶|⊗)\s+\*\*Rank\s+(\d+)\s+\[(.*?)\]:\*\*', r'\1 **Rango \2 (\3):**', text)
    text = re.sub(r'(▶|⊗)\s+\*\*Rank\s+(\d+)\s+\[(.*?)\]\*\*', r'\1 **Rango \2 (\3):**', text)
    # Re-normalize standard step modifiers
    text = re.sub(r'\bstep penalty\b', 'penalización de paso', text, flags=re.IGNORECASE)
    text = re.sub(r'\bstep bonus\b', 'bonificación de paso', text, flags=re.IGNORECASE)
    return text

def main():
    print("Loading terminology mapping...")
    mapping = load_mapping()
    print(f"Loaded {len(mapping)} terminology rules.")
    
    translator = GoogleTranslator(source='en', target='es')
    
    target_dir = 'site/content/warships'
    files = [f for f in os.listdir(target_dir) if f.endswith('.md') and not f.endswith('.es.md')]
    
    for filename in sorted(files):
        en_path = os.path.join(target_dir, filename)
        es_path = os.path.join(target_dir, filename.replace('.md', '.es.md'))
        
        print(f"Translating {en_path} to {es_path}...")
        
        with open(en_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Parse front matter
        fm_match = re.match(r'^\+\+\+\s*\n([\s\S]*?)\n\+\+\+\s*\n([\s\S]*)$', content)
        if not fm_match:
            print(f"Skipping {en_path}: Invalid front matter.")
            continue
            
        fm_text = fm_match.group(1)
        body_text = fm_match.group(2)
        
        # Translate title and description in front matter
        translated_fm_lines = []
        for line in fm_text.split('\n'):
            if line.startswith('title = '):
                title_val = re.search(r'title = "(.*?)"', line).group(1)
                trans_title = translate_text(title_val, translator)
                translated_fm_lines.append(f'title = "{trans_title}"')
            elif line.startswith('description = '):
                desc_val = re.search(r'description = "(.*?)"', line).group(1)
                trans_desc = translate_text(desc_val, translator)
                translated_fm_lines.append(f'description = "{trans_desc}"')
            else:
                translated_fm_lines.append(line)
                
        translated_fm = "+++\n" + "\n".join(translated_fm_lines) + "\n+++\n"
        
        # Translate body with paragraph chunking
        paragraphs = body_text.split('\n\n')
        translated_paragraphs = []
        
        current_chunk = []
        current_len = 0
        
        def process_chunk(chunk_text):
            if not chunk_text.strip():
                return ""
            # 1. Protect Markdown links/shortcodes
            p_no_blocks, blocks = protect_blocks(chunk_text)
            
            # 2. Protect terminology mapping terms
            protected_p, term_placeholders = protect_terms(p_no_blocks, mapping)
            
            # 3. Translate the chunk
            translated_p = translate_text(protected_p, translator)
            
            # 4. Restore protected terms and blocks
            restored_p = restore_terms(translated_p, term_placeholders)
            final_p = restore_blocks(restored_p, blocks)
            
            return normalize_formatting(final_p)

        for p in paragraphs:
            p_strip = p.strip()
            if not p_strip:
                continue
                
            # If it's a heading, flush current chunk first, then translate heading
            if p_strip.startswith('#'):
                if current_chunk:
                    translated_paragraphs.append(process_chunk("\n\n".join(current_chunk)))
                    current_chunk = []
                    current_len = 0
                
                # Translate heading
                level = re.match(r'^(#+)\s*', p_strip).group(1)
                header_text = p_strip[len(level):].strip()
                trans_header = translate_text(header_text, translator)
                translated_paragraphs.append(f"{level} {trans_header}")
                continue
                
            # Otherwise, add to chunk
            p_len = len(p_strip)
            if current_len + p_len + 2 > 3500:
                # Flush current chunk
                translated_paragraphs.append(process_chunk("\n\n".join(current_chunk)))
                current_chunk = [p_strip]
                current_len = p_len
            else:
                current_chunk.append(p_strip)
                current_len += p_len + 2
                
        # Flush any remaining chunk
        if current_chunk:
            translated_paragraphs.append(process_chunk("\n\n".join(current_chunk)))
            
        translated_body = "\n\n".join(translated_paragraphs)
        
        with open(es_path, 'w', encoding='utf-8') as f_out:
            f_out.write(translated_fm + translated_body)
            
        print(f"Finished translating {filename}.")

if __name__ == '__main__':
    main()

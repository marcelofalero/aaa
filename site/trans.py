import os
import re
import json
import traceback
from deep_translator import GoogleTranslator
from concurrent.futures import ThreadPoolExecutor

translator = GoogleTranslator(source='en', target='es')

# Simple cache to avoid redundant translations
t_cache = {}
def trans(text):
    if not text or not isinstance(text, str) or text.isnumeric():
        return text
    if text in t_cache:
        return t_cache[text]
        
    try:
        res = translator.translate(text)
        t_cache[text] = res
        return res
    except Exception as e:
        print(f"Failed to translate '{text}': {e}")
        return text

def translate_json_obj(obj, parent_key=None):
    if isinstance(obj, dict):
        new_obj = {}
        for k, v in obj.items():
            new_obj[k] = translate_json_obj(v, parent_key=k)
        return new_obj
    elif isinstance(obj, list):
        return [translate_json_obj(v, parent_key) for v in obj]
    elif isinstance(obj, str):
        # DO NOT TRANSLATE VALUES FOR THESE SPECIFIC KEYS
        if parent_key in ["key", "description_only", "columns"]:
            return obj
            
        # some hardcoded strings skipping
        if len(obj) < 2 and not obj.isalpha():
            return obj
        # Skip fractions like 2/1/0 or D&D stats like d4+1s/d6w
        if re.match(r'^[\d/+A-Za-z-]+$', obj) and '/' in obj:
            return obj
        # Keep numeric codes
        if re.match(r'^[-+]?\d+$', obj):
            return obj
            
        return trans(obj)
    else:
        return obj

def process_file(file_path):
    try:
        if file_path.endswith('.es.md') or file_path.endswith('.es.json'):
            return

        if file_path.endswith('.md'):
            new_path = file_path[:-3] + '.es.md'
            if os.path.exists(new_path):
                return

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Translate title
            def replace_title(match):
                original_title = match.group(1)
                translated = trans(original_title)
                print(f"MD [{file_path}] Title: {original_title} -> {translated}")
                return f'title = "{translated}"'
            
            # YAML or TOML title
            content = re.sub(r'^title\s*[=:]\s*"(.*?)"', replace_title, content, flags=re.MULTILINE)
            
            # Translate description
            def replace_desc(match):
                translated = trans(match.group(1))
                return f'description = "{translated}"'
            content = re.sub(r'^description\s*[=:]\s*"(.*?)"', replace_desc, content, flags=re.MULTILINE)

            with open(new_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
        elif file_path.endswith('.json'):
            new_path = file_path[:-5] + '.es.json'
            if os.path.exists(new_path):
                return
                
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            print(f"JSON Translate {file_path} ...")
            translated_data = translate_json_obj(data)
            
            with open(new_path, 'w', encoding='utf-8') as f:
                json.dump(translated_data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Exception processing {file_path}: {e}")
        traceback.print_exc()

def main():
    files_to_process = []
    
    # Gather JSON
    for root, dirs, files in os.walk('data'):
        for file in files:
            if file.endswith('.json') and not file.endswith('.es.json'):
                files_to_process.append(os.path.join(root, file))
                
    # Gather Markdown
    for root, dirs, files in os.walk('content'):
        for file in files:
            if file.endswith('.md') and not file.endswith('.es.md'):
                files_to_process.append(os.path.join(root, file))
                
    print(f"Found {len(files_to_process)} files to process.")
    
    # Run synchronously to avoid rate limits or overlap
    for f in files_to_process:
        process_file(f)
        
    print("Done bridging files to .es.*")

if __name__ == '__main__':
    main()

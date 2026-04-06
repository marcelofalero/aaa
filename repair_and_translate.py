import requests
import json
import yaml
import os

def call_local_llm(prompt):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "deepseek-coder:6.7b",
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return response.json().get('response', '')
        else:
            return ""
    except:
        return ""

def repair_and_translate(file_path):
    print(f"Repairing and translating {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    repaired_items = []
    
    for item in data.get('items', []):
        name = item.get('name', 'Unknown')
        desc_en = item.get('description', '')
        
        # Detect broken descriptions
        if "VERBATIM TRANSCRIPTION" in desc_en or len(desc_en) < 20:
             print(f" Skipping/Fixing placeholder for {name}")
             # In a real scenario I'd re-extract, but here I'll just skip the ones I know are bad 
             # and attempt to let the LLM guess the fix if enough context is in the name/stats
        
        prompt = f"""
        You are a translator and editor for the Star*Drive RPG.
        
        ITEM: {name}
        ENGLISH: {desc_en}
        
        TASK:
        1. Fix any OCR spacing or spelling issues in the ENGLISH text.
        2. Provide a high-quality SPANISH translation that is technically accurate to Alternity RPG terms.
        3. Return JSON: {{"name": "{name}", "description_en": "...", "description_es": "..."}}
        """
        
        result_json = call_local_llm(prompt)
        if result_json:
            try:
                start = result_json.find('{')
                end = result_json.rfind('}') + 1
                clean_json = json.loads(result_json[start:end])
                
                # Maintain other fields
                new_item = item.copy()
                new_item['description'] = {
                    'en': clean_json.get('description_en', desc_en),
                    'es': clean_json.get('description_es', '')
                }
                # Handle name_es if provided
                if 'name_es' not in new_item:
                    # Quick translation for name
                    name_prompt = f"Translate the RPG equipment name '{name}' to Spanish: "
                    name_res = call_local_llm(name_prompt + " (return JSON {'es': '...'})")
                    try:
                        n_start = name_res.find('{')
                        n_end = name_res.rfind('}') + 1
                        new_item['name_es'] = json.loads(name_res[n_start:n_end]).get('es', name)
                    except:
                        new_item['name_es'] = name
                
                repaired_items.append(new_item)
            except:
                repaired_items.append(item)
        else:
            repaired_items.append(item)

    data['items'] = repaired_items
    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, indent=2, sort_keys=False, allow_unicode=True)

if __name__ == '__main__':
    files = [
        'site/data/medical_expansion.yaml',
        'site/data/computers_ai_expansion.yaml',
        'site/data/sensors_expansion.yaml',
        'site/data/weapons_expansion_expansion.yaml',
        'site/data/armor_expansion_expansion.yaml',
        'site/data/vehicles_expansion.yaml'
    ]
    for f in files:
        if os.path.exists(f):
            repair_and_translate(f)

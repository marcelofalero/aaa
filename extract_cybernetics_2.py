import requests
import json
import os
import yaml

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

def process_cybernetics():
    input_file = 'site/Equipment_full_ocr.txt'
    output_file = 'site/data/cybernetics_expansion.yaml'
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Range 4813 to 5578 - focusing on structural, sensory, and implants
    text = "".join(lines[4813:5578])
    
    # Smaller chunks to help LLM precision
    chunk_size = 2000
    overlap = 200
    
    chunks = []
    i = 0
    while i < len(text):
        chunks.append(text[i:i+chunk_size])
        if i + chunk_size >= len(text):
            break
        i += chunk_size - overlap
    
    all_items = []
    seen_names = set()
    
    for idx, chunk in enumerate(chunks):
        print(f"Processing Cybernetics: Chunk {idx+1}/{len(chunks)}...")
        prompt = f"""
        Extract RPG Cybernetic items from the OCR text. 
        Items often start with a letter like 'A. Artificial Ear' or 'B. Artificial Eye'.
        Include ANY item described (structural, sensory, implants, etc).
        
        ITEM SCHEMA (Return JSON LIST):
        [
            {{
                "name": "Exact Name",
                "pl": "7",
                "mass": "Mass (e.g. 100 g)",
                "cost": "Cost (e.g. $1,000 for Ordinary)",
                "avail": "Controlled",
                "description": "VERBATIM TRANSCRIPTION including mechanics (e.g. -1 step bonus)."
            }}
        ]
        
        Text:
        {chunk}
        """
        
        result = call_local_llm(prompt)
        if result:
            try:
                # Find start and end of JSON
                s = result.find('[')
                e = result.rfind(']') + 1
                if s != -1 and e != -1:
                    items = json.loads(result[s:e])
                    if isinstance(items, list):
                        for itm in items:
                            name = itm.get('name', '').strip()
                            if name and name not in seen_names:
                                all_items.append(itm)
                                seen_names.add(name)
            except:
                pass

    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump({"items": all_items}, f, indent=2, sort_keys=False, allow_unicode=True)
    print(f"Saved {len(all_items)} cybernetics items.")

if __name__ == '__main__':
    process_cybernetics()

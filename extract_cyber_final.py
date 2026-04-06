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

def extract_cybernetics_full():
    input_file = 'site/Equipment_full_ocr.txt'
    output_file = 'site/data/cybernetics_expansion.yaml'
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Range 4813 to 5578
    text = "".join(lines[4813:5578])
    
    # Small chunks to ensure verbatim capture
    chunk_size = 1500
    overlap = 100
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size - overlap)]
    
    all_items = []
    seen_names = set()
    
    for idx, chunk in enumerate(chunks):
        print(f"Extracting Cybernetics... Chunk {idx+1}/{len(chunks)}")
        prompt = f"""
        Extract every cybernetic enhancement specification from the text.
        Items are often listed with a letter (e.g. A. Artificial Ear).
        
        OUTPUT JSON LIST:
        [
            {{
                "name": "Exact Name",
                "pl": "7",
                "mass": "Mass/Dim",
                "cost": "Cost (e.g. $1,000)",
                "avail": "Controlled",
                "nanocomp": "Yes/No",
                "description": "FULL VERBATIM TRANSCRIPTION including rules and flavor."
            }}
        ]
        
        Text:
        {chunk}
        """
        res = call_local_llm(prompt)
        if res:
            try:
                s = res.find('[')
                e = res.rfind(']') + 1
                items = json.loads(res[s:e])
                for itm in items:
                    name = itm.get('name', '').strip()
                    if name and name not in seen_names:
                        all_items.append(itm)
                        seen_names.add(name)
            except:
                pass

    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump({"items": all_items}, f, indent=2, sort_keys=False, allow_unicode=True)
    print(f"Extraction complete. Found {len(all_items)} items.")

if __name__ == '__main__':
    extract_cybernetics_full()

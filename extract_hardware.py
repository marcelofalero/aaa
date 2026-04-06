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

def final_extraction_cybernetics():
    input_file = 'site/Equipment_full_ocr.txt'
    output_base = 'site/data/cybernetics_expansion'
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 4813 to 5578 is the focus for Cybernetics
    text = "".join(lines[4813:5578])
    
    chunk_size = 2500
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    
    all_items = []
    
    for idx, chunk in enumerate(chunks):
        print(f"Extracting items... {idx+1}/{len(chunks)}")
        prompt = f"""
        Extract every 'Hardware Specification' from the following list.
        Provide result as a JSON list of objects:
        [
            {{
                "name": "Component Name",
                "spec": "Verbatim technical description of the component functionality and rules.",
                "cost": "Cost value mentioned",
                "mass": "Mass value mentioned"
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
                    all_items.append({
                        "name": itm.get('name', ''),
                        "pl": "7",
                        "mass": itm.get('mass', '-'),
                        "cost": itm.get('cost', '-'),
                        "avail": "Controlled",
                        "description": itm.get('spec', '')
                    })
            except:
                pass

    # Save to expansion yaml
    with open(f'{output_base}.yaml', 'w', encoding='utf-8') as f:
        yaml.dump({"items": all_items}, f, indent=2, sort_keys=False, allow_unicode=True)
    print(f"Extraction complete. {len(all_items)} components found.")

if __name__ == '__main__':
    final_extraction_cybernetics()

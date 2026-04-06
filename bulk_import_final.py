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
            print(f"Error: {response.status_code}")
            return ""
    except Exception as e:
        print(f"Connection error: {e}")
        return ""

def process_section(section_name, start_line, end_line):
    input_file = 'site/Equipment_full_ocr.txt'
    output_file = f'site/data/{section_name}_expansion.yaml'
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Bound check
    start_line = max(0, start_line)
    end_line = min(len(lines), end_line)
    
    text = "".join(lines[start_line:end_line])
    
    chunk_size = 4000
    overlap = 500
    
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
        print(f"Processing {section_name}: Chunk {idx+1}/{len(chunks)}...")
        prompt = f"""
        Extract EVERY RPG equipment item from this 'Arms & Equipment' guide OCR text.
        
        ITEM SCHEMA (Return a JSON LIST):
        [
            {{
                "name": "Exact Name",
                "pl": "7",
                "mass": "Mass (kg)",
                "cost": "Cost ($ or #)",
                "avail": "Availability",
                "description": "VERBATIM TRANSCRIPTION of the text. Include all rules, mechanics, flavor, and stats mentioned."
            }}
        ]

        HINT: Assume PL 7 for Star*Drive items if not specified.
        OCR Text:
        {chunk}
        """
        
        result = call_local_llm(prompt)
        if result:
            try:
                start = result.find('[')
                end = result.rfind(']') + 1
                if start != -1 and end != -1:
                    items = json.loads(result[start:end])
                    for item in items:
                        name = item.get('name', '').strip()
                        if name and name not in seen_names:
                            all_items.append(item)
                            seen_names.add(name)
                else:
                    # Check for single object
                    start = result.find('{')
                    end = result.rfind('}') + 1
                    if start != -1:
                        item = json.loads(result[start:end])
                        name = item.get('name', '').strip()
                        if name and name not in seen_names:
                            all_items.append(item)
                            seen_names.add(name)
            except Exception as e:
                print(f"Parse error in chunk {idx+1}: {e}")

    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump({"items": all_items}, f, indent=2, sort_keys=False, allow_unicode=True)
    print(f"Saved {len(all_items)} items to {output_file}")

if __name__ == '__main__':
    # Systematic extraction of the entire guide
    sections = [
        ("medical", 1683, 2050),
        ("computers_ai", 4465, 5000),
        ("sensors", 100, 500), # Includes communications
        ("weapons_expansion", 5500, 7500),
        ("armor_expansion", 7500, 9200),
        ("vehicles", 9200, 10300)
    ]
    
    for name, start, end in sections:
        process_section(name, start, end)

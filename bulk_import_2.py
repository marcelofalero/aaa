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
    
    text = "".join(lines[start_line:end_line])
    
    # Larger chunks to allow context for multiple items
    chunk_size = 3000
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    
    all_items = []
    
    for i, chunk in enumerate(chunks):
        print(f"Processing chunk {i+1}/{len(chunks)} of {section_name}...")
        prompt = f"""
        Extract EVERY RPG equipment item mentioned in this OCR text from the Star*Drive 'Arms & Equipment' guide.
        
        ITEM SCHEMA (Return a JSON LIST even if only one item is found):
        [
            {{
                "name": "Exact Item Name",
                "pl": "7",
                "mass": "Mass (e.g. 0.5 kg)",
                "cost": "Cost (e.g. $50 or #1,200)",
                "avail": "Availability (Any, Common, Controlled, Military, Restricted)",
                "description": "VERBATIM TRANSCRIPTION of the text. Include ALL mechanics, rules, and flavor text. Do not omit anything."
            }}
        ]

        OCR Text:
        {chunk}
        """
        
        result = call_local_llm(prompt)
        if result:
            try:
                # Find start and end of JSON content
                start_idx = -1
                end_idx = -1
                if '[' in result:
                    start_idx = result.find('[')
                    end_idx = result.rfind(']') + 1
                elif '{' in result:
                    start_idx = result.find('{')
                    end_idx = result.rfind('}') + 1
                
                if start_idx != -1 and end_idx != -1:
                    json_data = json.loads(result[start_idx:end_idx])
                    if isinstance(json_data, list):
                        all_items.extend(json_data)
                    elif isinstance(json_data, dict):
                        all_items.append(json_data)
                else:
                    print(f"No JSON found in chunk {i+1}")
            except Exception as e:
                print(f"Failed to parse chunk {i+1}: {e}")

    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump({"items": all_items}, f, indent=2, sort_keys=False, allow_unicode=True)
    print(f"Written {len(all_items)} items to {output_file}")

if __name__ == '__main__':
    # Full capture of the book in main sections
    # 1. Sensors & Computers (Pages 3-10ish)
    # 2. Weapons (Pages 11-30ish)
    # 3. Clothing & Accessories
    # 4. Medical
    # 5. Vehicles
    # 6. Ships
    
    sections = [
        ("medical", 1683, 2050),
        ("sensors", 100, 500), # Approximated
        ("weapons_expansion", 5500, 7500) # Approximated based on previous grep
    ]
    
    for name, start, end in sections:
        process_section(name, start, end)

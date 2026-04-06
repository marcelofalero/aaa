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
    
    # Smaller chunks to improve accuracy
    chunk_size = 2000
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    
    all_items = []
    
    for i, chunk in enumerate(chunks):
        print(f"Processing chunk {i+1}/{len(chunks)} of {section_name}...")
        prompt = f"""
        Extract RPG equipment items from the Star*Drive 'Arms & Equipment' guide OCR text.
        
        ITEM SCHEMA (JSON List):
        [
            {{
                "name": "Item Name",
                "pl": "7",
                "mass": "Mass in kg",
                "cost": "Cost in $",
                "avail": "Availability (Any, Common, Controlled, Military, Restricted)",
                "description": "VERBATIM TRANSCRIPTION of the text. Include all rules, mechanics, and flavor text. Do not summarize."
            }}
        ]

        OCR HINT: 
        - Headers are often in ALL CAPS like 'IsoMep ARTIFICIAL BLooD'.
        - Stats often look like: 'Item 200050101, $50, 0.3 kg, Common'.
        - Assume PL 7 if not explicitly mentioned.

        OCR Text:
        {chunk}
        """
        
        result = call_local_llm(prompt)
        if result:
            # Try to strip any potential non-JSON noise from Ollama
            try:
                # Find the first [ and last ]
                start = result.find('[')
                end = result.rfind(']') + 1
                if start != -1 and end != -1:
                    json_str = result[start:end]
                    items = json.loads(json_str)
                    if isinstance(items, list):
                        all_items.extend(items)
                else:
                    print(f"No JSON list found in response for chunk {i+1}")
                    print(f"LLM Response snippet: {result[:500]}")
            except Exception as e:
                print(f"Failed to parse JSON from chunk {i+1}: {e}")
                print(f"LLM Response snippet: {result[:200]}")

    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump({"items": all_items}, f, indent=2, sort_keys=False, allow_unicode=True)
    print(f"Written {len(all_items)} items to {output_file}")

if __name__ == '__main__':
    # Initial run on Medical section as per requirement
    process_section("medical", 1683, 2050)

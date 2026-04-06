import requests
import json
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
            print(f"Error: {response.status_code}")
            return ""
    except Exception as e:
        print(f"Connection error: {e}")
        return ""

def process_file_with_llm():
    input_file = 'site/Equipment_all_ocr.txt'
    output_file = 'site/data/extracted_armor.yaml'
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    # Split into chunks around keywords like "Availability" or "Cost" to keep items together
    # For now, simple length-based chunking with overlap
    chunk_size = 3000
    overlap = 500
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunks.append(text[i:i + chunk_size])

    print(f"Processing {len(chunks)} chunks...")
    
    with open(output_file, 'w', encoding='utf-8') as out:
        out.write("items:\n")
        
    for i, chunk in enumerate(chunks):
        print(f"Processing chunk {i+1}/{len(chunks)}...")
        prompt = f"""
        Extract RPG Armor equipment from this OCR text.
        Return a JSON list of objects. Each object MUST have:
        - name
        - availability
        - cost
        - mass
        - protection (the LI/HI/En values)
        - hide
        - type (if specified like combat, powered, etc)
        - description (VERBATIM from the text)
        
        Text:
        {chunk}
        """
        result_json = call_local_llm(prompt)
        if result_json:
            try:
                # Clean up if the LLM adds markdown or extra text
                # We asked for format: json, so it should be clean
                items = json.loads(result_json)
                if isinstance(items, list):
                    # Convert to YAML-like lines and append
                    import yaml
                    with open(output_file, 'a', encoding='utf-8') as out:
                        for item in items:
                            yaml.dump([item], out, sort_keys=False, allow_unicode=True)
            except Exception as e:
                print(f"Failed to parse JSON from chunk {i+1}: {e}")
                # Log the raw response for debugging
                with open('llm_error.log', 'a') as log:
                    log.write(f"\nCHUNK {i+1} ERROR:\n{result_json}\n")

if __name__ == '__main__':
    process_file_with_llm()

import requests
import os
import yaml

def call_local_llm(prompt):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "deepseek-coder:6.7b",
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return response.json().get('response', '')
        else:
            return ""
    except:
        return ""

def process_cybernetics_simple():
    input_file = 'site/Equipment_full_ocr.txt'
    output_file = 'site/data/cybernetics_expansion_raw.yaml'
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Sensory Cyberware section
    text = "".join(lines[4813:5578])
    
    chunk_size = 4000
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    
    raw_results = []
    
    for idx, chunk in enumerate(chunks):
        print(f"Extracting Chunk {idx+1}/{len(chunks)}...")
        prompt = f"""
        Identify every cybernetic implant in this text. 
        For each, copy the NAME and the FULL DESCRIPTION verbatim.
        
        Text:
        {chunk}
        """
        res = call_local_llm(prompt)
        if res:
            raw_results.append(res)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n\n---CHUNK SEPARATOR---\n\n".join(raw_results))
    print(f"Saved raw extraction to {output_file}")

if __name__ == '__main__':
    process_cybernetics_simple()

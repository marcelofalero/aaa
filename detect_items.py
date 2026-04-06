import requests
import os

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

def identify_items():
    input_file = 'site/Equipment_full_ocr.txt'
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    text = "".join(lines[4813:5000]) # First chunk of cyberware
    
    prompt = f"""
    List only the names of the equipment items described in this text.
    Format: 1. Item Name
    
    Text:
    {text}
    """
    print(call_local_llm(prompt))

if __name__ == '__main__':
    identify_items()

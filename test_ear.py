import requests
import json

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

def test_ear():
    input_file = 'site/Equipment_full_ocr.txt'
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    text = "".join(lines[4826:4842])
    
    prompt = f"""
    Extract the product information from this text. 
    Name, Description, and any tables or stats.
    
    Text:
    {text}
    """
    print(call_local_llm(prompt))

if __name__ == '__main__':
    test_ear()

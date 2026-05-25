import sys
import re
import yaml
from ruamel.yaml import YAML

# Initialize ruamel.yaml for round-tripping
yaml_ruamel = YAML()
yaml_ruamel.preserve_quotes = True
yaml_ruamel.width = 70
yaml_ruamel.indent(mapping=2, sequence=4, offset=2)

def smart_wrap(text, width=55):
    if not text or not isinstance(text, str):
        return text
    
    # Normalize whitespace: convert multiple spaces/newlines to single spaces
    # BUT preserve existing double newlines (paragraphs)
    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
    text = re.sub(r' +', ' ', text)
    
    # Tokenize: Extract technical blocks first to keep them atomic
    # Matches [text](url) (with optional space between) or {{< shortcode >}}
    token_pattern = r'(\[[\s\S]*?\]\s*\([\s\S]*?\)|{{<[\s\S]*?>}})'
    parts = re.split(token_pattern, text)
    
    new_lines = []
    current_line = ""
    
    # Process each part
    for part in parts:
        if not part: continue
        
        # If it's a technical token, split Markdown links into two words to allow wrapping
        if re.match(token_pattern, part):
            if part.startswith('['):
                match = re.match(r'(\[[\s\S]*?\])\s*(\([\s\S]*?\))', part)
                if match:
                    words = [match.group(1), match.group(2)]
                else:
                    words = [part]
            else:
                words = [part]
        else:
            # It's regular text, split into words
            words = part.split(' ')
            
        for word in words:
            if not word: continue
            
            # Check if adding this word (and a space) exceeds width
            test_line = (current_line + " " + word).strip()
            if len(test_line) <= width:
                current_line = test_line
            else:
                if current_line:
                    new_lines.append(current_line)
                current_line = word
                
    if current_line:
        new_lines.append(current_line)
        
    return "\n".join(new_lines)

def process_file(file_path):
    print(f"Processing {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml_ruamel.load(f)
    
    def walk_data(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if isinstance(v, str) and len(v) > 50:
                    node[k] = smart_wrap(v)
                else:
                    walk_data(node[k])
        elif isinstance(node, list):
            for i in range(len(node)):
                if isinstance(node[i], str) and len(node[i]) > 50:
                    node[i] = smart_wrap(node[i])
                else:
                    walk_data(node[i])

    walk_data(data)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        yaml_ruamel.dump(data, f)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 robust_yaml_formatter.py <file1> <file2> ...")
        sys.exit(1)
    
    for arg in sys.argv[1:]:
        process_file(arg)

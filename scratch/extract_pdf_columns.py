import sys
import re

def parse_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    pages = content.split('\x0c')
    
    GUTTER_START = 40
    GUTTER_END = 70
    
    with open(output_path, 'w', encoding='utf-8') as out:
        for page_idx, page in enumerate(pages):
            lines = page.split('\n')
            
            left_col = []
            right_col = []
            
            def flush_cols():
                nonlocal left_col, right_col
                if left_col:
                    out.write('\n'.join(left_col) + '\n\n')
                    left_col = []
                if right_col:
                    out.write('\n'.join(right_col) + '\n\n')
                    right_col = []
            
            for line in lines:
                stripped = line.rstrip()
                if not stripped:
                    continue
                
                # Check for 3 or more spaces
                matches = list(re.finditer(r' {3,}', stripped))
                
                gutter_match = None
                for m in matches:
                    start, end = m.span()
                    if start <= GUTTER_END and end >= GUTTER_START:
                        gutter_match = m
                        break
                
                if gutter_match:
                    start, end = gutter_match.span()
                    left_text = stripped[:start].strip()
                    right_text = stripped[end:].strip()
                    
                    if left_text:
                        left_col.append(left_text)
                    if right_text:
                        right_col.append(right_text)
                else:
                    first_char_idx = len(stripped) - len(stripped.lstrip())
                    
                    # If it doesn't even reach the right column, it's left
                    if len(stripped) <= GUTTER_END - 5:
                        left_col.append(stripped.strip())
                    # If it starts exactly where the right column should, it's right
                    elif first_char_idx >= GUTTER_START - 5:
                        right_col.append(stripped.strip())
                    else:
                        flush_cols()
                        out.write(stripped.strip() + '\n\n')
            
            flush_cols()
            out.write('\n--- PAGE BREAK ---\n\n')
            
if __name__ == '__main__':
    parse_file(sys.argv[1], sys.argv[2])

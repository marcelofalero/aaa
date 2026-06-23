import re

with open('scratch/ends_output.txt', 'r', encoding='utf-8') as f:
    text = f.read()

blocks = text.split("--- START: ")
for b in blocks[1:]:
    lines = b.split('\n')
    title = lines[0].strip()
    
    # We want to find the last line of the table. 
    # Usually, a table in warships_clean.txt is a bunch of lines with multiple spaces.
    # The first line that is a normal paragraph (less spaces) might be the end.
    print(f"TITLE: {title}")
    # just print the last few lines to manually inspect
    for i in range(20, 35):
        if i < len(lines):
            print(lines[i])
    print("-------")

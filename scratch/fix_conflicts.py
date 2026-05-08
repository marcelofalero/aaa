import os
import re

def resolve_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match conflict markers and keep HEAD version
    # <<<<<<< HEAD
    # OURS
    # =======
    # THEIRS
    # >>>>>>> ...
    pattern = re.compile(r'<<<<<<< HEAD\n(.*?)\n=======\n.*?\n>>>>>>> .*?\n', re.DOTALL)
    
    new_content = pattern.sub(r'\1\n', content)
    
    if new_content != content:
        print(f"Resolved: {filepath}")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

def main():
    files_with_conflicts = [
        "roll20_charsheet/Alternity_RPG.html",
        "site/data/skills-table.json",
        "site/data/skills.json",
        "site/data/skills-table.es.json",
        "sources/data_sources/skills.yaml"
    ]
    
    # Add all .md files in site/content/skills/
    for root, dirs, files in os.walk("site/content/skills"):
        for file in files:
            if file.endswith(".md"):
                files_with_conflicts.append(os.path.join(root, file))
                
    for f in files_with_conflicts:
        if os.path.exists(f):
            resolve_file(f)

if __name__ == "__main__":
    main()

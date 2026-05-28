import re
import sys
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap, CommentedSeq

def extract_benefits(text):
    if not text or not isinstance(text, str):
        return []
    # Regex pattern: look for Rank/rank followed by numbers, and then a bracketed title
    # e.g., "Rank 3, 6, 9, 12 [Increased Effect]"
    # e.g., "- **At rank 5, 9 [Increased Damage]**"
    # e.g., "Rank 4[Improved Balance]"
    pattern = re.compile(r'(?:Rank|rank)\s*([\d\s,a-d/&-]+)\s*\[([^\]]+)\]', re.IGNORECASE)
    
    benefits = []
    for match in pattern.finditer(text):
        ranks_str = match.group(1)
        title = match.group(2).strip()
        ranks = [int(x) for x in re.findall(r'\d+', ranks_str)]
        for r in ranks:
            benefits.append({'rank': r, 'title': title})
    return benefits

def update_item_benefits(key, val, parent_name=None):
    en_loc = None
    if 'localized' in val:
        en_loc = next((loc['en'] for loc in val['localized'] if 'en' in loc), None)
        
    desc = ""
    if en_loc and 'description' in en_loc:
        desc = en_loc['description']
    elif 'description' in val:
        desc = val['description']
        
    extracted = extract_benefits(desc)
    if not extracted:
        # Check if we should recurse into items
        changed = False
        if 'items' in val and isinstance(val['items'], dict):
            for sub_key, sub_val in val['items'].items():
                if update_item_benefits(sub_key, sub_val, key):
                    changed = True
        return changed

    # Determine where the current rank_benefits belongs
    # If the root level has a non-None rank_benefits field, or if en_loc does not exist/does not have it
    target_obj = val
    if en_loc and 'rank_benefits' in en_loc and 'rank_benefits' not in val:
        target_obj = en_loc
        
    current_rb = target_obj.get('rank_benefits')
    
    # Standardize the extracted benefits to match ruamel.yaml structure if needed
    # We want CommentedSeq of CommentedMap
    new_rb = CommentedSeq()
    for b in extracted:
        item = CommentedMap()
        item['rank'] = b['rank']
        item['title'] = b['title']
        new_rb.append(item)
        
    # Compare to see if updated
    def is_equal(seq1, seq2):
        if not seq1 and not seq2:
            return True
        if not seq1 or not seq2:
            return False
        if len(seq1) != len(seq2):
            return False
        for a, b in zip(seq1, seq2):
            if a.get('rank') != b.get('rank') or a.get('title') != b.get('title'):
                return False
        return True

    if not is_equal(current_rb, new_rb):
        label = f"{parent_name} -> {key}" if parent_name else key
        print(f"Updating {label}:")
        print(f"  Old: {list(current_rb) if current_rb else 'None'}")
        print(f"  New: {list(new_rb)}")
        target_obj['rank_benefits'] = new_rb
        return True
        
    # Recurse into sub-items
    changed = False
    if 'items' in val and isinstance(val['items'], dict):
        for sub_key, sub_val in val['items'].items():
            if update_item_benefits(sub_key, sub_val, key):
                changed = True
    return changed

def process_file(file_path, commit=False):
    print(f"\nProcessing {file_path}...")
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.allow_unicode = True
    yaml.width = 1000
    yaml.indent(mapping=2, sequence=4, offset=2)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.load(f)
        
    items = data.get('items', data)
    
    changed = False
    for key, val in items.items():
        if update_item_benefits(key, val):
            changed = True
            
    if changed and commit:
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f)
        print(f"Successfully updated and saved {file_path}.")
    elif changed:
        print(f"Dry run complete. Changes detected in {file_path}. Run with --commit to save.")
    else:
        print(f"No changes needed for {file_path}.")

if __name__ == '__main__':
    commit = '--commit' in sys.argv
    process_file('sources/data_sources/skills.yaml', commit=commit)
    process_file('sources/data_sources/psionics.yaml', commit=commit)

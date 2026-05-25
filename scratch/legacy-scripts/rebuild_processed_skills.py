import sys
from ruamel.yaml import YAML

yaml = YAML(typ='safe')
try:
    with open('sources/data_sources/skills.yaml', 'r', encoding='utf-8') as f:
        data = yaml.load(f)
        
    if 'items' in data:
        data = data['items']
        
except Exception as e:
    print(f"Error reading YAML: {e}")
    sys.exit(1)

markdown_content = ""

# The skills we have been working on
target_skills = [
    'acrobatics', 'administration', 'animal-handling', 'armor-operation',
    'athletics', 'awareness', 'business', 'computer-science', 'covert-ops',
    'creativity', 'culture'
]

for key in sorted(target_skills):
    if key in data:
        skill_data = data[key]
        
        en_loc = None
        for loc in skill_data.get('localized', []):
            if 'en' in loc:
                en_loc = loc['en']
                break
                
        if en_loc:
            name = en_loc.get('name', key.replace('-', ' ').title())
            desc = en_loc.get('description', '')
            markdown_content += f"# {name} (Broad Skill)\n{desc}\n\n"
            
            items = skill_data.get('items', {})
            for item_key in sorted(items.keys()):
                item_data = items[item_key]
                item_en_loc = None
                for loc in item_data.get('localized', []):
                    if 'en' in loc:
                        item_en_loc = loc['en']
                        break
                
                if item_en_loc:
                    item_name = item_en_loc.get('name', item_key.replace('-', ' ').title())
                    item_desc = item_en_loc.get('description', '')
                    markdown_content += f"## {item_name} (Specialty)\n{item_desc}\n"
                    
                    # Append Rank Benefits if they exist separately in the YAML structure
                    rank_benefits = item_data.get('rank_benefits', [])
                    if rank_benefits:
                        markdown_content += "\n### YAML Rank Benefits (Mechanical Triggers)\n"
                        for benefit in rank_benefits:
                            rank = benefit.get('rank')
                            title = benefit.get('title', 'Benefit')
                            markdown_content += f"- **Rank {rank}:** {title}\n"
                            
                    markdown_content += "\n"

with open('sources/processed-skills.md', 'w', encoding='utf-8') as f:
    f.write(markdown_content)

print("Successfully rebuilt processed-skills.md with all YAML descriptions and mechanical rank triggers.")
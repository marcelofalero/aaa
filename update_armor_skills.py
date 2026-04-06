import yaml
import re

def update_armor_skills():
    file_path = 'site/data_sources/armor.yaml'
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    # All armors now use combat armor subskill
    target_skill = "Armor Operation—combat armor"
    target_skill_es = "Operación de Armadura—armadura de combate"

    for cat_id, cat in data['categories'].items():
        is_powered_cat = (cat_id == 'powered')
        for grp_id, items in cat['groups'].items():
            for item in items:
                # Add Power Armor field
                # If they are in the powered category, it's True
                item['power_armor'] = True if is_powered_cat else False
                
                # Add Skill field
                item['skill_req'] = target_skill
                
                # Sweep descriptions to update any mention of the skill
                # Standardizing dash as — (em dash used in book)
                for lang in ['en', 'es']:
                    if lang in item['description']:
                        desc = item['description'][lang]
                        # Replace any "armor operation—powered armor" regardless of dash type
                        desc = re.sub(r'Armor Operation[-—]powered armor', target_skill, desc, flags=re.IGNORECASE)
                        desc = re.sub(r'Armor Operation[-—]combat armor', target_skill, desc, flags=re.IGNORECASE)
                        
                        # Spanish replacements
                        desc = re.sub(r'Operación de Armadura[-—]armadura de combate', target_skill_es, desc, flags=re.IGNORECASE)
                        desc = re.sub(r'Operación de Armadura[-—]armadura motorizada', target_skill_es, desc, flags=re.IGNORECASE)
                        
                        # Add the field to the stat block in the description if it exists
                        # I'll replace the existing skill line or add it
                        if "**Skill Required:**" not in desc and lang == 'en':
                             desc += f"\n- **Skill Required:** {target_skill}"
                        if "**Habilidad Requerida:**" not in desc and lang == 'es':
                             desc += f"\n- **Habilidad Requerida:** {target_skill_es}"
                        
                        item['description'][lang] = desc

    # Re-syncing the stat blocks from my previous turn too
    # I'll make sure the Power Armor field is in the displayed stat block too
    for cat_id, cat in data['categories'].items():
        for grp_id, items in cat['groups'].items():
            for item in items:
                for lang in ['en', 'es']:
                    desc = item['description'][lang]
                    pa_status = "Yes" if item.get('power_armor') else "No"
                    pa_status_es = "Sí" if item.get('power_armor') else "No"
                    
                    if lang == 'en':
                        if "- **Power Armor:**" not in desc:
                             desc = desc.replace("**Stat Block:**", f"**Stat Block:**\n- **Power Armor:** {pa_status}")
                    else:
                        if "- **Armadura Motorizada:**" not in desc:
                             desc = desc.replace("**Bloque de Estadísticas:**", f"**Bloque de Estadísticas:**\n- **Armadura Motorizada:** {pa_status_es}")
                    
                    item['description'][lang] = desc

    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, indent=2, sort_keys=False, allow_unicode=True)
    print("Armor skills updated and Power Armor field added.")

if __name__ == '__main__':
    update_armor_skills()

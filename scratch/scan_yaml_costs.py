import csv
from ruamel.yaml import YAML

# Hardcoded rulebook costs from the provided images
RULEBOOK_COSTS = {
    "Acrobatics": 7,
    "Daredevil": 4,
    "Dodge": 4,
    "Fall": 3,
    "Zero-g Training": 2,
    "Administration": 4,
    "Bureaucracy": 3,
    "Management": 3,
    "Animal Handling": 3,
    "Animal riding": 1,
    "Animal training": 1,
    "Armor Operation": 7,
    "Combat armor": 3,
    "Athletics": 3,
    "Climb": 2,
    "Jump": 1,
    "Swim": 1,
    "Throw": 2,
    "Awareness": 3,
    "Intuition": 3,
    "Perception": 2,
    "Business": 4,
    "Corporate": 3,
    "Illicit business": 3,
    "Small business": 3,
    "Computer Science": 7,
    "Hacking": 5,
    "Hardware": 4,
    "Programming": 4,
    "Demolitions": 6,
    "Disarm": 4,
    "Set explosives": 3,
    "Knowledge": 3,
    "Computer Operation": 1,
    "Deduce": 2,
    "First Aid": 2,
    "Law": 5,
    "Court procedures": 3,
    "Leadership": 4,
    "Command": 4,
    "Inspire": 4,
    "Life Science": 7,
    "Biology": 3,
    "Botany": 3,
    "Genetics": 3,
    "Xenology": 4,
    "Zoology": 3,
    "Medical Science": 7,
    "Forensics": 3,
    "Medical Knowledge": 3,
    "Psychology": 3,
    "Surgery": 5,
    "Treatment": 4,
    "Navigation": 6,
    "Physical Science": 7,
    "Astronomy": 3,
    "Chemistry": 3,
    "Physics": 3,
    "Planetology": 3,
    "Security": 5,
    "Protection protocols": 3,
    "Security devices": 3,
    "System Operation": 4,
    "Communications": 3,
    "Defenses": 3,
    "Engineering": 3,
    "Sensors": 3,
    "Weapons": 3,
    "Tactics": 6,
    "Infantry tactics": 3,
    "Space tactics": 3,
    "Vehicle tactics": 3,
    "Technical Science": 7,
    "Technical Knowledge": 3,
    "Invention": 4,
    "Repair": 3,
    "Juryrig": 3,
    "Vehicle Operation": 3,
    "Air vehicle": 5,
    "Land vehicle": 3,
    "Space vehicle": 5,
    "Water vehicle": 3,
    "Pickpocket": 4,
    "Creativity": 4,
    "Investigate": 7,
    "Interrogate": 4,
    "Search": 4,
    "Track": 4,
    "Resolve": 5,
    "Mental resolve": 3,
    "Physical resolve": 3,
    "Street Smart": 5,
    "Street Knowledge": 3,
    "Criminal elements": 3,
    "Culture": 5,
    "Diplomacy": 3,
    "First Encounter": 3,
    "Deception": 5,
    "Bluff": 3,
    "Bribe": 3,
    "Entertainment": 4,
    "Act": 2,
    "Dance": 2,
    "Musical instrument": 2,
    "Sing": 2,
    "Heavy Weapons": 6,
    "Direct fire": 4,
    "Indirect fire": 4,
    "Interaction": 3,
    "Bargain": 3,
    "Charm": 3,
    "Interview": 3,
    "Intimidate": 3,
    "Seduce": 3,
    "Taunt": 2,
    "Defensive Martial Arts": 5,
    "Power Martial Arts": 5,
    "Trailblazing": 3,
    "Endurance": 4,
    "Resist pain": 4,
    "Survival": 5,
    "Survival training": 3,
    "Pistol": 4,
    "Rifle": 4,
    "SMG": 4,
    "Bow": 4,
    "Crossbow": 3,
    "Flintlock": 3,
    "Sling": 4,
    "Blade": 3,
}

def scan_skills_costs_csv(yaml_path, output_csv_path):
    yaml = YAML()
    with open(yaml_path, 'r', encoding='utf-8') as f:
        yaml_data = yaml.load(f)

    rows = []
    
    # Iterate through broad skills
    for broad_key, broad_val in yaml_data.get('items', {}).items():
        # Get English name
        broad_name = broad_key
        localized = broad_val.get('localized', [])
        for lang_dict in localized:
            if 'en' in lang_dict:
                broad_name = lang_dict['en'].get('name', broad_key)
                break
        
        cost = broad_val.get('cost')
        rb_cost = RULEBOOK_COSTS.get(broad_name, '')
        
        # Add Broad Skill row
        rows.append({
            'Skill Type': 'Broad',
            'Broad Skill': broad_name,
            'Skill Name': broad_name,
            'Cost': cost,
            'Rulebook Cost': rb_cost
        })
        
        # Iterate through specialty skills under this broad skill
        for spec_key, spec_val in broad_val.get('items', {}).items():
            spec_name = spec_key
            spec_localized = spec_val.get('localized', [])
            for lang_dict in spec_localized:
                if 'en' in lang_dict:
                    spec_name = lang_dict['en'].get('name', spec_key)
                    break
            
            spec_cost = spec_val.get('cost')
            rb_spec_cost = RULEBOOK_COSTS.get(spec_name, '')
            
            # Add Specialty Skill row
            rows.append({
                'Skill Type': 'Specialty',
                'Broad Skill': broad_name,
                'Skill Name': spec_name,
                'Cost': spec_cost,
                'Rulebook Cost': rb_spec_cost
            })

    # Write to CSV file
    with open(output_csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['Skill Type', 'Broad Skill', 'Skill Name', 'Cost', 'Rulebook Cost'])
        writer.writeheader()
        writer.writerows(rows)
        
    print(f"Successfully wrote {len(rows)} skills and costs to {output_csv_path}")

if __name__ == "__main__":
    scan_skills_costs_csv('sources/data_sources/skills.yaml', 'scratch/current_skills_costs.csv')

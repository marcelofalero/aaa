import yaml

def check_rank_benefits(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    items = data.get('items', data)
    for broad_key, broad_val in items.items():
        if 'rank_benefits' in broad_val:
            print(f"Broad skill '{broad_key}' has rank_benefits")
        
        specs = broad_val.get('items', {})
        for spec_key, spec_val in specs.items():
            if 'rank_benefits' in spec_val:
                # print(f"  Spec '{spec_key}' has rank_benefits")
                pass
            
            # Check inside localized en
            loc = broad_val.get('localized', [])
            en_loc = next((l['en'] for l in loc if 'en' in l), None)
            if en_loc and 'rank_benefits' in en_loc:
                 print(f"Broad skill '{broad_key}' has rank_benefits in EN localization")
                 
            spec_loc = spec_val.get('localized', [])
            spec_en_loc = next((l['en'] for l in spec_loc if 'en' in l), None)
            if spec_en_loc and 'rank_benefits' in spec_en_loc:
                 print(f"  Spec '{spec_key}' has rank_benefits in EN localization")

print("Checking skills.yaml:")
check_rank_benefits('sources/data_sources/skills.yaml')
print("\nChecking psionics.yaml:")
check_rank_benefits('sources/data_sources/psionics.yaml')

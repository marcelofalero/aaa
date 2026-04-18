import os
import yaml

# Custom YAML dumper for better formatting
class FoldedDumper(yaml.SafeDumper):
    pass

def folded_str_representer(dumper, data):
    if len(data.splitlines()) > 1:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

FoldedDumper.add_representer(str, folded_str_representer)

CORRECTIONS = {
    "Biokinesis": {"cost": 6, "items": {
        "bio-armor": {"cost": 3, "trained_only": True},
        "bioweapon": {"cost": 3, "trained_only": True},
        "clamber": {"cost": 2, "trained_only": False},
        "control-metabolism": {"cost": 2, "trained_only": False},
        "heal": {"cost": 4, "trained_only": True},
        "intangibility": {"cost": 4, "trained_only": True},
        "morph": {"cost": 4, "trained_only": True},
        "rejuvenate": {"cost": 3, "trained_only": True},
        "shatter": {"cost": 3, "trained_only": False},
        "transfer-damage": {"cost": 2, "trained_only": False},
    }},
    "ESP": {"cost": 5, "items": {
        "battle-mind": {"cost": 4, "trained_only": False},
        "clairaudience": {"cost": 2, "trained_only": False},
        "clairvoyance": {"cost": 2, "trained_only": False},
        "dream-hunt": {"cost": 3, "trained_only": False, "alien_only": True},
        "empathy": {"cost": 1, "trained_only": False},
        "mind-reading": {"cost": 3, "trained_only": False},
        "navcognition": {"cost": 3, "trained_only": True},
        "postcognition": {"cost": 3, "trained_only": False},
        "precognition": {"cost": 4, "trained_only": True},
        "psychometry": {"cost": 3, "trained_only": False},
        "sensitivity": {"cost": 2, "trained_only": False},
    }},
    "Psychoportation": {"cost": 7, "items": {
        "alter-speed": {"cost": 4, "trained_only": True},
        "apportation": {"cost": 6, "trained_only": True},
        "dimension-walk": {"cost": 6, "trained_only": True}, # Needs adding
        "duplicate": {"cost": 6, "trained_only": True},
        "teleportation": {"cost": 5, "trained_only": True},
        "timeslip": {"cost": 6, "trained_only": True},
    }},
    "Telekinesis": {"cost": 6, "items": {
        "cryokinetics": {"cost": 3, "trained_only": True},
        "electrokinetics": {"cost": 3, "trained_only": True},
        "kinetic-blow": {"cost": 3, "trained_only": True},
        "kinetic-shield": {"cost": 2, "trained_only": False},
        "levitation": {"cost": 2, "trained_only": False},
        "photokinetics": {"cost": 1, "trained_only": True},
        "psychokinetics": {"cost": 3, "trained_only": True},
        "pyrokinesis": {"cost": 4, "trained_only": True},
        "sheya's-clutch": {"cost": 5, "trained_only": True, "alien_only": True},
    }},
    "Telepathy": {"cost": 5, "items": {
        "contact": {"cost": 3, "trained_only": False},
        "datalink": {"cost": 4, "trained_only": False},
        "drain": {"cost": 4, "trained_only": True},
        "empathic-projection": {"cost": 3, "trained_only": False},
        "guidance": {"cost": 4, "trained_only": False},
        "illusion": {"cost": 3, "trained_only": False},
        "mind-blast": {"cost": 4, "trained_only": True},
        "mind-shield": {"cost": 2, "trained_only": False},
        "mind-wipe": {"cost": 4, "trained_only": True},
        "psychic-armor": {"cost": 2, "trained_only": False},
        "psychic-projection": {"cost": 3, "trained_only": False},
        "subdual": {"cost": 3, "trained_only": True},
        "suggest": {"cost": 3, "trained_only": False},
        "tire": {"cost": 3, "trained_only": True},
        "undo": {"cost": 3, "trained_only": True},
    }}
}

def main():
    root_dir = "/home/dimble/projects/aaa"
    yaml_path = os.path.join(root_dir, "sources/data_sources/psionics.yaml")
    
    with open(yaml_path, 'r', encoding='utf-8') as f:
        psionics_data = yaml.safe_load(f)
    
    for disc_key, disc_corr in CORRECTIONS.items():
        if disc_key in psionics_data['items']:
            disc_data = psionics_data['items'][disc_key]
            disc_data['cost'] = disc_corr['cost']
            
            items = disc_data.get('items', {})
            for item_id, item_corr in disc_corr['items'].items():
                if item_id in items:
                    item_data = items[item_id]
                    item_data['cost'] = item_corr['cost']
                    item_data['trained_only'] = item_corr['trained_only']
                    if item_corr.get('alien_only'):
                        item_data['alien_only'] = True
                    print(f"Updated {item_id}")
                else:
                    # Special case for missing items like dimension-walk
                    if item_id == "dimension-walk":
                        items[item_id] = {
                            "attribute": "WIL",
                            "cost": 6,
                            "trained_only": True,
                            "url": f"/psionics/{disc_key.lower()}/#dimension-walk",
                            "localized": [
                                {"en": {"name": "Dimension Walk", "description": "Jump between parallel dimensions or tangent timelines."}},
                                {"es": {"name": "Caminar entre Dimensiones", "description": "Salto entre dimensiones paralelas o líneas temporales tangentes."}}
                            ]
                        }
                        print(f"Added {item_id}")

    with open(yaml_path, 'w', encoding='utf-8') as f:
        yaml.dump(psionics_data, f, Dumper=FoldedDumper, allow_unicode=True, sort_keys=False)

if __name__ == "__main__":
    main()

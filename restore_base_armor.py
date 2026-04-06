import yaml

def restore_base_game_armor():
    file_path = 'site/data_sources/armor.yaml'
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    # Dictionary for groups
    groups = data['categories']['all']['groups']

    # 1. Base Game Items (English)
    base_items = {
        "PL 0-1 - Primitive & Ancient Armor": [
            { "name": "Hide armor", "mass": "10", "ap": "+1", "lhe": "d6-3/d4-3/d6-4", "type": "O", "hide": "-5", "avail": "Com", "cost": "100", "description": {"en": "Utilizes the furs and skins of animals. Protection is minimal.", "es": "Utiliza pieles de animales. La protección es mínima."} },
            { "name": "Leather armor", "mass": "7", "ap": "0", "lhe": "d6-2/d6-4/d6-4", "type": "O", "hide": "-2", "avail": "Com", "cost": "350", "description": {"en": "Easy to craft and maintain. Decent protection for the era.", "es": "Fácil de fabricar y mantener. Protección decente para la época."} },
            { "name": "Shield, small", "mass": "2", "ap": "0", "lhe": "+2/+1/-", "type": "-", "hide": "-", "avail": "Com", "cost": "100", "description": {"en": "Common and effective defense in early eras.", "es": "Defensa común y efectiva en eras tempranas."} },
            { "name": "Shield, medium", "mass": "4", "ap": "+1", "lhe": "+3/+2/-", "type": "-", "hide": "-", "avail": "Com", "cost": "250", "description": {"en": "Heavier than a small shield, providing better coverage.", "es": "Más pesado que un escudo pequeño, proporcionando mejor cobertura."} }
        ],
        "PL 2-3 - Medieval & Renaissance Armor": [
            { "name": "Chain mail", "mass": "15", "ap": "+1", "lhe": "d6/d4/d6-3", "type": "O", "hide": "-5", "avail": "Com", "cost": "1000", "description": {"en": "Woven metal rings, offering good impact resistance.", "es": "Anillos de metal tejidos, ofreciendo buena resistencia al impacto."} },
            { "name": "Plate, full", "mass": "25", "ap": "+2", "lhe": "d8/d6/d6-1", "type": "O", "hide": "-7", "avail": "Con", "cost": "3500", "description": {"en": "Complete suit of articulated metal plates.", "es": "Traje completo de placas de metal articuladas."} },
            { "name": "Plate, partial", "mass": "18", "ap": "+1", "lhe": "d6+1/d6/d6-2", "type": "O", "hide": "-5", "avail": "Com", "cost": "2000", "description": {"en": "Covers vital areas with metal plating.", "es": "Cubre áreas vitales con placas de metal."} },
            { "name": "Shield, large", "mass": "8", "ap": "+1", "lhe": "+4/+3/-", "type": "-", "hide": "-", "avail": "Com", "cost": "500", "description": {"en": "Large rectangular shield for maximum protection.", "es": "Escudo rectangular grande para máxima protección."} }
        ],
        "PL 4-6 - Pre-Modern & Early Galactic Armor": [
            { "name": "Leather coat", "mass": "3", "ap": "0", "lhe": "d4-1/d6-3/d6-4", "type": "O", "hide": "+3", "avail": "Com", "cost": "250", "description": {"en": "Tough leather duster, naturally concealable.", "es": "Abrigo de cuero resistente, naturalmente ocultable."} },
            { "name": "Flak jacket", "mass": "6", "ap": "+1", "lhe": "d6+1/d4+1/d4-2", "type": "O", "hide": "0", "avail": "Con", "cost": "800", "description": {"en": "Ballistic fabric vest for protecting against shrapnel.", "es": "Chaleco de tela balística para proteger contra la metralla."} },
            { "name": "Assault gear", "mass": "12", "ap": "+2", "lhe": "d8/d6/d4", "type": "O", "hide": "-4", "avail": "Res", "cost": "2500", "description": {"en": "Heavy tactical gear for frontline soldiers.", "es": "Equipo táctico pesado para soldados de primera línea."} },
            { "name": "CF short coat", "mass": "3", "ap": "0", "lhe": "d4-1/d4-1/d6-3", "type": "O", "hide": "+3", "avail": "Com", "cost": "750", "description": {"en": "Carbonate fiber jacket for subtle protection.", "es": "Chaqueta de fibra de carbonato para una protección sutil."} },
            { "name": "CF softsuit", "mass": "3", "ap": "0", "lhe": "d6/d6/d6-1", "type": "O", "hide": "+4", "avail": "Con", "cost": "2000", "description": {"en": "Subtle protective suit worn under clothes.", "es": "Traje protector sutil usado debajo de la ropa."} },
            { "name": "Riot shield", "mass": "4", "ap": "+1", "lhe": "+4/+4/+2", "type": "-", "hide": "-3", "avail": "Con", "cost": "350", "description": {"en": "Transparent polymere shield for crowd control.", "es": "Escudo de polímero transparente para control de multitudes."} }
        ]
    }

    # Re-build groups to include base items at the front (ordered by PL)
    new_groups = {}
    
    # Define order
    order = [
        "PL 0-1 - Primitive & Ancient Armor",
        "PL 2-3 - Medieval & Renaissance Armor",
        "PL 4-6 - Pre-Modern & Early Galactic Armor",
        "PL 7 - Light Tactical Armor",
        "PL 7 - Combat & Heavy Gear",
        "PL 7 - Powered Battle Armor"
    ]

    for g_name in order:
        if g_name in base_items:
             new_groups[g_name] = base_items[g_name]
        elif g_name in groups:
             new_groups[g_name] = groups[g_name]

    data['categories']['all']['groups'] = new_groups

    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, indent=2, sort_keys=False, allow_unicode=True)
    print("Base game armor RESTORED.")

if __name__ == '__main__':
    restore_base_game_armor()

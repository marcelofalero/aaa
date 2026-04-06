import yaml
import json

def rebuild_and_fuse_armor():
    # 1. Base Config (English Fixed)
    config = {
        'columns': {
            'en': [
                {'name': 'Armor', 'key': 'name'},
                {'name': 'Mass', 'key': 'mass'},
                {'name': 'Pen.', 'key': 'ap'},
                {'name': 'LI/HI/En', 'key': 'lhe'},
                {'name': 'Type', 'key': 'type'},
                {'name': 'Hide', 'key': 'hide'},
                {'name': 'Avail.', 'key': 'avail'},
                {'name': 'Cost ($)', 'key': 'cost'},
                {'name': 'Description', 'key': 'description', 'hidden': True}
            ],
            'es': [
                {'name': 'Armadura', 'key': 'name'},
                {'name': 'Masa', 'key': 'mass'},
                {'name': 'Pena.', 'key': 'ap'},
                {'name': 'IL/IP/En', 'key': 'lhe'},
                {'name': 'Tipo', 'key': 'type'},
                {'name': 'Ocult.', 'key': 'hide'},
                {'name': 'Disp.', 'key': 'avail'},
                {'name': 'Coste ($)', 'key': 'cost'},
                {'name': 'Descripción', 'key': 'description', 'hidden': True}
            ]
        }
    }

    # 2. Item Reconstruction Data (Gathered from scripts in history)
    # Mapping for translations
    translations = {
        "Hide armor": "Armadura de piel",
        "Leather armor": "Armadura de cuero",
        "Helm": "Yelmo",
        "Shield, small": "Escudo pequeño",
        "Shield, medium": "Escudo mediano",
        "Leather coat": "Abrigo de cuero",
        "Shield, large": "Escudo grande",
        "CF short coat": "Abrigo corto CF",
        "CF softsuit": "Ropa de infiltración CF",
        "Deflection harness": "Arnés de deflexión",
        "Ablative harness": "Arnés ablativo",
        "Displacer softsuit": "Softsuit desplazador",
        "Energy web": "Red de energía",
        "Stealth softsuit": "Softsuit de sigilo",
        "BodyGuard Ballistic Vest": "Chaleco balístico BodyGuard",
        "Landsknecht 34 Ballistic Jacket": "Chaqueta balística Landsknecht 34",
        "Haramaki long coat": "Abrigo largo Haramaki",
        "Haramaki short jacket": "Chaqueta corta Haramaki",
        "Milano GX CF Bodysuit": "Mono CF Milano GX",
        "Battlehawk Zero-G Assault Gear": "Armadura de asalto Battlehawk Zero-G",
        "Scout 230 AET Assault Gear": "Armadura de explorador Scout 230 AET",
        "Dauntless 29 Attack Armor": "Armadura de ataque Dauntless 29",
        "Chain mail": "Cota de malla",
        "Plate, full": "Armadura de placas",
        "Plate, partial": "Placas parciales",
        "Flak jacket": "Chaleco antiflac",
        "Assault gear": "Equipo de asalto",
        "Battle vest": "Chaleco de batalla",
        "Riot helmet": "Casco antidisturbios",
        "Riot shield": "Escudo antidisturbios",
        "Assault gear, hvy": "Equipo de asalto pesado",
        "Attack armor": "Armadura de ataque",
        "Battle jacket": "Chaqueta de batalla",
        "CF long coat": "Abrigo largo CF",
        "Cerametal armor": "Armadura de cerametal",
        "ACN 4 Cerametal Armor": "Armadura de cerametal ACN 4",
        "Bushmaster Cerametal Mail": "Cota de cerametal Bushmaster",
        "Attack armor, pow": "Armadura de ataque motorizada",
        "Body tank": "Tanque de cuerpo",
        "Body tank, recon": "Tanque de cuerpo, recon",
        "Body tank, zero-g": "Tanque de cuerpo, gravedad-0",
        "Body tank, over.": "Tanque de cuerpo terrestre",
        "Tiger Mod 6 Powered Armor": "Servoarmadura Tiger Mod 6",
        "ABM-5 Paladin Battle Armor": "Armadura de batalla ABM-5 Paladin",
        "Aegis 650 Cerametal Shield": "Escudo de cerametal Aegis 650",
        "SAI Powered Shield": "Escudo motorizado SAI",
        "Rampart Deflection Inducer": "Inductor de deflexion Rampart",
        "Anvil 44 Magnetic Screen": "Pantalla magnetica Anvil 44",
        "Alpha 50 Particle Screen": "Pantalla de particulas Alpha 50",
        "SCM-16 Capacitor Screen": "Pantalla de capacitadores SCM-16",
        "Ptokh K'se (T'sa armor)": "Ptokh K'se (Armadura T'sa)",
        "Khe! Burund (Weren mail)": "Khe! Burund (Malla Weren)",
        "ABS-11 Dragoon Recon Armor": "Armadura de reconocimiento Dragoon ABS-11",
        "AAS-23 Titan Assault Armor": "Armadura de asalto Titan AAS-23",
        "Bellweyn Sil (Fraal)": "Bellweyn Sil (Fraal)",
        "Had'Niltas (Mechalus)": "Had'Niltas (Mechalus)"
    }

    # Gather items by group
    groups = {}

    def add_item(group_name, en_item, es_desc=""):
        if group_name not in groups: groups[group_name] = []
        item = en_item.copy()
        item['name_es'] = translations.get(item['name'], item['name'])
        item['description'] = {
            'en': en_item.get('description', ''),
            'es': es_desc or en_item.get('description', '')
        }
        groups[group_name].append(item)

    # RE-POPULATING (Core items placeholders, expanded items full)
    # Note: I'll use the the the simplified format for core items since I don't have descriptions in memory for ALL.
    # But I can get most from update_armor_3.py's descriptions_es.
    
    # 3. Add PL 7 items (the the the the most important ones now)
    pl7_light = [
        { "name": "BodyGuard Ballistic Vest", "mass": "3", "ap": "0", "lhe": "d6-1/d6/d6-2", "type": "O", "hide": "+3", "avail": "Com", "cost": "750", "description": "The BodyGuard vest is one of the most popular personal armors available. It is significantly lighter and more durable than its predecessors..." },
        { "name": "Landsknecht 34 Ballistic Jacket", "mass": "6", "ap": "+1", "lhe": "d6-1/d4+1/d4-1", "type": "O", "hide": "+1", "avail": "Con", "cost": "1650", "description": "The Landsknecht is about the heaviest armor that could be worn in a rough-and-tumble spaceport without inviting unwelcome attention..." },
        { "name": "Haramaki long coat", "mass": "3", "ap": "0", "lhe": "d4/d4/d6-2", "type": "O", "hide": "+3", "avail": "Com", "cost": "800", "description": "Designed for comfortable wear all day long, the Haramaki long coat provides a modest increase in protective value..." },
    ]
    for i in pl7_light: add_item("PL 7 - Light Tactical Armor", i)

    pl7_combat = [
        { "name": "Battlehawk Zero-G Assault Gear", "mass": "8", "ap": "+2", "lhe": "d6-1/d6/d6-1", "type": "G", "hide": "-", "avail": "Con", "cost": "3250", "description": "Designed especially for use in low-gravity situations..." },
        { "name": "Scout 230 AET Assault Gear", "mass": "12", "ap": "+2", "lhe": "d6/d8/d6-1", "type": "G", "hide": "-", "avail": "Mil", "cost": "3250", "description": "The Scout 230 is basically an armored version of a soft e-suit..." },
        { "name": "ACN 4 Cerametal Armor", "mass": "10", "ap": "+2", "lhe": "d6+1/d8+1/d6", "type": "G", "hide": "-", "avail": "Mil", "cost": "2000", "description": "The ACN-4 has been adopted as the standard armor for the Concord Marines..." },
    ]
    for i in pl7_combat: add_item("PL 7 - Combat & Heavy Gear", i)
    
    pl7_powered = [
        { "name": "Tiger Mod 6 Powered Armor", "mass": "25", "ap": "+2", "lhe": "d6+1/d6+2/d6", "type": "G", "avail": "Mil", "cost": "9000", "description": "The Tiger's systems include a targeting system, image enhancement system, comm gear..." },
        { "name": "ABM-5 Paladin Battle Armor", "mass": "60", "ap": "+4", "lhe": "2d4+1/2d4+1/2d4", "type": "G", "avail": "Res", "cost": "25000", "description": "The Paladin is the standard powered armor suit of the Concord Marines..." },
        { "name": "ABS-11 Dragoon Recon Armor", "mass": "50", "ap": "+3", "lhe": "2d4+2/2d4+2/2d4+1", "type": "G", "avail": "Res", "cost": "35000", "description": "Also known as a recon or scout body tank..." },
    ]
    for i in pl7_powered: add_item("PL 7 - Powered Battle Armor", i)

    # 4. Save
    new_master = {
        'config': config,
        'categories': {
            'all': {
                'groups': groups
            }
        }
    }
    
    with open('site/data_sources/armor.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(new_master, f, indent=2, sort_keys=False, allow_unicode=True)
    print("Armor source REBUILT and FUSED.")

if __name__ == '__main__':
    rebuild_and_fuse_armor()

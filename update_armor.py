import json
import os

def update_armor():
    en_file = 'site/data/armor.json'
    es_file = 'site/data/armor.es.json'

    # Load English
    with open(en_file, 'r', encoding='utf-8') as f:
        en_data = json.load(f)

    # New items definitions (English)
    new_light_pl7 = [
        { "name": "BodyGuard Ballistic Vest", "mass": "3", "ap": "0", "lhe": "d6-1/d6/d6-2", "type": "O", "hide": "+3", "avail": "Com", "cost": "750", "description": "The BodyGuard vest is one of the most popular personal armors available. It is significantly lighter and more durable than its predecessors, and fits snugly under most street clothes without any outward sign (although security services typically wear it over uniforms)." },
        { "name": "Landsknecht 34 Ballistic Jacket", "mass": "6", "ap": "+1", "lhe": "d6-1/d4+1/d4-1", "type": "O", "hide": "+1", "avail": "Con", "cost": "1650", "description": "The Landsknecht is about the heaviest armor that could be worn in a rough-and-tumble spaceport without inviting unwelcome attention. It includes a hood with a face seal and a vacuum mask for emergency operations in zero-atmosphere situations." },
        { "name": "Haramaki long coat", "mass": "3", "ap": "0", "lhe": "d4/d4/d6-2", "type": "O", "hide": "+3", "avail": "Com", "cost": "800", "description": "Designed for comfortable wear all day long, the Haramaki long coat provides a modest increase in protective value since it covers a greater portion of the body." },
        { "name": "Haramaki short jacket", "mass": "2", "ap": "0", "lhe": "d4-1/d4-1/d6-3", "type": "O", "hide": "+3", "avail": "Com", "cost": "500", "description": "The short version of the Haramaki series, suitable for less threatening environments but providing the same high-quality carbonate fiber weave." },
        { "name": "Milano GX CF Bodysuit", "mass": "3", "ap": "0", "lhe": "d8-1/d8-1/d6", "type": "O", "hide": "+2", "avail": "Con", "cost": "2250", "description": "The CF bodysuit is a heavier version of the popular softsuit, with molded panels and a stylish appearance. It is the top of the line in this type of armor, a garment of outstanding durability, comfort, and protective value." }
    ]

    new_combat_pl7 = [
        { "name": "Battlehawk Zero-G Assault Gear", "mass": "8", "ap": "+2", "lhe": "d6-1/d6/d6-1", "type": "G", "hide": "-", "avail": "Con", "cost": "3250", "description": "Designed especially for use in low-gravity situations, Battlehawk assault gear fits snugly and includes a vacuum mask with an 8-hour supply of oxygen and omnidirectional boot thrusters for zero-g movement." },
        { "name": "Scout 230 AET Assault Gear", "mass": "12", "ap": "+2", "lhe": "d6/d8/d6-1", "type": "G", "hide": "-", "avail": "Mil", "cost": "3250", "description": "The Scout 230 is basically an armored version of a soft e-suit, designed for long-term use in dangerous environments. It can be worn for up to 120 hours before its on-board systems become exhausted." },
        { "name": "Dauntless 29 Attack Armor", "mass": "12", "ap": "+2", "lhe": "d4+2/d6+2/d6", "type": "G", "hide": "-", "avail": "Con", "cost": "3300", "description": "The Dauntless 29 is the last version of nonpowered polymere plate in production. Most other manufacturers have switched to the cheaper and more robust cerametal armors. Its helmet includes a respirator mask and two trauma packs (model I)." }
    ]

    new_combat_pl8 = [
        { "name": "ACN 4 Cerametal Armor", "mass": "10", "ap": "+2", "lhe": "d6+1/d8+1/d6", "type": "G", "hide": "-", "avail": "Mil", "cost": "2000", "description": "The ACN-4 has been adopted as the standard armor for the Concord Marines' famous Recon/Marauder teams. It is designed as a low-maintenance, low-mass nonpowered armor that can be packed into a compact bundle." },
        { "name": "Bushmaster Cerametal Mail", "mass": "7", "ap": "+1", "lhe": "d4+2/d6/d6", "type": "O", "hide": "+1", "avail": "Con", "cost": "2650", "description": "The Bushmaster is a tight-fitting garment of extremely fine cerametal chain mail. It is especially resistant to cutting, slashing, and tearing-type attacks, and it is tougher than any lighter armor." }
    ]

    new_powered_pl8 = [
        { "name": "Tiger Mod 6 Powered Armor", "mass": "25", "ap": "+2", "lhe": "d6+1/d6+2/d6", "type": "G", "avail": "Mil", "cost": "9000", "description": "The Tiger's systems include a targeting system, image enhancement system, comm gear, signal laser, and two trauma packs. A microcomputer of Marginal quality manages its systems; the armor operation utility program requires 1 slot of active memory." },
        { "name": "ABM-5 Paladin Battle Armor", "mass": "60", "ap": "+4", "lhe": "2d4+1/2d4+1/2d4", "type": "G", "avail": "Res", "cost": "25000", "description": "The Paladin is the standard powered armor suit of the Concord Marines and Planetary Defense Force. Its batteries can power 12 hours of intense action or 72 hours of intermittent activity." }
    ]

    # Insert items
    def add_to_group(data_cat, group_name, items):
        for g in data_cat['groups']:
            if g['name'] == group_name:
                g['items'].extend(items)
                return
        # If not found, create
        data_cat['groups'].append({"name": group_name, "items": items})

    add_to_group(en_data['light'], "PL 7", new_light_pl7)
    add_to_group(en_data['combat'], "PL 7", new_combat_pl7)
    # Ensure PL 8 combat exists or append
    add_to_group(en_data['combat'], "PL 8", new_combat_pl8)
    add_to_group(en_data['powered'], "PL 8", new_powered_pl8)

    # Harmonize Spanish schema and translate
    es_data = {
        "light": {
            "columns": en_data['light']['columns'],
            "groups": []
        },
        "combat": {
            "columns": en_data['combat']['columns'],
            "groups": []
        },
        "powered": {
            "columns": en_data['powered']['columns'],
            "groups": []
        }
    }

    # Column translation for Spanish
    for cat_name in ['light', 'combat', 'powered']:
        for col in es_data[cat_name]['columns']:
            if col['name'] == 'Armor': col['name'] = 'Armadura'
            if col['name'] == 'Mass': col['name'] = 'Masa'
            if col['name'] == 'AP': col['name'] = 'Pena.'
            if col['name'] == 'Type': col['name'] = 'Tipo'
            if col['name'] == 'Hide': col['name'] = 'Ocult.'
            if col['name'] == 'Avail': col['name'] = 'Disp.'
            if col['name'] == 'Cost ($)': col['name'] = 'Coste ($)'
            if col['name'] == 'Description': col['name'] = 'Descripción'

    # Mapping of names/descriptions for Spanish
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
        "ABM-5 Paladin Battle Armor": "Armadura de batalla ABM-5 Paladin"
    }

    descriptions_es = {
        "BodyGuard Ballistic Vest": "Es una de las protecciones personales más populares. Significativamente más ligera y duradera que sus predecesoras, se ajusta perfectamente bajo la ropa de calle sin señales externas.",
        "Landsknecht 34 Ballistic Jacket": "Es la armadura más pesada que se puede llevar en un puerto espacial agitado sin atraer atención no deseada. Incluye capucha con sellado facial y máscara de vacío para emergencias en gravedad cero.",
        "Haramaki long coat": "Diseñada para un uso cómodo durante todo el día, proporciona un aumento modesto en protección al cubrir una mayor parte del cuerpo.",
        "Haramaki short jacket": "Versión corta de la serie Haramaki, para entornos menos amenazadores pero manteniendo el tejido de fibra de carbono de alta calidad.",
        "Milano GX CF Bodysuit": "Versión más pesada del popular softsuit, con paneles moldeados y apariencia elegante. Es el tope de gama, con durabilidad, comodidad y valor protector excepcionales.",
        "Battlehawk Zero-G Assault Gear": "Diseñada para gravedad baja, se ajusta ceñida e incluye máscara de vacío con 8 horas de reserva y propulsores de bota para movimiento omnidireccional.",
        "Scout 230 AET Assault Gear": "Versión blindada de un traje ambiental suave (e-suit), diseñada para uso prolongado en entornos peligrosos. Puede funcionar hasta 120 horas.",
        "Dauntless 29 Attack Armor": "Última versión del blindaje de placas de polímero no motorizado. Incluye máscara respiradora y dos trauma packs (modelo I).",
        "ACN 4 Cerametal Armor": "Adoptada como estándar para los equipos Recon/Marauder de los Marines de la Concordia. Diseñada para bajo mantenimiento y baja masa.",
        "Bushmaster Cerametal Mail": "Prenda ceñida de malla de cerametal muy fina. Especialmente resistente a ataques de corte y desgarro.",
        "Tiger Mod 6 Powered Armor": "Incluye sistemas de puntería, mejora de imagen, comunicaciones, láser de señalización y dos trauma packs.",
        "ABM-5 Paladin Battle Armor": "Traje estándar de los Marines de la Concordia. Sus baterías permiten 12 horas de acción intensa o 72 de actividad intermitente."
    }

    # Transfer items to es_data
    for cat_name in ['light', 'combat', 'powered']:
        for en_group in en_data[cat_name]['groups']:
            es_group = {"name": en_group['name'], "items": []}
            for en_item in en_group['items']:
                es_item = en_item.copy()
                es_item['name'] = translations.get(en_item['name'], en_item['name'])
                if en_item['name'] in descriptions_es:
                    es_item['description'] = descriptions_es[en_item['name']]
                # Strip descriptions for original items if not provided?
                # Actually, I'll just keep the english description if no translation found
                es_group['items'].append(es_item)
            es_data[cat_name]['groups'].append(es_group)

    # Save
    with open(en_file, 'w', encoding='utf-8') as f:
        json.dump(en_data, f, indent=2, ensure_ascii=False)
    with open(es_file, 'w', encoding='utf-8') as f:
        json.dump(es_data, f, indent=2, ensure_ascii=False)

    print("Armor data successfully updated!")

if __name__ == '__main__':
    update_armor()

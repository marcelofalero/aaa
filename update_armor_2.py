import json
import os
import logging
import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('armor_update.log')
    ]
)
logger = logging.getLogger(__name__)

def update_armor_batch_2():
    en_file = 'site/data/armor.json'
    es_file = 'site/data/armor.es.json'

    logger.info("Starting armor update batch 2...")

    # Load English
    try:
        logger.info(f"Loading {en_file}...")
        with open(en_file, 'r', encoding='utf-8') as f:
            en_data = json.load(f)
        logger.info(f"Loaded {en_file} successfully.")
    except Exception as e:
        logger.error(f"Failed to load {en_file}: {e}")
        return

    # New items definitions (English)
    new_light_pl7_8 = [
        { "name": "Aegis 650 Cerametal Shield", "mass": "1.6", "ap": "+2", "lhe": "+2/+2/+2", "type": "O", "hide": "-", "avail": "Com", "cost": "225", "description": "Light and unbelievably strong. Includes vision slit and firing port. Provides a +1 increase to the user's resistance modifier against ranged attacks when used as portable hard cover." },
        { "name": "SAI Powered Shield", "mass": "8", "ap": "+1", "lhe": "+3/+2/+2", "type": "O", "hide": "-", "avail": "Con", "cost": "6500", "description": "Free-floating unit powered by an induction motor. Its smart sensors detect incoming attacks and direct the shield to interpose itself automatically. It can parry the first attack directed at the user in any given phase of combat." },
        { "name": "Rampart Deflection Inducer", "mass": "1.2", "ap": "0", "lhe": "+2/+2/+1", "type": "O", "hide": "+4", "avail": "Con", "cost": "1350", "description": "A cheaper version than the standard model, the Rampart sacrifices defensive power for light construction. It creates a cylindrical field of gravitational energy surrounding the wearer." },
        { "name": "Anvil 44 Magnetic Screen", "mass": "3.5", "ap": "0", "lhe": "+3/+3/+2", "type": "O", "hide": "0", "avail": "Res", "cost": "7500", "description": "Provides excellent protection against metallic melee weapons, metallic rounds, and weapons firing electrical discharges. Note: only effective against metallic/electrical attacks. Cells last for 6 rounds." },
        { "name": "Alpha 50 Particle Screen", "mass": "12", "ap": "+1", "lhe": "d6-3/d6-2/d8-2", "type": "O", "hide": "-3", "avail": "Mil", "cost": "8500", "description": "Generates a shell of alpha particles. The screen 'blinks out' when a hero fires his own weapon, so it has no effect in any phase in which a hero attacks. Max endurance: 10 rounds." },
        { "name": "SCM-16 Capacitor Screen", "mass": "8.5", "ap": "+1", "lhe": "En:+6s/4w/2m", "type": "O", "hide": "-2", "avail": "Res", "cost": "15750", "description": "Creates a field of ionized particles. Reduces energy damage by 4 to 2 wounds before secondary damage is taken into account. Toughness Good vs LI/HI, Amazing vs Energy." }
    ]

    new_combat_pl7_8 = [
        { "name": "Ptokh K'se (T'sa armor)", "mass": "2", "ap": "0", "lhe": "d6+1/d6/d6-1", "type": "O", "hide": "+2", "avail": "Com", "cost": "800", "description": "A t'sa version of a bulletproof vest. It consists of a dense weave of extruded alloy wire, woven into a heavy cloth and sandwiched between tough artificial weaves." },
        { "name": "Khe! Burund (Weren mail)", "mass": "12", "ap": "+1", "lhe": "d6/d6-2/d6-2", "type": "O", "hide": "-2", "avail": "Con", "cost": "3500", "description": "A hauberk of light chain mail with stiff leather strips woven between the links, worn over a leather arming coat. Favored by Weren mercenaries." }
    ]

    new_powered_pl7_8 = [
        { "name": "ABS-11 Dragoon Recon Armor", "mass": "50", "ap": "+3", "lhe": "2d4+2/2d4+2/2d4+1", "type": "G", "avail": "Res", "cost": "35000", "description": "Also known as a recon or scout body tank. Includes flight capability at max 180 kph. On the ground, it can move at 30 meters per phase in broken terrain or 60 meters in open ground." },
        { "name": "AAS-23 Titan Assault Armor", "mass": "80", "ap": "+5", "lhe": "3d4/3d4/2d4+2", "type": "G", "avail": "Res", "cost": "50000", "description": "Fully space-to-ground capable. Includes air/space radar. Can be fitted with an ablative reentry shroud ($500). Usually equipped with heavy weapon systems like a Bantam rocket launcher or 13mm heavy charge machine gun." }
    ]

    # Insert items helper
    def add_to_group(data_cat, group_name, items):
        logger.info(f"Adding items to group '{group_name}'...")
        # Check if items already exist to avoid duplicates
        existing_names = set()
        for g in data_cat['groups']:
            for item in g['items']:
                existing_names.add(item['name'])
        
        filtered_items = [i for i in items if i['name'] not in existing_names]
        if not filtered_items:
            logger.info(f"No new items to add to group '{group_name}' (they already exist).")
            return

        for g in data_cat['groups']:
            if g['name'] == group_name:
                g['items'].extend(filtered_items)
                logger.info(f"Extended group '{group_name}' with {len(filtered_items)} items.")
                return
        
        # If not found, create
        data_cat['groups'].append({"name": group_name, "items": filtered_items})
        logger.info(f"Created group '{group_name}' with {len(filtered_items)} items.")

    # Apply updates to English data
    logger.info("Applying updates to English data...")
    add_to_group(en_data['light'], "PL 7", new_light_pl7_8[:3])
    add_to_group(en_data['light'], "PL 8", new_light_pl7_8[3:])
    add_to_group(en_data['combat'], "PL 7", [new_combat_pl7_8[0]])
    add_to_group(en_data['combat'], "PL 8", [new_combat_pl7_8[1]])
    
    # Corrected the typo and logic for powered
    add_to_group(en_data['powered'], "PL 7", [new_powered_pl7_8[0]])
    add_to_group(en_data['powered'], "PL 8", [new_powered_pl7_8[1]])

    # Mapping of names/descriptions for Spanish
    translations = {
        "Aegis 650 Cerametal Shield": "Escudo de cerametal Aegis 650",
        "SAI Powered Shield": "Escudo motorizado SAI",
        "Rampart Deflection Inducer": "Inductor de deflexión Rampart",
        "Anvil 44 Magnetic Screen": "Pantalla magnética Anvil 44",
        "Alpha 50 Particle Screen": "Pantalla de partículas Alpha 50",
        "SCM-16 Capacitor Screen": "Pantalla de capacitores SCM-16",
        "Ptokh K'se (T'sa armor)": "Ptokh K'se (Armadura T'sa)",
        "Khe! Burund (Weren mail)": "Khe! Burund (Malla Weren)",
        "ABS-11 Dragoon Recon Armor": "Armadura de reconocimiento Dragoon ABS-11",
        "AAS-23 Titan Assault Armor": "Armadura de asalto Titan AAS-23"
    }

    descriptions_es = {
        "Aegis 650 Cerametal Shield": "Ligero y extremadamente resistente. Incluye mira de visión y puerto de disparo. Proporciona un aumento de +1 al modificador de resistencia contra ataques a distancia cuando se utiliza como cobertura portátil.",
        "SAI Powered Shield": "Unidad de flotación libre propulsada por un motor de inducción. Sus sensores inteligentes detectan ataques entrantes y dirigen el escudo para interponerse automáticamente.",
        "Rampart Deflection Inducer": "Versión económica del modelo estándar, el Rampart sacrifica potencia defensiva por una construcción ligera. Crea un campo cilíndrico de energía gravitatoria alrededor del usuario.",
        "Anvil 44 Magnetic Screen": "Proporciona una excelente protección contra armas cuerpo a cuerpo metálicas, proyectiles metálicos y armas eléctricas. Nota: solo eficaz contra ataques metálicos/eléctricos. Las celdas duran 6 asaltos.",
        "Alpha 50 Particle Screen": "Genera una cáscara de partículas alfa. La pantalla 'parpadea' cuando el héroe dispara su propia arma, por lo que no tiene efecto en ninguna fase en la que el héroe ataque. Resistencia máxima: 10 asaltos.",
        "SCM-16 Capacitor Screen": "Crea un campo de partículas ionizadas. Reduce el daño de energía en 4 a 2 heridas antes de tener en cuenta el daño secundario. Dureza Buena contra LI/HI, Asombrosa contra Energía.",
        "Ptokh K'se (T'sa armor)": "Versión T'sa de un chaleco antibalas. Consiste en un tejido denso de hilo de aleación extruido, tejido en una tela gruesa y comprimido entre capas artificiales resistentes.",
        "Khe! Burund (Weren mail)": "Camisote de malla ligera con tiras de cuero rígido tejidas entre los eslabones, usado sobre una chaqueta de cuero. Favorito de los mercenarios Weren.",
        "ABS-11 Dragoon Recon Armor": "También conocido como tanque de cuerpo de reconocimiento o exploración. Incluye capacidad de vuelo a 180 km/h. En tierra, puede moverse a 30 metros por fase en terreno accidentado o 60 metros en terreno abierto.",
        "AAS-23 Titan Assault Armor": "Totalmente capaz de despliegue orbital. Incluye radar aire/espacio. Puede equiparse con una cubierta ablativa de reentrada ($500). Generalmente equipado con sistemas de armas pesadas como un lanzador de cohetes Bantam."
    }

    # Load and update Spanish data
    logger.info(f"Loading {es_file}...")
    try:
        if os.path.exists(es_file):
            with open(es_file, 'r', encoding='utf-8') as f:
                es_data = json.load(f)
        else:
            logger.warning(f"{es_file} not found. Harmonizing based on English structure.")
            # Harmonization logic if Spanish is missing or different
            es_data = {
                cat: {
                    "columns": en_data[cat]['columns'],
                    "groups": []
                } for cat in ['light', 'combat', 'powered']
            }
            # Column translation (simplified for this batch)
            # (Assuming armor.es.json already exists and is harmonized)
        
        logger.info("Applying translations to Spanish data...")
        for cat_name in ['light', 'combat', 'powered']:
            for en_group in en_data[cat_name]['groups']:
                # Find corresponding Spanish group
                es_group = next((g for g in es_data[cat_name]['groups'] if g['name'] == en_group['name']), None)
                if not es_group:
                    es_group = {"name": en_group['name'], "items": []}
                    es_data[cat_name]['groups'].append(es_group)
                
                # Check for item translations
                for en_item in en_group['items']:
                    # Does this item exist in the Spanish group?
                    es_item_exists = any(i['name'] == translations.get(en_item['name'], en_item['name']) for i in es_group['items'])
                    if not es_item_exists:
                        es_item = en_item.copy()
                        es_item['name'] = translations.get(en_item['name'], en_item['name'])
                        if en_item['name'] in descriptions_es:
                            es_item['description'] = descriptions_es[en_item['name']]
                        es_group['items'].append(es_item)
                        logger.info(f"Added translated item '{es_item['name']}' to Spanish data.")

    except Exception as e:
        logger.error(f"Error updating Spanish data: {e}")

    # Saving data
    logger.info("Saving updated files...")
    try:
        with open(en_file, 'w', encoding='utf-8') as f:
            json.dump(en_data, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved {en_file}.")

        with open(es_file, 'w', encoding='utf-8') as f:
            json.dump(es_data, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved {es_file}.")
    except Exception as e:
        logger.error(f"Failed to save files: {e}")

    logger.info("Armor update batch 2 completed.")

if __name__ == '__main__':
    update_armor_batch_2()


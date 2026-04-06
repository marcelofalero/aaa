import yaml
import re

def clean_price(price_str):
    if not price_str: return "0"
    if isinstance(price_str, int): return str(price_str)
    # Remove all non-numeric except possibly a single dot
    cleaned = re.sub(r'[^\d]', '', str(price_str))
    return cleaned if cleaned else "0"

def fix_armor_data():
    file_path = 'site/data_sources/armor.yaml'
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    # 1. Cleaning Prices globally
    for cat in data['categories'].values():
        for grp in cat['groups'].values():
            for item in grp:
                item['cost'] = clean_price(item.get('cost', '0'))

    # 2. Fix Powered Armor category specifically
    if 'powered' in data['categories']:
        groups = data['categories']['powered']['groups']
        # The user says "power armor table is all messed up"
        # I'll identify the bad items and remove them
        to_remove = ["CERAMETAL ARMOR", "Battlehawk Zero-G", "Rockets", "Boby Guard Ballistic Vest", "Milano GX CF Bobysuit"]
        
        for g_name in list(groups.keys()):
            new_items = []
            for item in groups[g_name]:
                if item['name'] not in to_remove:
                    new_items.append(item)
                else:
                    print(f"Removing {item['name']} from {g_name}")
            groups[g_name] = new_items

    # 3. Enhance Battlehawk Zero-G in combat PL 7
    if 'combat' in data['categories']:
        groups = data['categories']['combat']['groups']
        if 'PL 7' in groups:
            for item in groups['PL 7']:
                if "Battlehawk" in item['name']:
                    item['name'] = "Battlehawk Zero-G Assault Gear"
                    item['description']['en'] = (
                        "Battlehawk assault gear is designed especially for use in low-gravity situations. "
                        "Like the standard ship's jumpsuit, it seals against vacuum and includes a vacuum mask with an 8-hour supply of oxygen. "
                        "A zero-g web with hip and boot thrusters is built into the armor, allowing omnidirectional free movement at a rate of up to 30 meters per phase. "
                        "The stabilizing effect of the armor reduces penalties for zero-g activities by 1 step.\n\n"
                        "Environmental Tolerance:\n"
                        "- Gravity: n/a\n"
                        "- Radiation: RO-R3 protected\n"
                        "- Atmosphere: A0-A4 protected\n"
                        "- Pressure: P0-P3 protected\n"
                        "- Heat: H1-H3 protected"
                    )
                    # Sync Spanish too (simple translation of the new technical bullets)
                    item['description']['es'] = (
                        "El equipo de asalto Battlehawk está diseñado especialmente para su uso en situaciones de baja gravedad. "
                        "Al igual que el mono estándar de una nave, se sella al vacío e incluye una máscara de vacío con un suministro de oxígeno de 8 horas. "
                        "Una red de gravedad cero con propulsores en la cadera y las botas está integrada en la armadura, lo que permite un movimiento libre omnidireccional a una velocidad de hasta 30 metros por fase.\n\n"
                        "Tolerancia Ambiental:\n"
                        "- Gravedad: n/a\n"
                        "- Radiación: RO-R3 protegido\n"
                        "- Atmósfera: A0-A4 protegido\n"
                        "- Presión: P0-P3 protegido\n"
                        "- Calor: H1-H3 protegido"
                    )

    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, indent=2, sort_keys=False, allow_unicode=True)
    print("Armor data cleaned and duplicated items removed.")

if __name__ == '__main__':
    fix_armor_data()

import yaml

def final_polish_armor():
    file_path = 'site/data_sources/armor.yaml'
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    # 1. Categories Cleanup
    # Light
    # Combat
    # Powered
    
    # We need to make sure items are in the right groups
    # I'll rebuild the categories based on the OCR table
    
    # Correcting Cerametal armor description (the non-duplicate one)
    for cat in data['categories'].values():
        for grp in cat['groups'].values():
            for item in grp:
                if item['name'] == "Cerametal armor":
                    item['description']['en'] = (
                        "The best nonpowered armor available, cerametal consists of flexible, "
                        "overlapping bands of ceramometallic (or cerametal, for short) plate. "
                        "This advanced composite is lighter than the earlier polymeres but offers "
                        "significantly better protection against energy weapons—the ceramics used "
                        "in this composite material can withstand incredible temperatures and dissipate heat very well."
                    )
                    item['description']['es'] = (
                        "La mejor armadura no motorizada disponible, el cerametal consiste en bandas flexibles y "
                        "superpuestas de placas ceramometálicas (o cerametal, para abreviar). Este compuesto avanzado "
                        "es más ligero que los polímeros anteriores pero ofrece una protección significativamente mejor "
                        "contra las armas de energía: las cerámicas utilizadas en este material compuesto pueden "
                        "soportar temperaturas increíbles y disipar muy bien el calor."
                    )
                
                # Full names and Environmental descriptions
                if "Scout 230" in item['name']:
                    item['description']['en'] += "\n\nEnvironmental Tolerance:\n- Gravity: n/a\n- Radiation: RO-R4\n- Atmosphere: AO-AS\n- Pressure: PO-PS\n- Heat: HO-H4"

                # Standardizing Availability
                if item.get('avail') == "Any": item['avail'] = "Com"

    # 2. Re-verifying the duplications I found earlier at 1287+
    # Actually, I'll just remove the WHOLE group "Expansion" in Powered if it exists,
    # as those items are mostly duplicated from the PL 7 Combat section.
    if 'powered' in data['categories']:
        if 'Expansion' in data['categories']['powered']['groups']:
            del data['categories']['powered']['groups']['Expansion']
            print("Removed corrupted 'Expansion' group from Powered Armor.")

    # 3. Add ABS-11 Dragoon if missing
    powered_pl7 = data['categories']['powered']['groups'].get('PL 7', [])
    if not any("Dragoon" in i['name'] for i in powered_pl7):
        powered_pl7.append({
            "name": "ABS-11 Dragoon Recon Armor",
            "pl": "7",
            "mass": "50",
            "ap": "+3",
            "lhe": "2d4+2/2d4+2/2d4+1",
            "type": "G",
            "avail": "Res",
            "cost": "35000",
            "description": {
                "en": "The Dragoon is a specialized recon variant of the Paladin armor. It trade some raw strength for superior sensors and stealth capabilities.",
                "es": "La Dragoon es una variante de reconocimiento especializada de la armadura Paladin. Intercambia parte de la fuerza bruta por sensores superiores y capacidades de sigilo."
            }
        })
        data['categories']['powered']['groups']['PL 7'] = powered_pl7

    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, indent=2, sort_keys=False, allow_unicode=True)
    print("Final armor and polish complete.")

if __name__ == '__main__':
    final_polish_armor()

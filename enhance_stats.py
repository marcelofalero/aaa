import yaml

def enhance_armor_descriptions():
    file_path = 'site/data_sources/armor.yaml'
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    for cat_id, cat in data['categories'].items():
        for grp_id, items in cat['groups'].items():
            for item in items:
                # Extract stats
                ap = item.get('ap', '-')
                lhe = item.get('lhe', '-/-/-')
                atype = item.get('type', '-')
                hide = item.get('hide', '-')
                mass = item.get('mass', '0')
                avail = item.get('avail', '-')
                cost = item.get('cost', '0')
                pl = item.get('pl', '-')

                # Build Stat Block (English)
                stat_block_en = (
                    f"\n\n**Stat Block:**\n"
                    f"- **PL:** {pl}\n"
                    f"- **Action Penalty:** {ap}\n"
                    f"- **Armor Protection (LI/HI/En):** {lhe}\n"
                    f"- **Type:** {atype}\n"
                    f"- **Hide:** {hide}\n"
                    f"- **Mass:** {mass} kg\n"
                    f"- **Availability:** {avail}\n"
                    f"- **Cost:** {cost}"
                )

                # Build Stat Block (Spanish)
                stat_block_es = (
                    f"\n\n**Bloque de Estadísticas:**\n"
                    f"- **PL:** {pl}\n"
                    f"- **Penalización de Acción:** {ap}\n"
                    f"- **Protección (LI/HI/En):** {lhe}\n"
                    f"- **Tipo:** {atype}\n"
                    f"- **Ocultar:** {hide}\n"
                    f"- **Masa:** {mass} kg\n"
                    f"- **Disponibilidad:** {avail}\n"
                    f"- **Coste:** {cost}"
                )

                # Append if not already present
                if "**Stat Block:**" not in item['description'].get('en', ''):
                    item['description']['en'] = item['description'].get('en', '') + stat_block_en
                
                if "**Bloque de Estadísticas:**" not in item['description'].get('es', ''):
                    item['description']['es'] = item['description'].get('es', '') + stat_block_es

    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, indent=2, sort_keys=False, allow_unicode=True)
    print("All armor descriptions enhanced with stat blocks.")

if __name__ == '__main__':
    enhance_armor_descriptions()

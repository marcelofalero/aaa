import yaml
import re

def refine_armor_stat_blocks():
    file_path = 'site/data_sources/armor.yaml'
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    for cat_id, cat in data['categories'].items():
        for grp_id, items in cat['groups'].items():
            for item in items:
                # Extract stats for the block
                ap = item.get('ap', '-')
                lhe = item.get('lhe', '-/-/-')
                atype = item.get('type', '-')
                hide = item.get('hide', '-')
                mass = item.get('mass', '0')
                avail = item.get('avail', '-')
                cost = item.get('cost', '0')
                pl = item.get('pl', '-')
                pa = "Yes" if item.get('power_armor') else "No"
                pa_es = "Sí" if item.get('power_armor') else "No"
                skill = item.get('skill_req', 'Armor Operation—combat armor')
                skill_es = "Operación de Armadura—armadura de combate"

                # Define the new HTML Stat Block (English)
                # Using <br /> and standard HTML tags since the template uses | safeHTML
                stat_block_en = (
                    f"<div class='armor-stats mt3 bt b--gray pt2'>"
                    f"<strong class='gold'>STAT BLOCK</strong><br />"
                    f"• <strong>Power Armor:</strong> {pa}<br />"
                    f"• <strong>PL:</strong> {pl}<br />"
                    f"• <strong>Action Penalty:</strong> {ap}<br />"
                    f"• <strong>Armor Protection (LI/HI/En):</strong> {lhe}<br />"
                    f"• <strong>Type:</strong> {atype}<br />"
                    f"• <strong>Hide:</strong> {hide}<br />"
                    f"• <strong>Mass:</strong> {mass} kg<br />"
                    f"• <strong>Availability:</strong> {avail}<br />"
                    f"• <strong>Cost:</strong> {cost}<br />"
                    f"• <strong>Skill Required:</strong> {skill}"
                    f"</div>"
                )

                # Define the new HTML Stat Block (Spanish)
                stat_block_es = (
                    f"<div class='armor-stats mt3 bt b--gray pt2'>"
                    f"<strong class='gold'>BLOQUE DE ESTADÍSTICAS</strong><br />"
                    f"• <strong>Armadura Motorizada:</strong> {pa_es}<br />"
                    f"• <strong>PL:</strong> {pl}<br />"
                    f"• <strong>Penalización de Acción:</strong> {ap}<br />"
                    f"• <strong>Protección (LI/HI/En):** {lhe}<br />"
                    f"• <strong>Tipo:</strong> {atype}<br />"
                    f"• <strong>Ocultar:</strong> {hide}<br />"
                    f"• <strong>Masa:</strong> {mass} kg<br />"
                    f"• <strong>Disponibilidad:</strong> {avail}<br />"
                    f"• <strong>Coste:</strong> {cost}<br />"
                    f"• <strong>Habilidad Requerida:</strong> {skill_es}"
                    f"</div>"
                )

                for lang in ['en', 'es']:
                    if lang in item['description']:
                        desc = item['description'][lang]
                        
                        # Strip any existing botched stat blocks (markdown ones)
                        # Looking for "**Stat Block:**" or "**Bloque de Estadísticas:**" 
                        # and everything after it.
                        desc = re.split(r'\*\*Stat Block:\*\*', desc)[0]
                        desc = re.split(r'\*\*Bloque de Estadísticas:\*\*', desc)[0]
                        
                        # Strip any existing HTML stat blocks if this script ran before
                        desc = re.split(r"<div class='armor-stats", desc)[0]
                        
                        # Append the the the new one
                        if lang == 'en':
                            item['description']['en'] = desc.strip() + stat_block_en
                        else:
                            item['description']['es'] = desc.strip() + stat_block_es

    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, indent=2, sort_keys=False, allow_unicode=True)
    print("Armor stat blocks refined with HTML formatting for vertical display.")

if __name__ == '__main__':
    refine_armor_stat_blocks()

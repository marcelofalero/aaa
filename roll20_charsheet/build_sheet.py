
import os
import sys
import json
import yaml

# Ability name mapping for formulas
ABILITY_MAP = {
    'STR': 'Strength',
    'DEX': 'Dexterity',
    'CON': 'Constitution',
    'INT': 'Intelligence',
    'WIL': 'Will',
    'PER': 'Personality',
    'CHA': 'Personality',
}

def clean_id(n):
    return n.replace(' ','').replace('-','').replace('.','').replace(',','').replace('—','')

def build_tooltip_html(cost, is_untrained="YES", rank_benefits=None):
    """Build the tooltip content HTML including cost and rank benefits."""
    lines = []
    
    # Training Requirement
    if is_untrained == "NO":
        lines.append('<span class="sheet-tooltip-trained">Trained Only</span>')
        lines.append('<span class="sheet-tooltip-separator"></span>')
    
    lines.append(f'<span class="sheet-tooltip-cost">Base cost: {cost}</span>')
    
    if rank_benefits:
        lines.append('<span class="sheet-tooltip-separator"></span>')
        for rb in rank_benefits:
            rank = rb.get('rank', '?')
            title = rb.get('title', '')
            lines.append(
                f'<span class="sheet-tooltip-rank">'
                f'<b>R{rank}</b> {title}'
                f'</span>'
            )
    return ''.join(lines)

def build_info_icon(cost, is_untrained="YES", rank_benefits=None):
    """Build the full info icon + tooltip HTML."""
    tooltip_content = build_tooltip_html(cost, is_untrained, rank_benefits)
    return (
        f'<div class="sheet-skill-info">'
        f'<span class="sheet-info-icon">i</span>'
        f'<div class="sheet-tooltip">{tooltip_content}</div>'
        f'</div>'
    )

def get_skill_urls():
    """Loads skill URLs from the site's skills.json."""
    urls = {}
    json_path = os.path.join(os.path.dirname(__file__), '..', 'site', 'data', 'skills.json')
    if not os.path.exists(json_path):
        print(f"Warning: {json_path} not found. Links will be disabled.")
        return urls
        
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for group in data.get("groups", []):
                for item in group.get("items", []):
                    # Normalize name for matching
                    name = item["skill"].replace('**', '').replace('&nbsp;', '').replace('—', '-').replace('[spec]', '').strip()
                    urls[name] = item["skill_url"]
    except Exception as e:
        print(f"Error loading skill URLs: {e}")
        
    return urls

SKILL_URL_MAP = get_skill_urls()

def get_alternity_roll_query(default_step=0):
    """Generates the Roll20 roll query for situation modifiers from -10 to +10."""
    def get_step_label(s):
        if s == 0: return "None"
        sign = "+" if s > 0 else "-"
        val = abs(s)
        if val == 1: d = "d4"
        elif val == 2: d = "d6"
        elif val == 3: d = "d8"
        elif val == 4: d = "d12"
        elif val == 5: d = "d20"
        else: d = f"{val-4}d20"
        return f"{s:+d} Steps ({sign}{d})"

    def get_step_value(s):
        if s == 0: return "1d20cs<1cf>20"
        sign = "+" if s > 0 else "-"
        val = abs(s)
        if val == 1: d = "1d4"
        elif val == 2: d = "1d6"
        elif val == 3: d = "1d8"
        elif val == 4: d = "1d12"
        elif val == 5: d = "1d20"
        else: d = f"{val-4}d20"
        return f"1d20cs<1cf>20{sign}{d}cs<0cf<0"

    all_steps = list(range(-10, 11))
    if default_step in all_steps:
        all_steps.remove(default_step)
    
    ordered_steps = [default_step] + sorted(all_steps)
    options = []
    for s in ordered_steps:
        options.append(f"{get_step_label(s)}, {get_step_value(s)}")
    
    return f"?{{Situation Modifier|{'|'.join(options)}}}"

def parse_yaml_skills(file_path):
    """Parses the YAML skill source and returns the structured data for the sheet."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    items = data.get('items', data)
    attributes = ['STR', 'DEX', 'CON', 'INT', 'WIL', 'PER']
    skills_by_attr = {attr: [] for attr in attributes}

    for broad_key, broad_val in items.items():
        attr = broad_val.get('attribute', 'INT')
        if attr not in skills_by_attr:
            attr = 'INT'
            
        en_loc = next((loc['en'] for loc in broad_val.get('localized', []) if 'en' in loc), None)
        name = en_loc.get('name', broad_key.replace('-', ' ').title()) if en_loc else broad_key.replace('-', ' ').title()
        untrained = 'YES' if not broad_val.get('trained_only', False) else 'NO'
        cost = broad_val.get('cost', 0)
        
        specialties = []
        specs_data = broad_val.get('items', {})
        for spec_key, spec_val in specs_data.items():
            spec_en_loc = next((loc['en'] for loc in spec_val.get('localized', []) if 'en' in loc), None)
            spec_name = spec_en_loc.get('name', spec_key.replace('-', ' ').title()) if spec_en_loc else spec_key.replace('-', ' ').title()
            spec_attr = spec_val.get('attribute', attr)
            spec_untrained = 'YES' if not spec_val.get('trained_only', False) else 'NO'
            spec_cost = spec_val.get('cost', 0)
            
            rb = [{'rank': str(b.get('rank')), 'title': b.get('title')} for b in spec_val.get('rank_benefits', [])]
            
            spec_entry = {'n': spec_name, 'at': spec_attr, 'u': spec_untrained, 'c': spec_cost}
            if rb: spec_entry['rb'] = rb
            specialties.append(spec_entry)

        broad_entry = {
            'n': name, 'u': untrained, 'at': attr,
            'sp': sorted(specialties, key=lambda x: x['n']),
            'c': cost
        }
        skills_by_attr[attr].append(broad_entry)

    skills_data = []
    for attr in attributes:
        if skills_by_attr[attr]:
            sorted_skills = sorted(skills_by_attr[attr], key=lambda x: x['n'])
            skills_data.append({'a': attr, 's': sorted_skills})
    return skills_data

def generate_skills_html(data_list, indent_level=3, is_psionics=False):
    """Generates the HTML for broad and specialty skills based on the provided data."""
    all_broad_skills = []
    for group in data_list:
        all_broad_skills.extend(group["s"])
    
    all_broad_skills.sort(key=lambda x: x["n"])
    
    output_html = []
    skill_ids = []
    indent = "\t" * indent_level

    broad_roll_results = f"{{{{results= [[{get_alternity_roll_query(default_step=1)}]]}}}}"
    spec_roll_results = f"{{{{results= [[{get_alternity_roll_query(default_step=0)}]]}}}}"

    for skill in all_broad_skills:
        name = skill["n"]
        attr_short = skill["at"]
        is_untrained = skill["u"]
        attr_full = ABILITY_MAP[attr_short]
        id_name = clean_id(name)
        
        fallback_path = "psionics" if is_psionics else "skills"
        default_url = f"https://aaa.dimble.net/{fallback_path}/{name.lower().replace(' ', '-')}"
        url = SKILL_URL_MAP.get(name, default_url)
        
        if "https://aaa.dimble.net/psionics/" in url:
            url = url.replace("/psionics/", "/core-mechanics/psionics/")

        roll_scores = f"{{{{score= [[@{{{id_name}O}}]]/[[@{{{id_name}G}}]]/[[@{{{id_name}A}}]]}}}}"
        wiki_link = f"{{{{wiki= [↗ Wiki Documentation]({url})}}}}"

        if is_untrained == "NO":
            formula = f"(floor(@{{{attr_full}}}*@{{{id_name}}}))"
        else:
            formula = f"(floor(@{{{attr_full}}}/(2-@{{{id_name}}})))"
            
        cost = skill.get("c", 0)
        trained_only_class = " sheet-trained-only" if is_untrained == "NO" else ""
        info_icon = build_info_icon(cost, is_untrained)
        h = f'{indent}<div class="sheet-skill-group-box">\n'
        h += f'{indent}\t<div class="sheet-skill-header-row">\n'
        h += f'{indent}\t\t<div></div><div class="sheet-skill-name">{name.upper()}</div><div></div>\n'
        h += f'{indent}\t\t<div class="sheet-skill-ability-label">RANKS</div>\n'
        h += f'{indent}\t\t<div class="sheet-skill-ability-label">SCORE</div>\n'
        h += f'{indent}\t</div>\n'
        h += f'{indent}\t<div class="sheet-skill-row">\n'
        h += f'{indent}\t\t<button type="roll" name="roll_{id_name}" value="&{{template:default}} {{{{name= @{{character_name}} - {name}}}}} {roll_scores} {broad_roll_results} {wiki_link}"></button>\n'
        h += f'{indent}\t\t<div class="sheet-skill-name{trained_only_class}">{name} <button type="roll" name="roll_{id_name}_link" class="sheet-skill-link" value="[{name} Wiki]({url})">&#x2197;</button>{info_icon}</div>\n'
        h += f'{indent}\t\t<div class="sheet-skill-ability-label">{attr_short}</div>\n'
        h += f'{indent}\t\t<input type="checkbox" name="attr_{id_name}" value="1" />\n'
        h += f'{indent}\t\t<div class="sheet-skill-score-cell">\n'
        h += f'{indent}\t\t\t<input type="text" name="attr_{id_name}O" class="sheet-scoredisabled" disabled="true" value="{formula}">/\n'
        h += f'{indent}\t\t\t<input type="text" name="attr_{id_name}G" class="sheet-scoredisabled" disabled="true" value="(floor(@{{{id_name}O}}/2))">/\n'
        h += f'{indent}\t\t\t<input type="text" name="attr_{id_name}A" class="sheet-scoredisabled" disabled="true" value="(floor(@{{{id_name}O}}/4))">\n'
        h += f'{indent}\t\t</div>\n'
        h += f'{indent}\t</div>\n'
        h += f'{indent}\t<div class="sheet-specialties-container">\n'
        
        for spec in skill.get("sp", []):
            spec_name = spec["n"]
            spec_attr = spec["at"]
            spec_untrained = spec["u"]
            spec_attr_full = ABILITY_MAP[spec_attr]
            spec_id = clean_id(spec_name)
            
            spec_url = SKILL_URL_MAP.get(spec_name)
            if spec_url:
                if "https://aaa.dimble.net/psionics/" in spec_url:
                    spec_url = spec_url.replace("/psionics/", "/core-mechanics/psionics/")
            else:
                anchor = spec_name.lower().replace(' ', '-').replace('\'', '').replace('(', '').replace(')', '')
                spec_url = f"{url}#{anchor}"
            
            spec_wiki_link = f"{{{{wiki= [↗ Wiki Documentation]({spec_url})}}}}"

            if spec_untrained == "NO":
                spec_formula = f"(floor(((@{{{spec_id}Rank}}+@{{{spec_attr_full}}})*@{{{id_name}}}) * (@{{{spec_id}Rank}}/(@{{{spec_id}Rank}}+0.001)) + 0.5))"
                trained_only_class = " sheet-trained-only"
            else:
                spec_formula = f"(floor(((@{{{spec_id}Rank}}*@{{{id_name}}})+@{{{spec_attr_full}}})/(2-@{{{id_name}}})))"
                trained_only_class = ""
                
            spec_cost = spec.get("c", 0)
            spec_rank_benefits = spec.get("rb", None)
            spec_info_icon = build_info_icon(spec_cost, spec_untrained, spec_rank_benefits)
            
            h += f'{indent}\t\t<div class="sheet-skill-row sheet-spec">\n'
            h += f'{indent}\t\t\t<button type="roll" name="roll_{spec_id}" value="&{{template:default}} {{{{name= @{{character_name}} - {spec_name}}}}} {{{{score= [[@{{{spec_id}O}}]]/[[@{{{spec_id}G}}]]/[[@{{{spec_id}A}}]]}}}} {spec_roll_results} {spec_wiki_link}"></button>\n'
            h += f'{indent}\t\t\t<div class="sheet-skill-name{trained_only_class}">{spec_name} <button type="roll" name="roll_{spec_id}_link" class="sheet-skill-link" value="[{spec_name} Wiki]({spec_url})">&#x2197;</button>{spec_info_icon}</div>\n'
            h += f'{indent}\t\t\t<div class="sheet-skill-ability-label">{spec_attr}</div>\n'
            h += f'{indent}\t\t\t<input type="number" name="attr_{spec_id}Rank" class="sheet-score" value="0">\n'
            h += f'{indent}\t\t\t<div class="sheet-skill-score-cell">\n'
            h += f'{indent}\t\t\t\t<input type="text" name="attr_{spec_id}O" class="sheet-scoredisabled" disabled="true" value="{spec_formula}">/\n'
            h += f'{indent}\t\t\t\t<input type="text" name="attr_{spec_id}G" class="sheet-scoredisabled" disabled="true" value="(floor(@{{{spec_id}O}}/2))">/\n'
            h += f'{indent}\t\t\t\t<input type="text" name="attr_{spec_id}A" class="sheet-scoredisabled" disabled="true" value="(floor(@{{{spec_id}O}}/4))">\n'
            h += f'{indent}\t\t\t</div>\n'
            h += f'{indent}\t\t</div>\n'
        h += f'{indent}\t</div>\n'
        h += f'{indent}</div>\n'
        output_html.append(h)
        skill_ids.append(id_name)

    return "".join(output_html), skill_ids

def build():
    root_dir = os.path.dirname(os.path.dirname(__file__))
    src_dir = os.path.join(os.path.dirname(__file__), 'src/tabs')
    output_file = os.path.join(os.path.dirname(__file__), 'Alternity_RPG.html')
    
    skills_yaml = os.path.join(root_dir, 'sources/data_sources/skills.yaml')
    psionics_yaml = os.path.join(root_dir, 'sources/data_sources/psionics.yaml')
    
    print(f"Loading skills from {skills_yaml}...")
    skills_data = parse_yaml_skills(skills_yaml)
    print(f"Loading psionics from {psionics_yaml}...")
    psionics_data = parse_yaml_skills(psionics_yaml)

    # Files to join in order
    files = [
        'header.html', 'core.html', 'skills.html', 'psionics.html',
        'cybermutations.html', 'wealthequipment.html', 'customskills.html',
        'options.html', 'starship.html', 'footer.html'
    ]
    
    final_html = []
    all_skill_ids = []

    roll_query_0 = get_alternity_roll_query(default_step=0)
    roll_query_1 = get_alternity_roll_query(default_step=1)
    
    for filename in files:
        path = os.path.join(src_dir, filename)
        if not os.path.exists(path):
            print(f"Warning: {path} not found. Skipping.")
            continue
            
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if filename == 'skills.html':
            skills_html, skill_ids = generate_skills_html(skills_data, indent_level=3)
            content = content.replace('<!-- SKILLS_PLACEHOLDER -->', skills_html)
            all_skill_ids.extend(skill_ids)
        elif filename == 'psionics.html':
            psionics_html, skill_ids = generate_skills_html(psionics_data, indent_level=3, is_psionics=True)
            content = content.replace('<!-- PSIONICS_PLACEHOLDER -->', psionics_html)
            all_skill_ids.extend(skill_ids)
            
        content = content.replace('<!-- ROLL_QUERY_DEFAULT_0 -->', roll_query_0)
        content = content.replace('<!-- ROLL_QUERY_DEFAULT_1 -->', roll_query_1)
            
        final_html.append(content)
        
    combined_html = "".join(final_html)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(combined_html)
        
    print(f"Successfully built {output_file} from modular source files.")

if __name__ == "__main__":
    build()

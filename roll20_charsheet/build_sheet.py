
import os
import sys
import json

# Add src to the path so we can import skills_data
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from skills_data import SKILLS_DATA, PSIONICS_DATA, ABILITY_MAP

def clean_id(n):
    return n.replace(' ','').replace('-','').replace('.','').replace(',','').replace('—','')

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
                    urls[name] = "https://aaa.dimble.net" + item["skill_url"]
    except Exception as e:
        print(f"Error loading skill URLs: {e}")
        
    # Psionics might not be in the same JSON or format, adding fallback for them if needed
    # But usually broad skills follow the pattern
    return urls

SKILL_URL_MAP = get_skill_urls()

def get_smart_anchor(item):
    """Generates a Hugo-compatible anchor based on the user's website patterns."""
    name = item.get("n", "").replace('[Specific]', '').replace('[spec]', '').strip()
    attr = item.get("at", "")
    pr = item.get("u", "") # In the sheet data, 'u' is "YES" or "NO"
    
    # Mapping sheet terminology to website terminology
    # Note: Medical Science is 'u': 'NO', which means "Requires training"
    pr_label = ""
    if pr == "NO":
        pr_label = "Trained Only"
    
    parts = []
    if attr: parts.append(attr)
    if pr_label: parts.append(pr_label)
    
    if parts:
        heading = f"{name} ({' - '.join(parts)})"
    else:
        heading = name
        
    # Hugo-like anchorize logic derived from user example "surgery-int---trained-only"
    import re
    anchor = heading.lower()
    anchor = anchor.replace(" - ", "---")
    anchor = anchor.replace(" (", "-")
    anchor = anchor.replace(" ", "-")
    anchor = anchor.replace(")", "")
    return anchor

def generate_skills_html(data_list, indent_level=3):
    """Generates the HTML for broad and specialty skills based on the provided data."""
    all_broad_skills = []
    for group in data_list:
        all_broad_skills.extend(group["s"])
    
    all_broad_skills.sort(key=lambda x: x["n"])
    
    output_html = []
    skill_ids = []
    indent = "\t" * indent_level

    for skill in all_broad_skills:
        name = skill["n"]
        attr_short = skill["at"]
        is_untrained = skill["u"]
        attr_full = ABILITY_MAP[attr_short]
        id_name = clean_id(name)
        
        # Base URL for the broad skill
        url = f"https://aaa.dimble.net/skills/{name.lower().replace(' ', '-')}"

        # Common roll value partials
        roll_scores = f"{{{{score= [[@{{{id_name}O}}]]/[[@{{{id_name}G}}]]/[[@{{{id_name}A}}]]}}}}"
        roll_results = "{{results= [[?{Situation Modifier|None, 1d20cs<1cf>20|-5 Steps (-d20), 1d20cs<1cf>20-1d20cs<0cf<0|-4 Steps (-d12), 1d20cs<1cf>20-1d12cs<0cf<0|-3 Steps (-d8), 1d20cs<1cf>20-1d8cs<0cf<0|-2 Steps (-d6), 1d20cs<1cf>20-1d6cs<0cf<0|-1 Steps (-d4), 1d20cs<1cf>20-1d4cs<0cf<0|+1 Steps (+d4), 1d20cs<1cf>20+1d4cs<0cf<0|+2 Steps (+d6), 1d20cs<1cf>20+1d6cs<0cf<0|+3 Steps (+d8), 1d20cs<1cf>20+1d8cs<0cf<0|+4 Steps (+d12), 1d20cs<1cf>20+1d12cs<0cf<0|+5 Steps (+d20), 1d20cs<1cf>20+1d20cs<0cf<0|+6 Steps (+2d20), 1d20cs<1cf>20+2d20cs<0cf<0|+7 Steps (+3d20), 1d20cs<1cf>20+3d20cs<0cf<0}]]}}"
        wiki_link = f"{{{{wiki= [↗ Wiki Documentation]({url})}}}}"

        # Broad skill formula
        if is_untrained == "NO":
            formula = f"(floor(@{{{attr_full}}}*@{{{id_name}}}))"
        else:
            formula = f"(floor(@{{{attr_full}}}/(2-@{{{id_name}}})))"
            
        # Broad Skill Row (Simplified, removed collapse/expand)
        h = f'{indent}<div class="sheet-skill-group-box">\n'
        h += f'{indent}\t<div class="sheet-skill-header-row">\n'
        h += f'{indent}\t\t<div></div><div class="sheet-skill-name">{name.upper()}</div><div></div>\n'
        h += f'{indent}\t\t<div class="sheet-skill-ability-label">RANKS</div>\n'
        h += f'{indent}\t\t<div class="sheet-skill-ability-label">SCORE</div>\n'
        h += f'{indent}\t</div>\n'
        h += f'{indent}\t<div class="sheet-skill-row">\n'
        h += f'{indent}\t\t<button type="roll" name="roll_{id_name}" value="&{{template:default}} {{{{name= @{{character_name}} - {name}}}}} {roll_scores} {roll_results} {wiki_link}"></button>\n'
        h += f'{indent}\t\t<div class="sheet-skill-name">{name} <button type="roll" name="roll_{id_name}_link" class="sheet-skill-link" value="[{name} Wiki]({url})">&#x2197;</button></div>\n'
        h += f'{indent}\t\t<div class="sheet-skill-ability-label">{attr_short}</div>\n'
        h += f'{indent}\t\t<input type="checkbox" name="attr_{id_name}" value="1" />\n'
        h += f'{indent}\t\t<div class="sheet-skill-score-cell">\n'
        h += f'{indent}\t\t\t<input type="text" name="attr_{id_name}O" class="sheet-scoredisabled" disabled="true" value="{formula}">/\n'
        h += f'{indent}\t\t\t<input type="text" name="attr_{id_name}G" class="sheet-scoredisabled" disabled="true" value="(floor(@{{{id_name}O}}/2))">/\n'
        h += f'{indent}\t\t\t<input type="text" name="attr_{id_name}A" class="sheet-scoredisabled" disabled="true" value="(floor(@{{{id_name}O}}/4))">\n'
        h += f'{indent}\t\t</div>\n'
        h += f'{indent}\t</div>\n'
        h += f'{indent}\t<div class="sheet-specialties-container">\n'
        
        # Specialty Skill Rows
        for spec in skill.get("sp", []):
            spec_name = spec["n"]
            spec_attr = spec["at"]
            spec_untrained = spec["u"]
            spec_attr_full = ABILITY_MAP[spec_attr]
            spec_id = clean_id(spec_name)
            
            # Smart Anchor generation for specialties
            anchor = get_smart_anchor(spec)
            spec_url = f"{url}#{anchor}"
            spec_wiki_link = f"{{{{wiki= [↗ Wiki Documentation]({spec_url})}}}}"

            if spec_untrained == "NO":
                spec_formula = f"(floor(((@{{{spec_id}Rank}}+@{{{spec_attr_full}}})*@{{{id_name}}}) * (@{{{spec_id}Rank}}/(@{{{spec_id}Rank}}+0.001)) + 0.5))"
                trained_only_class = " sheet-trained-only"
            else:
                spec_formula = f"(floor(((@{{{spec_id}Rank}}*@{{{id_name}}})+@{{{spec_attr_full}}})/(2-@{{{id_name}}})))"
                trained_only_class = ""
                
            h += f'{indent}\t\t<div class="sheet-skill-row sheet-spec">\n'
            h += f'{indent}\t\t\t<button type="roll" name="roll_{spec_id}" value="&{{template:default}} {{{{name= @{{character_name}} - {spec_name}}}}} {{{{score= [[@{{{spec_id}O}}]]/[[@{{{spec_id}G}}]]/[[@{{{spec_id}A}}]]}}}} {roll_results} {spec_wiki_link}"></button>\n'
            h += f'{indent}\t\t\t<div class="sheet-skill-name{trained_only_class}">{spec_name} <button type="roll" name="roll_{spec_id}_link" class="sheet-skill-link" value="[{spec_name} Wiki]({spec_url})">&#x2197;</button></div>\n'
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
    src_dir = 'src/tabs'
    output_file = 'Alternity_RPG.html'
    
    # Files to join in order
    files = [
        'header.html',
        'core.html',
        'skills.html',
        'psionics.html',
        'cybermutations.html',
        'wealthequipment.html',
        'customskills.html',
        'options.html',
        'starship.html',
        'footer.html'
    ]
    
    final_html = []
    all_skill_ids = []
    
    for filename in files:
        path = os.path.join(src_dir, filename)
        if not os.path.exists(path):
            print(f"Warning: {path} not found. Skipping.")
            continue
            
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Handle dynamic content
        if filename == 'skills.html':
            skills_html, skill_ids = generate_skills_html(SKILLS_DATA, indent_level=3)
            content = content.replace('<!-- SKILLS_PLACEHOLDER -->', skills_html)
            all_skill_ids.extend(skill_ids)
        elif filename == 'psionics.html':
            psionics_html, skill_ids = generate_skills_html(PSIONICS_DATA, indent_level=3)
            content = content.replace('<!-- PSIONICS_PLACEHOLDER -->', psionics_html)
            all_skill_ids.extend(skill_ids)
            
        final_html.append(content)
        
    combined_html = "".join(final_html)
    
    # Write to final file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(combined_html)
        
    print(f"Successfully built {output_file} from modular source files.")

if __name__ == "__main__":
    build()

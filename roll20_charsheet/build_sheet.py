
import os
import sys

# Add src to the path so we can import skills_data
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from skills_data import SKILLS_DATA, PSIONICS_DATA, ABILITY_MAP

def clean_id(n):
    return n.replace(' ','').replace('-','').replace('.','').replace(',','').replace('—','')

def generate_skills_html(data_list, indent_level=3):
    """Generates the HTML for broad and specialty skills based on the provided data."""
    all_broad_skills = []
    for group in data_list:
        all_broad_skills.extend(group["s"])
    
    all_broad_skills.sort(key=lambda x: x["n"])
    
    output_html = []
    indent = "\t" * indent_level

    for skill in all_broad_skills:
        name = skill["n"]
        attr_short = skill["at"]
        is_untrained = skill["u"]
        attr_full = ABILITY_MAP[attr_short]
        id_name = clean_id(name)

        # Broad skill formula
        if is_untrained == "NO":
            formula = f"(floor(@{{{attr_full}}}*@{{{id_name}}}))"
        else:
            formula = f"(floor(@{{{attr_full}}}/(2-@{{{id_name}}})))"
            
        # Broad Skill Row
        h = f'{indent}<div class="sheet-skill-group-box">\n'
        h += f'{indent}\t<input type="checkbox" name="attr_{id_name}" class="sheet-collapse-check" value="1" />\n'
        h += f'{indent}\t<div class="sheet-skill-header-row">\n'
        h += f'{indent}\t\t<div></div><div class="sheet-skill-name">{name.upper()}</div><div></div>\n'
        h += f'{indent}\t\t<div class="sheet-skill-ability-label">RANKS</div>\n'
        h += f'{indent}\t\t<div class="sheet-skill-ability-label">SCORE</div>\n'
        h += f'{indent}\t</div>\n'
        h += f'{indent}\t<div class="sheet-skill-row">\n'
        h += f'{indent}\t\t<button type="roll" name="roll_{id_name}" value="&{{template:default}} {{{{name= @{{character_name}} - {name}}}}} {{{{score= [[@{{{id_name}O}}]]/[[@{{{id_name}G}}]]/[[@{{{id_name}A}}]]}}}} {{{{results= [[?{{Situation Modifier|None, 1d20cs<1cf>20|-5 Steps (-d20), 1d20cs<1cf>20-1d20cs<0cf<0|-4 Steps (-d12), 1d20cs<1cf>20-1d12cs<0cf<0|-3 Steps (-d8), 1d20cs<1cf>20-1d8cs<0cf<0|-2 Steps (-d6), 1d20cs<1cf>20-1d6cs<0cf<0|-1 Steps (-d4), 1d20cs<1cf>20-1d4cs<0cf<0|+1 Steps (+d4), 1d20cs<1cf>20+1d4cs<0cf<0|+2 Steps (+d6), 1d20cs<1cf>20+1d6cs<0cf<0|+3 Steps (+d8), 1d20cs<1cf>20+1d8cs<0cf<0|+4 Steps (+d12), 1d20cs<1cf>20+1d12cs<0cf<0|+5 Steps (+d20), 1d20cs<1cf>20+1d20cs<0cf<0|+6 Steps (+2d20), 1d20cs<1cf>20+2d20cs<0cf<0|+7 Steps (+3d20), 1d20cs<1cf>20+3d20cs<0cf<0}}]]}}}}"></button>\n'
        h += f'{indent}\t\t<div class="sheet-skill-name">{name}</div>\n'
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

            if spec_untrained == "NO":
                # Trained only: requires both Broad skill (@{bi}) and Rank > 0
                spec_formula = f"(floor(((@{{{spec_id}Rank}}+@{{{spec_attr_full}}})*@{{{id_name}}}) * (@{{{spec_id}Rank}}/(@{{{spec_id}Rank}}+0.001))))"
            else:
                # Normal specialty: can be used untrained (+1 step penalty if broad is missing)
                spec_formula = f"(floor(((@{{{spec_id}Rank}}*@{{{id_name}}})+@{{{spec_attr_full}}})/(2-@{{{id_name}}})))"
                
            h += f'{indent}\t\t<div class="sheet-skill-row sheet-spec">\n'
            h += f'{indent}\t\t\t<button type="roll" name="roll_{spec_id}" value="&{{template:default}} {{{{name= @{{character_name}} - {spec_name}}}}} {{{{score= [[@{{{spec_id}O}}]]/[[@{{{spec_id}G}}]]/[[@{{{spec_id}A}}]]}}}} {{{{results= [[?{{Situation Modifier|None, 1d20cs<1cf>20|-5 Steps (-d20), 1d20cs<1cf>20-1d20cs<0cf<0|-4 Steps (-d12), 1d20cs<1cf>20-1d12cs<0cf<0|-3 Steps (-d8), 1d20cs<1cf>20-1d8cs<0cf<0|-2 Steps (-d6), 1d20cs<1cf>20-1d6cs<0cf<0|-1 Steps (-d4), 1d20cs<1cf>20-1d4cs<0cf<0|+1 Steps (+d4), 1d20cs<1cf>20+1d4cs<0cf<0|+2 Steps (+d6), 1d20cs<1cf>20+1d6cs<0cf<0|+3 Steps (+d8), 1d20cs<1cf>20+1d8cs<0cf<0|+4 Steps (+d12), 1d20cs<1cf>20+1d12cs<0cf<0|+5 Steps (+d20), 1d20cs<1cf>20+1d20cs<0cf<0|+6 Steps (+2d20), 1d20cs<1cf>20+2d20cs<0cf<0|+7 Steps (+3d20), 1d20cs<1cf>20+3d20cs<0cf<0}}]]}}}}"></button>\n'
            h += f'{indent}\t\t\t<div class="sheet-skill-name">{spec_name}</div>\n'
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

    return "".join(output_html)

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
    
    for filename in files:
        path = os.path.join(src_dir, filename)
        if not os.path.exists(path):
            print(f"Warning: {path} not found. Skipping.")
            continue
            
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Handle dynamic content
        if filename == 'skills.html':
            skills_html = generate_skills_html(SKILLS_DATA, indent_level=3)
            content = content.replace('<!-- SKILLS_PLACEHOLDER -->', skills_html)
        elif filename == 'psionics.html':
            psionics_html = generate_skills_html(PSIONICS_DATA, indent_level=3)
            content = content.replace('<!-- PSIONICS_PLACEHOLDER -->', psionics_html)
            
        final_html.append(content)
        
    # Write to final file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("".join(final_html))
        
    print(f"Successfully built {output_file} from modular source files.")

if __name__ == "__main__":
    build()

import subprocess
import yaml

def get_yaml_at_revision(rev):
    cmd = ["git", "show", f"{rev}:sources/data_sources/psionics.yaml"]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return yaml.safe_load(res.stdout)

def main():
    old_data = get_yaml_at_revision("3fcbb78")
    new_data = yaml.safe_load(open("sources/data_sources/psionics.yaml", "r"))
    
    old_items = old_data.get("items", {})
    new_items = new_data.get("items", {})
    
    for disc_name, disc_data in old_items.items():
        print(f"=== Discipline: {disc_name} ===")
        old_skills = disc_data.get("items", {})
        new_disc = new_items.get(disc_name, {})
        new_skills = new_disc.get("items", {})
        
        for skill_id, old_skill in old_skills.items():
            new_skill = new_skills.get(skill_id)
            if not new_skill:
                print(f"Skill {skill_id} is missing in current version!")
                continue
                
            old_loc = old_skill.get("localized", [])
            new_loc = new_skill.get("localized", [])
            
            old_en = next((item["en"] for item in old_loc if "en" in item), {})
            new_en = next((item["en"] for item in new_loc if "en" in item), {})
            
            old_desc = old_en.get("description", "").strip()
            new_desc = new_en.get("description", "").strip()
            
            if old_desc != new_desc:
                print(f"Skill: {skill_id}")
                print(f"  OLD LEN: {len(old_desc)}")
                print(f"  NEW LEN: {len(new_desc)}")
                if len(old_desc) > len(new_desc):
                    print("  -> OLD version is longer/more detailed!")
                else:
                    print("  -> NEW version is longer/more detailed!")
                print()

if __name__ == "__main__":
    main()

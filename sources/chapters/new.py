import re
import json

# Define the path to the markdown file
markdown_file_path = "/home/dimble/projects/aaa/chapters/GnS.SoT.md"

# Read the markdown content from the file
with open(markdown_file_path, 'r') as f:
    markdown_content = f.read()

# Extract "Clothing and Accessories" section
clothing_accessories_section_match = re.search(
    r"### Clothing and Accessories\n\n(.*?)(?=\n###|\n##|$)",
    markdown_content,
    re.DOTALL
)

item_descriptions = {}
if clothing_accessories_section_match:
    clothing_accessories_text = clothing_accessories_section_match.group(1).strip()

    # Split by item headings, keeping the delimiter
    # This regex needs to be robust to handle descriptions that might contain newlines
    # and to correctly identify the start of the next item or end of the section.
    # The previous regex for items_raw was a bit off, let's refine it.
    # We'll look for "Item Name (PL X):" followed by the description until the next item or end of section.
    
    # A more robust approach: find all item headers and then extract content between them
    item_pattern = re.compile(r"([A-Za-z\s,]+? \(PL \d+(?: or \d+)?\)):(.*?)(?=\n[A-Za-z\s,]+? \(PL \d+(?: or \d+)?\):|\n###|\n##|$)", re.DOTALL)
    
    for match in item_pattern.finditer(clothing_accessories_text):
        full_header = match.group(1).strip()
        description_raw = match.group(2).strip()

        # Extract clean name from header (remove PL info)
        name = re.sub(r' \(PL \d+(?: or \d+)?\)', '', full_header).strip()
        
        # Clean up description: remove leading colon if present, and strip whitespace
        description = description_raw.lstrip(':').strip()
        
        item_descriptions[name] = description

# Now, read the JSON file and update it
json_file_path = "/home/dimble/projects/aaa/site/data/goods_and_services.json"

# Read the existing JSON content
with open(json_file_path, 'r') as f:
    goods_services_data = json.load(f)

# Update descriptions in the JSON
if "clothing_and_accessories" in goods_services_data and \
        "groups" in goods_services_data["clothing_and_accessories"]:

    for group in goods_services_data["clothing_and_accessories"]["groups"]:
        if "items" in group:
            for item in group["items"]:
                item_name_json = item["name"]
                if item_name_json in item_descriptions:
                    item["description"] = item_descriptions[item_name_json]

# Write the updated JSON back to the file
updated_json_content = json.dumps(goods_services_data, indent=2)
with open(json_file_path, 'w') as f:
    f.write(updated_json_content)

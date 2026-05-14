import requests
import json
import re
import os

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '_', text)
    return text.strip('_')

def clean_wikitext(text, title):
    # Extract Infobox data if present
    infobox_data = {}
    infobox_match = re.search(r'\{\{Infobox(.*?)\}\}', text, re.DOTALL | re.IGNORECASE)
    if infobox_match:
        content = infobox_match.group(1)
        pairs = re.findall(r'\|\s*([^=]+?)\s*=\s*(.*?)\s*(?=\||$)', content, re.DOTALL)
        for k, v in pairs:
            v = re.sub(r'\[\[(.*?)\|(.*?)\]\]', r'\2', v)
            v = re.sub(r'\[\[(.*?)\]\]', r'\1', v)
            infobox_data[k.strip()] = v.strip()
    
    # Remove all templates
    text = re.sub(r'\{\{.*?\}\}', '', text, flags=re.DOTALL)

    # Convert headers
    text = re.sub(r'={4,5}\s*(.*?)\s*={4,5}', r'#### \1', text)
    text = re.sub(r'={3}\s*(.*?)\s*={3}', r'### \1', text)
    text = re.sub(r'={2}\s*(.*?)\s*={2}', r'## \1', text)
    
    text = re.sub(r'^(#+)\s*\'\'\'(.*?)\'\'\'', r'\1 \2', text, flags=re.MULTILINE)
    text = re.sub(r'^(#+)\s*\'\'(.*?)\'\'', r'\1 \2', text, flags=re.MULTILINE)

    def link_repl(match):
        page = match.group(1).strip()
        label = match.group(2).strip()
        if page.startswith('File:') or page.startswith('Category:'):
            return ''
        slug = slugify(page)
        return f'[{label}]({{{{< relref "/nations/{slug}" >}}}})'

    text = re.sub(r'\[\[([^|\]]+)\|([^|\]]+)\]\]', link_repl, text)

    def simple_link_repl(match):
        page = match.group(1).strip()
        if page.startswith('File:') or page.startswith('Category:'):
            return ''
        slug = slugify(page)
        return f'[{page}]({{{{< relref "/nations/{slug}" >}}}})'

    text = re.sub(r'\[\[([^|\]]+)\]\]', simple_link_repl, text)
    
    text = re.sub(r"'''''(.*?)'''''", r'***\1***', text)
    text = re.sub(r"'''(.*?)'''", r'**\1**', text)
    text = re.sub(r"''(.*?)''", r'*\1*', text)

    text = text.replace('<br />', '\n')
    text = text.replace('<br>', '\n')
    text = text.replace('<nowiki/>', '')
    text = text.replace('<nowiki>', '')
    text = text.replace('</nowiki>', '')

    if infobox_data:
        table = "\n| Property | Value |\n| --- | --- |\n"
        for k, v in infobox_data.items():
            if v:
                table += f"| {k} | {v} |\n"
        text = table + "\n" + text

    text = text.strip()
    return text

def fetch_page(title):
    url = "https://alternityrpg.fandom.com/api.php"
    params = {
        "action": "parse",
        "page": title,
        "prop": "wikitext",
        "format": "json"
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        if 'parse' in data:
            return data['parse']['wikitext']['*']
    except Exception as e:
        print(f"Error fetching {title}: {e}")
    return None

nations = [
    "Austrin-Ontis Unlimited", "Borealis Republic", "Hatire Community",
    "Insight", "Nariac Domain", "Orion League", "Orlamu Theocracy",
    "Rigunmor Star Consortium", "StarMech Collective", "Thuldan Empire",
    "Union of Sol", "Voidcorp", "Galactic Concord", "Stellar Nations",
    "Expansion Pentad", "First Galactic War", "Profit Confederation",
    "Second Galactic War", "Star*Drive Universe", "Stellar Ring",
    "Treaty of Concord", "Verge", "Cosimir"
]

output_dir = "sources/nations"
os.makedirs(output_dir, exist_ok=True)

for nation in nations:
    print(f"Fetching {nation}...")
    wikitext = fetch_page(nation)
    if wikitext:
        if not wikitext.strip():
            print(f"Page {nation} is empty.")
            continue
        markdown = clean_wikitext(wikitext, nation)
        filename = slugify(nation) + ".md"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w") as f:
            f.write(f"# {nation}\n\n")
            f.write(markdown)
        print(f"Saved to {filepath}")
    else:
        print(f"Failed to fetch {nation}")

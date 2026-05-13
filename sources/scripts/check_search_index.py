import json
import os
import sys

def check_index(file_path, canaries):
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return False

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: {file_path} is not valid JSON: {e}")
        return False

    count = len(data)
    print(f"Found {count} items in {file_path}")

    # Threshold check
    if count < 300:
        print(f"Warning: Item count ({count}) is lower than expected (300+).")
        # For now we don't fail on count, but we should eventually
        # return False

    # Canary checks
    missing = []
    titles = [item.get('title', '').lower() for item in data]
    for canary in canaries:
        if canary.lower() not in titles:
            missing.append(canary)

    if missing:
        print(f"Error: Missing canary items in {file_path}: {', '.join(missing)}")
        return False

    print(f"Success: {file_path} passed all checks.")
    return True

def main():
    root_dir = os.path.join(os.path.dirname(__file__), '../..')
    indices = [
        (os.path.join(root_dir, 'site/public/index.json'), ["Rifle Assault", "Modern Ranged Weapons", "The Hacker", "Alien Artifact"]),
        (os.path.join(root_dir, 'site/public/es/index.json'), ["Rifle Assault", "Armas a distancia modernas", "El Hacker", "Artefacto alienígena"])
    ]

    all_passed = True
    for path, canaries in indices:
        if not check_index(path, canaries):
            all_passed = False

    if not all_passed:
        sys.exit(1)

if __name__ == "__main__":
    main()

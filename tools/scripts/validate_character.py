#!/usr/bin/env python3
"""
Character JSON Rulebook Validator Bridge

Delegates validation directly to `CharacterEngine.js` via Node.js to ensure
`CharacterEngine` remains the single source of truth across all tools and UI.
"""

import sys
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
JS_VALIDATOR_PATH = ROOT_DIR / "tools" / "scripts" / "validate_character.js"

def main():
    cmd = ["node", str(JS_VALIDATOR_PATH)] + sys.argv[1:]
    result = subprocess.run(cmd)
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()

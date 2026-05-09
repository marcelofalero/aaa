import re

text = '[Physical Science—Physics]({{< relref "skills/physical-science#physics" >}})'
mapping = {
    "Physical Science": "Ciencias Físicas",
    "Physics": "Física"
}

# 1. Protect blocks
placeholders = []
def store_block(match):
    placeholders.append(match.group(0))
    return f"__BLOCK_PLACEHOLDER_{len(placeholders)-1}__"

# Protect Markdown URLs (the part starting from ]) and Hugo shortcodes
block_pattern = r'(\]\s*\([\s\S]*?\)|{{<[\s\S]*?>}})'
text_with_placeholders = re.sub(block_pattern, store_block, text, flags=re.DOTALL)

print(f"After protection: {text_with_placeholders}")

# 2. Apply mapping
sorted_terms = sorted(mapping.keys(), key=len, reverse=True)
for en in sorted_terms:
    es = mapping[en]
    pattern = f"\\b{re.escape(en)}\\b"
    text_with_placeholders = re.sub(pattern, es, text_with_placeholders, flags=re.IGNORECASE)

print(f"After mapping: {text_with_placeholders}")

# 3. Restore blocks
for i, block in enumerate(placeholders):
    text_with_placeholders = text_with_placeholders.replace(f"__BLOCK_PLACEHOLDER_{i}__", block)

print(f"Final: {text_with_placeholders}")

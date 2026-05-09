import re

text = 'Consulte [Physical Science—Chemistry]({{< relref "skills/physical-science#chemistry" >}}) para obtener más información.'
block_pattern = r'(\[[\s\S]*?\]\s*\([\s\S]*?\)|{{<[\s\S]*?>}})'

placeholders = []
def store_block(match):
    placeholders.append(match.group(0))
    return f"__BLOCK_PLACEHOLDER_{len(placeholders)-1}__"

text_with_placeholders = re.sub(block_pattern, store_block, text, flags=re.DOTALL)

print(f"Text with placeholders: {text_with_placeholders}")
print(f"Placeholders: {placeholders}")

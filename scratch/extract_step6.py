with open('scratch/warships_clean.txt', 'r', encoding='utf-8') as f:
    text = f.read()
start = text.find('STEP 6: SUPPORT SYSTEMS')
end = text.find('STEP 7: WEAPONS')
print(text[start:start+1000])
print("\n...snip...\n")
print(text[end-1000:end])

with open('scratch/warships_clean.txt', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('STEP 3: POWER PLANT')
end = text.find('STEP 4: ENGINES')
print(text[start:start+1500])
print("\n...snip...\n")
print(text[end-1500:end])

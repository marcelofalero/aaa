with open('scratch/warships_clean.txt', 'r', encoding='utf-8') as f:
    clean_txt = f.read()

start_idx = clean_txt.find("STEP 3: POWER PLANT")
end_idx = clean_txt.find("STEP 6: SUPPORT SYSTEMS")

eng_text = clean_txt[start_idx:end_idx]
with open('scratch/eng_clean.txt', 'w', encoding='utf-8') as f:
    f.write(eng_text)

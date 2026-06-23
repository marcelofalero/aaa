with open('scratch/warships_clean.txt', 'r', encoding='utf-8') as f:
    clean_txt = f.read()

def find_end(start_str):
    idx = clean_txt.find(start_str)
    if idx == -1:
        print(f"NOT FOUND: {start_str}")
        return
    snippet = clean_txt[idx:idx+1000]
    print(f"--- START: {start_str} ---")
    print(snippet)
    print("--------------------------\n")

find_end("Table 5-3: Power Plants\n")
find_end("Table 5-4: Engines\n")
find_end("Table 5-5: FTL Drives\n")

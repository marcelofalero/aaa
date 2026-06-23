with open('scratch/warships_clean.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

table_starts = [7066, 7332, 7583, 7679, 7772, 7996, 8329, 8543]

for start in table_starts:
    # Print the start line
    print(f"--- START: {lines[start-1].strip()}")
    # Look ahead 100 lines and print the last few lines of the table
    # The table ends when the text becomes normal paragraphs (less spaces)
    # Actually I'll just print lines start to start+50, I can manually see where it ends!
    for i in range(start-1, start+50):
        print(f"{i+1}: {lines[i].strip()}")
    print("---")

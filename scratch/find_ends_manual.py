with open('scratch/warships_clean.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

table_starts = [7066, 7332, 7583, 7996, 8329, 8543]

# Table 5-8 starts at 7066.
# Let's print out lines 7080 to 7100 to find the end.
print("--- Table 5-8 ---")
for i in range(7080, 7100):
    print(f"{i}: {lines[i-1].strip()}")

# Table 5-9 starts at 7332.
print("--- Table 5-9 ---")
for i in range(7350, 7370):
    print(f"{i}: {lines[i-1].strip()}")

# Table 5-10 starts at 7583. It has multiple parts.
# Let's check part 3 around 7772.
print("--- Table 5-10 ---")
for i in range(7780, 7820):
    print(f"{i}: {lines[i-1].strip()}")

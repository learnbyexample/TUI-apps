total = 0
with open('nums.txt', 'r') as f:
    for line in f:
        total += float(line)
print(total)

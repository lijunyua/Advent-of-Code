# Part 1 + 2

def update_max_totals(max_totals, cur_total):
	for i in range(len(max_totals)):
		if cur_total > max_totals[i]:
			max_totals.insert(i, cur_total)
			max_totals.pop()
			break
	return max_totals


f = open("puzzle-input.txt", "r")
cur_total = 0
max_totals = [0, 0, 0]
for line in f:
	current = line.strip()
	if current == "":
		max_totals = update_max_totals(max_totals, cur_total)
		cur_total = 0
		continue
	cur_total += int(line.strip())

print(max_totals)
print(sum(max_totals))
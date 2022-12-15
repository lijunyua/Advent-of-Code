f = open("puzzle-input.txt", "r")

for line in f:
	info = line.strip()

track = set()
counter = 1
for i in range(len(info)):
	if i >= 14:
		if len(set(info[i-14:i])) == 14:
			print(i)
			break
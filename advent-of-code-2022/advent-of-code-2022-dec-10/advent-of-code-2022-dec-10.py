f = open("puzzle-input.txt", "r")
puzzle_input = [line.strip().split(" ") for line in f]
f.close()

# Part 1

X = [-1, 1]
cur_X = 1
cycles_completed = 0
for line in puzzle_input:
	instruction = line[0]
	if instruction == "noop":
		cycles_completed += 1
		X.append(cur_X)
	elif instruction == "addx":
		X.append(cur_X)
		cur_X += int(line[1])
		X.append(cur_X)
		cycles_completed += 2

print(sum([j * X[j] for j in range(20, 240, 40)]))

# Part 2

X.pop(0)
X.pop()
drawing = []
for i in range(cycles_completed):
	# draw pixel i during cycle i+1
	if abs((i % 40) - X[i]) <= 1:
		drawing.append("#")
	else:
		drawing.append(".")

for i in range(6):
	for j in range(40):
		print(drawing[i * 40 + j], end="")
	print()
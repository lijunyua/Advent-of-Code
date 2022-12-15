# Part 1

# elves_dict = {"A": 1, "B": 2, "C": 3}
# my_dict = {"X": 1, "Y": 2, "Z": 3}

# f = open("puzzle-input.txt", "r")

# score = 0
# for line in f:
# 	# print(line.strip().split())
# 	current = line.strip().split()
# 	elves_move = current[0]
# 	my_move = current[1]
# 	if (my_dict[my_move] - elves_dict[elves_move]) % 3 == 0:
# 		score += 3
# 	elif (my_dict[my_move] - elves_dict[elves_move]) % 3 == 1:
# 		score += 6
# 	score += my_dict[my_move]

# print(score)

# Part 2


elves_dict = {"A": 1, "B": 2, "C": 3}
my_dict = {"X": 0, "Y": 3, "Z": 6}

f = open("puzzle-input.txt", "r")

score = 0
this_total = 0
for line in f:
	this_total = 0
	# print(line.strip().split())
	current = line.strip().split()
	elves_move = current[0]
	expected = current[1]
	this_total += my_dict[expected]
	if expected == "X":
		this_total += (elves_dict[elves_move] + 2) % 3 if (elves_dict[elves_move] + 2 > 3) else elves_dict[elves_move] + 2
	if expected == "Y":
		this_total += elves_dict[elves_move]
	if expected == "Z":
		this_total += (elves_dict[elves_move] + 1) % 3 if (elves_dict[elves_move] + 1 > 3) else elves_dict[elves_move] + 1 
	print(this_total)
	score += this_total

print(score)

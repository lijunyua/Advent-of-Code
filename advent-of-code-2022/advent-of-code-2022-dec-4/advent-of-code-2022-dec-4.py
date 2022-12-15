# Part 1

# f = open("puzzle-input.txt", "r")

# counter = 0
# for line in f:
# 	current = line.strip().split(",")
# 	first = current[0].split("-")
# 	second = current[1].split("-")
# 	if int(first[0]) <= int(second[0]) and int(first[1]) >= int(second[1]):
# 		counter += 1
# 	elif int(second[0]) <= int(first[0]) and int(second[1]) >= int(first[1]):
# 		counter += 1

# print(counter)

# Part 2

f = open("puzzle-input.txt", "r")

counter = 0
for line in f:
	current = line.strip().split(",")
	first = current[0].split("-")
	second = current[1].split("-")
	if int(first[0]) <= int(second[0]) and int(first[1]) >= int(second[0]):
		counter += 1
	elif int(first[0]) > int(second[0]) and int(first[0]) <= int(second[1]):
		counter += 1


print(counter)


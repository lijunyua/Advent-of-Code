# Part 1

# priorities_lower = {chr(n): n-96 for n in range(97, 123)}
# priorities_upper = {chr(n): n-38 for n in range(65, 91)}
# priorities = dict(priorities_lower, **priorities_upper)

# # print(priorities_lower)
# # print(priorities_upper)

# f = open("puzzle-input.txt", "r")

# total = 0
# for line in f:
# 	current = line.strip()
# 	current_len = len(current)
# 	firsthalf = set(current[:current_len//2])
# 	secondhalf = set(current[current_len//2:])
# 	total += priorities[list(firsthalf.intersection(secondhalf))[0]]

# print(total)

##############################################################################

# Part 2

# priorities_lower = {chr(n): n-96 for n in range(97, 123)}
# priorities_upper = {chr(n): n-38 for n in range(65, 91)}
# priorities = dict(priorities_lower, **priorities_upper)

# f = open("puzzle-input.txt", "r")
# counter = 0
# total = 0
# for line in f:
# 	if counter % 3 == 0:
# 		first = set(line.strip())
# 	if counter % 3 == 1:
# 		second = set(line.strip())
# 	if counter % 3 == 2:
# 		third = set(line.strip())
# 		total += priorities[list(third.intersection(first.intersection(second)))[0]]
# 	counter += 1

# print(total)



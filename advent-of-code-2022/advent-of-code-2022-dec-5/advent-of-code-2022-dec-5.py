# Part 1

# import re

# f = open("puzzle-input.txt", "r")

# piles = {n:[] for n in range(1, 10)}

# info = []
# line_counter = 0
# for line in f:
# 	info.append(line)
# 	if len(line) == 1:
# 		info.pop()
# 		info.pop()
# 		for item in info[::-1]:
# 			counter = 0
# 			pile_count = 1
# 			while counter < len(item):
# 				if counter % 4 == 1:
# 					if item[counter] != " ":
# 						piles[pile_count].append(item[counter])
# 					pile_count += 1
# 				counter += 1
# 	elif line_counter >= 9:
# 		nums = re.findall(r'\d+', line)
# 		total = int(nums[0])
# 		pile_move_from = piles[int(nums[1])]
# 		len_pile_move_from = len(pile_move_from)
# 		pile_move_to = piles[int(nums[2])]	
# 		for i in range(total):
			
# 			print(pile_move_from, pile_move_to, len_pile_move_from, total)
# 			pile_move_to.append(pile_move_from.pop())



# 	line_counter += 1

# for i in range(1, 10):
# 	print(piles[i][-1], end="")
# print()


# Part 2

import re

f = open("puzzle-input.txt", "r")

piles = {n:[] for n in range(1, 10)}

info = []
line_counter = 0
for line in f:
	info.append(line)
	if len(line) == 1:
		info.pop()
		info.pop()
		for item in info[::-1]:
			counter = 0
			pile_count = 1
			while counter < len(item):
				if counter % 4 == 1:
					if item[counter] != " ":
						piles[pile_count].append(item[counter])
					pile_count += 1
				counter += 1
	elif line_counter >= 9:
		nums = re.findall(r'\d+', line)
		total = int(nums[0])
		pile_move_from = piles[int(nums[1])]
		len_pile_move_from = len(pile_move_from)
		pile_move_to = piles[int(nums[2])]	
		for i in range(total):
			print(pile_move_from, pile_move_to, len_pile_move_from, total)
			pile_move_to.append(pile_move_from.pop(len_pile_move_from-total))



	line_counter += 1

for i in range(1, 10):
	print(piles[i][-1], end="")
print()
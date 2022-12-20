import numpy as np

fd1 = open("part1-demo-input.txt", "r")
fp = open("puzzle-input.txt", "r")
part1_demo_input = [line.strip() for line in fd1]
puzzle_input = [line.strip() for line in fp]
fd1.close()
fp.close()

selected_input = puzzle_input
jet_pattern = selected_input[0]
jet_pattern_len = len(jet_pattern)
# print(jet_pattern_len)

# Part 1

def find_height(num_of_rocks):
	heights_info = []
	# Pattern types: 1 for -, 2 for +, 3 for mirror L, 4 for |, 5 for square
	pattern_1_coords = [(0, 2), (0, 3), (0, 4), (0, 5)]
	pattern_2_coords = [(0, 3), (1, 2), (1, 3), (1, 4), (2, 3)]
	pattern_3_coords = [(0, 4), (1, 4), (2, 2), (2, 3), (2, 4)]
	pattern_4_coords = [(0, 2), (1, 2), (2, 2), (3, 2)]
	pattern_5_coords = [(0, 2), (0, 3), (1, 2), (1, 3)]
	pattern_coords = [-1, pattern_1_coords, pattern_2_coords, pattern_3_coords, pattern_4_coords, pattern_5_coords]
	pattern_height = [-1, 1, 3, 3, 4, 2]

	pattern_type = 1
	rock_map = np.ones((1, 7))
	top_rock_y_coord = 0

	jet_counter = 0
	rock_counter = 0
	while rock_counter < num_of_rocks:
		# print(rock_counter)
		# if rock map not tall enough, stack it taller
		cur_pattern_height = pattern_height[pattern_type]
		if top_rock_y_coord < 3 + cur_pattern_height:
			num_of_rows = cur_pattern_height + 3 - top_rock_y_coord
			rock_map = np.vstack((np.zeros((num_of_rows, 7)), rock_map))
			top_rock_y_coord += num_of_rows
		# print(rock_map)
		# print(num_of_rows)

		# spawn the rock in the right position based on top_rock_y_coord
		coords = pattern_coords[pattern_type]
		rock_coords = []
		# if rock_counter == 1:
			# print(top_rock_y_coord)
			# print(coords)
		for coord in coords:
			rock_coords.append((top_rock_y_coord - 3 - cur_pattern_height + coord[0], coord[1]))
		# print(rock_coords)
		# break

		# rock motion
		come_to_rest = False
		while not come_to_rest:
			# Push to left / right
			if jet_counter >= jet_pattern_len:
				jet_counter %= jet_pattern_len
			jet_action = jet_pattern[jet_counter]
			new_coords = []
			if jet_action == "<":
				new_coords = [(coord[0], coord[1] - 1) for coord in rock_coords]
			elif jet_action == ">":
				new_coords = [(coord[0], coord[1] + 1) for coord in rock_coords]

			# Check if movable. If so, move left/right.
			movable = True
			for coord in new_coords:
				if coord[1] < 0 or coord[1] > 6 or rock_map[coord] != 0:
					movable = False
					break
			if movable:
				rock_coords = new_coords

			# Fall down
			new_coords = [(coord[0] + 1, coord[1]) for coord in rock_coords]
			# if rock_counter == 1:
			# 	print(new_coords)
			# Check if come to rest
			for coord in new_coords:
				if rock_map[coord] == 1:
					come_to_rest = True
			if not come_to_rest:
				rock_coords = new_coords

			jet_counter += 1

		# came to rest, draw on rock_map, update top_rock_y_coord
		for coord in rock_coords:
			rock_map[coord] = 1
		for y in range(rock_map.shape[0]):
			if not np.all(rock_map[y, :] == 0):
				top_rock_y_coord = y
				break
		# print(rock_map)
		# print(top_rock_y_coord)
		# cycle rock pattern
		if pattern_type < 5:
			pattern_type += 1
		elif pattern_type == 5:
			pattern_type = 1

		rock_counter += 1

		# print(rock_counter, jet_counter)
		if jet_counter == 1:
			heights_info.append((rock_counter, jet_counter, rock_map.shape[0] - top_rock_y_coord - 1))
		# if jet_counter == 0:
		# 	print(pattern_type)

	return rock_map.shape[0] - top_rock_y_coord - 1, heights_info

num_of_rocks = 2022
height, info = find_height(num_of_rocks)
print(height)

# Part 2

temp_rocks = 10000

_, info = find_height(temp_rocks)

base_rocks = info[0][0]
rock_period = info[1][0] - base_rocks
base_height = info[0][2]
height_period = info[1][2] - base_height

num_of_rocks = 1000000000000

remainder_rocks = (num_of_rocks - base_rocks) % rock_period

remainder_height, _ = find_height(base_rocks + remainder_rocks)
remainder_height -= base_height

print(base_height + (num_of_rocks - base_rocks) // rock_period * height_period + remainder_height)
# Just keep track of the tallest rock of each column and do not store the whole thing

# also: find a time where the jet runs to the end and the next rock "treats" the previous as ground, cycle that and find remainder

# num_of_rocks = 1000000000000

# tallest_by_columns = [0 for i in range(7)]

# jet_counter = 0
# rock_counter = 0
# while rock_counter < num_of_rocks:





# 	rock_counter += 1
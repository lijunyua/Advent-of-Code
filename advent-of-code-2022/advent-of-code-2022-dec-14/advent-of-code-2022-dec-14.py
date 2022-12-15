import math
import numpy as np

fd1 = open("part1-demo-input.txt", "r")
fp = open("puzzle-input.txt", "r") 
part1_demo_input = [[list(map(int, x)) for x in lst] for lst in [list(map(lambda x: x.split(","), line.strip().split(" -> "))) for line in fd1]]
puzzle_input = [[list(map(int, x)) for x in lst] for lst in [list(map(lambda x: x.split(","), line.strip().split(" -> "))) for line in fp]]
fd1.close()
fp.close()

selected_input = puzzle_input

# Part 1

# Find dimensions of the slice
def find_dimension(selected_input):
	min_right_dist = math.inf
	max_right_dist = -1
	max_down_dist = -1
	for path in selected_input:
		for point in path:
			if point[0] < min_right_dist:
				min_right_dist = point[0]
			if point[0] > max_right_dist:
				max_right_dist = point[0]
			if point[1] > max_down_dist:
				max_down_dist = point[1]
	return min_right_dist, max_right_dist, max_down_dist

# Create the rocks
def create_rocks(dimension, selected_input):
	slice_info = np.zeros(dimension)
	for path in selected_input:
		for point_index in range(len(path)-1):
			cur_point = path[point_index]
			next_point = path[point_index+1]
			if cur_point[0] == next_point[0]:
				left, right = min(cur_point[1], next_point[1]), max(cur_point[1], next_point[1])
				slice_info[left:right+1, cur_point[0]-min_right_dist] = 2
			elif cur_point[1] == next_point[1]:
				up, down = min(cur_point[0], next_point[0]), max(cur_point[0], next_point[0])
				up, down = up - min_right_dist, down - min_right_dist
				slice_info[cur_point[1], up:down+1] = 2
	return slice_info

def within_dimension(dimension, cur_pos):
	return cur_pos[0] < dimension[0] and cur_pos[1] >= 0 and cur_pos[1] < dimension[1]

# Generate sands
def simulate(min_right_dist, slice_info, sand_source_right):
	sand_source = sand_source_right - min_right_dist
	fall_through = False
	sand_counter = 0
	while not fall_through:
		come_to_rest = False
		sand_pos = (0, sand_source)
		while not come_to_rest:
			down = (sand_pos[0]+1, sand_pos[1])
			left_diag = (sand_pos[0]+1, sand_pos[1]-1)
			right_diag = (sand_pos[0]+1, sand_pos[1]+1)
			if within_dimension(slice_info.shape, down):
				if slice_info[down] == 0:
					sand_pos = down
					continue
			else:
				fall_through = True
				break
			if within_dimension(slice_info.shape, left_diag):
				if slice_info[left_diag] == 0:
					sand_pos = left_diag
					continue
			else:
				fall_through = True
				break
			if within_dimension(slice_info.shape, right_diag):
				if slice_info[right_diag] == 0:
					sand_pos = right_diag
					continue
				else:
					sand_counter += 1
					slice_info[sand_pos] = 1
					come_to_rest = True
					if sand_pos == (0, sand_source):
						fall_through = True
			else:
				fall_through = True
				break
	return sand_counter

min_right_dist, max_right_dist, max_down_dist = find_dimension(selected_input)
slice_info = create_rocks((max_down_dist + 1, max_right_dist - min_right_dist + 1), selected_input)
print(simulate(min_right_dist, slice_info, 500))

# Part 2

# add rocks that represent the ground
def add_ground(selected_input, sand_source_right):
	_, _, max_down_dist = find_dimension(selected_input)
	max_down_dist += 2
	min_right_dist = sand_source_right - max_down_dist
	max_right_dist = sand_source_right + max_down_dist
	selected_input.append([[min_right_dist, max_down_dist], [max_right_dist, max_down_dist]])
	return selected_input

selected_input = add_ground(selected_input, 500)
min_right_dist, max_right_dist, max_down_dist = find_dimension(selected_input)
slice_info = create_rocks((max_down_dist + 1, max_right_dist - min_right_dist + 1), selected_input)
print(simulate(min_right_dist, slice_info, 500))
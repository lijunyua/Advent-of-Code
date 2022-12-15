import math

fd1 = open("part1-demo-input.txt", "r")
fp = open("puzzle-input.txt", "r")
part1_demo_input = [list(line.strip()) for line in fd1]
puzzle_input = [list(line.strip()) for line in fp]
fd1.close()
fp.close()

selected_input = puzzle_input

# Part 1

num_of_rows = len(selected_input)
num_of_cols = len(selected_input[0])

start_pos = None

for i in range(num_of_rows):
	for j in range(num_of_cols):
		if selected_input[i][j] == "S":
			start_pos = (i, j)

height_dict = {chr(i): i-96 for i in range(97, 123)}
height_dict["S"] = 1
height_dict["E"] = 26


graph = dict()
directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]
for i in range(num_of_rows):
	for j in range(num_of_cols):
		graph[(i, j)] = []
		cur_height = height_dict[selected_input[i][j]]
		for cur_dir in directions:
			new_i = i + cur_dir[0]
			new_j = j + cur_dir[1]
			if new_i >= 0 and new_i < num_of_rows and new_j >= 0 and new_j < num_of_cols:
				if height_dict[selected_input[new_i][new_j]] <= cur_height + 1:
					graph[(i, j)].append((new_i, new_j))

def BFS(graph, selected_input, start_pos):
	visited = set()
	queue = [] 
	queue.append(start_pos)
	queue.append("level_end")
	visited.add(start_pos)
	depths = []
	depth = 1
	while queue:
		cur_pos = queue.pop(0)
		if cur_pos == "level_end":
			depth += 1
			queue.append("level_end")
			cur_pos = queue.pop(0)
			if cur_pos == "level_end":
				break
		for pos in graph[cur_pos]:
			if selected_input[pos[0]][pos[1]] == "E":
				depths.append(depth)
			if pos not in visited:
				queue.append(pos)
				visited.add(pos)
	return min(depths) if depths else math.inf

print(BFS(graph, selected_input, start_pos))

# Part 2

all_start_pos = []
for i in range(num_of_rows):
	for j in range(num_of_cols):
		if selected_input[i][j] == "a":
			all_start_pos.append((i, j))

depth_candidates = []
for cur_start_pos in all_start_pos:
	depth_candidates.append(BFS(graph, selected_input, cur_start_pos))

print(min(depth_candidates))
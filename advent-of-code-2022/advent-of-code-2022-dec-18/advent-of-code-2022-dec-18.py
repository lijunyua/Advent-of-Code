fd1 = open("part1-demo-input.txt", "r")
fp = open("puzzle-input.txt", "r")
part1_demo_input = [list(map(int, line.strip().split(","))) for line in fd1]
puzzle_input = [list(map(int, line.strip().split(","))) for line in fp]
fd1.close()
fp.close()

selected_input = puzzle_input

# Part 1

x_y = {}
x_z = {}
y_z = {}
for item in selected_input:
	x = item[0]
	y = item[1]
	z = item[2]
	if (x, y) in x_y:
		x_y[(x, y)].append(z)
	else:
		x_y[(x, y)] = [z]
	if (x, z) in x_z:
		x_z[(x, z)].append(y)
	else:
		x_z[(x, z)] = [y]
	if (y, z) in y_z:
		y_z[(y, z)].append(x)
	else:
		y_z[(y, z)] = [x]

connection_list = list(x_y.values())
connection_list.extend(list(x_z.values()))
connection_list.extend(list(y_z.values()))

counter = 0
for item in connection_list:
	if len(item) == 1:
		continue
	for coord in item:
		if coord + 1 in item:
			counter += 1

print(len(selected_input) * 6 - counter * 2)

# Part 2

x_coords = [item[0] for item in selected_input]
y_coords = [item[1] for item in selected_input]
z_coords = [item[2] for item in selected_input]
x_min, x_max = min(x_coords), max(x_coords)
y_min, y_max = min(y_coords), max(y_coords)
z_min, z_max = min(z_coords), max(z_coords)

graph = {}
for x in range(x_min-1, x_max+2):
	for y in range(y_min-1, y_max+2):
		for z in range(z_min-1, z_max+2):
			x_p = (x + 1, y, z)
			x_m = (x - 1, y, z)
			y_p = (x, y + 1, z)
			y_m = (x, y - 1, z)
			z_p = (x, y, z + 1)
			z_m = (x, y, z - 1)
			graph[(x, y, z)] = []
			graph[(x, y, z)].append(x_p)
			graph[(x, y, z)].append(x_m)
			graph[(x, y, z)].append(y_p)
			graph[(x, y, z)].append(y_m)
			graph[(x, y, z)].append(z_p)
			graph[(x, y, z)].append(z_m)
			if x == x_min - 1:
				graph[(x, y, z)].remove(x_m)
			if x == x_max + 1:
				graph[(x, y, z)].remove(x_p)
			if y == y_min - 1:
				graph[(x, y, z)].remove(y_m)
			if y == y_max + 1:
				graph[(x, y, z)].remove(y_p)
			if z == z_min - 1:
				graph[(x, y, z)].remove(z_m)
			if z == z_max + 1:
				graph[(x, y, z)].remove(z_p)

# print(x_min, x_max, y_min, y_max, z_min, z_max)				
# print(graph)

droplet = set()
for item in selected_input:
	droplet.add((item[0], item[1], item[2]))

def BFS(droplet, graph, start):
	visited = set()
	queue = []
	queue.append(start)
	visited.add(start)
	counter = 0
	while queue:
		cur_pos = queue.pop(0)
		# print(f"searching {cur_pos}, graph {graph[cur_pos]}", end=", ")
		for pos in graph[cur_pos]:

			if pos in droplet:
				# print(f"{pos}", end=" ")
				counter += 1
			if pos not in visited and pos not in droplet:
				queue.append(pos)
				visited.add(pos)
		# print("in droplet")
	return counter

# print(droplet)
print(BFS(droplet, graph, (x_min, y_min, z_min)))
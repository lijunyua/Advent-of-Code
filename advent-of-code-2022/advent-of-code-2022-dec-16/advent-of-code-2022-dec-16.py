import re
import copy

fd1 = open("part1-demo-input.txt", "r")
fp = open("puzzle-input.txt", "r")
part1_demo_input = [line.strip() for line in fd1]
puzzle_input = [line.strip() for line in fp]
fd1.close()
fp.close()

selected_input = puzzle_input

valve_flow_rate = {}
valve_connections = {}
for line in selected_input:
	flow_rate = int(re.findall("[0-9]+", line)[0])
	valves = re.findall("[A-Z][A-Z]", line)
	cur_valve = valves[0]
	connected_valves = valves[1:]
	valve_connections[cur_valve] = connected_valves
	valve_flow_rate[cur_valve] = flow_rate

# print(valve_flow_rate)

# Part 1

def BFS(graph, start, target):
	visited = set()
	queue = []
	queue.append(start)
	queue.append("level_end")
	visited.add(start)
	depths = []
	depth = 0
	while queue:
		cur_pos = queue.pop(0)
		if cur_pos == "level_end":
			depth += 1
			queue.append("level_end")
			cur_pos = queue.pop(0)
			if cur_pos == "level_end":
				break
		for pos in graph[cur_pos]:
			if pos == target:
				depths.append(depth+1)
			if pos not in visited:
				queue.append(pos)
				visited.add(pos)
	return min(depths)

starting_valve = "AA"

working_valves = [starting_valve]
for valve in valve_flow_rate.keys():
	if valve_flow_rate[valve] != 0:
		working_valves.append(valve)
# print(working_valves)

valve_distances = {valve : {} for valve in working_valves}
# print(valve_distances)
for cur_valve in working_valves:
	for target_valve in working_valves:
		if cur_valve == target_valve or target_valve == starting_valve:
			continue
		valve_distances[cur_valve][target_valve] = BFS(valve_connections, cur_valve, target_valve)

# print(valve_distances)

# for item in valve_distances.keys():
# 	if item.startswith("AA"):
# 		print(item, valve_distances[item])

working_valves.remove(starting_valve)

pressure_candidates = []
path_candidates = []

def find_pressure_candidates(opened_valves, pressure_per_min, cur_path, minutes_left, pressure_released):
	# If minutes left too small to even open current valve
	if minutes_left <= 1:
		pressure_candidates.append(pressure_released + pressure_per_min * minutes_left)
		path_candidates.append(cur_path)
		# print("there")
		# exit()
		return
		
	cur_valve = cur_path[-1]
	new_opened_valves = copy.copy(opened_valves)
	# Open current valve if it's not the starting valve
	if len(cur_path) != 1:
		new_opened_valves.add(cur_valve)
		pressure_released += pressure_per_min * 1
		pressure_per_min += valve_flow_rate[cur_valve]
		minutes_left -= 1
		# print(f'opening valve {cur_valve}, {minutes_left} minutes left, {pressure_per_min} flow, {pressure_released} total')

	# If minutes left too small to go and open another valve,
	# or all working valves are open, calculate total pressure released and return value
	cannot_open_valves = minutes_left <= (min(valve_distances[cur_valve].values()) + 1)
	if len(new_opened_valves) == len(working_valves) or cannot_open_valves:
		pressure_candidates.append(pressure_released + pressure_per_min * minutes_left)
		path_candidates.append(cur_path)
		# print("")
		# exit()
		return

	# Go to another valve
	for valve in working_valves:
		if valve != starting_valve and valve not in new_opened_valves:
			new_cur_path = copy.copy(cur_path)
			new_cur_path.append(valve)
			minutes_used = valve_distances[cur_valve][valve]
			find_pressure_candidates(new_opened_valves, pressure_per_min, new_cur_path, minutes_left-minutes_used, pressure_released + pressure_per_min * minutes_used)

find_pressure_candidates(set(), 0, [starting_valve], 30, 0)
print(max(pressure_candidates))
# print(path_candidates[1])
# for i, item in enumerate(path_candidates):
# 	# print(item[1:])
# 	if item[1:] == ["DD", "BB", "JJ", "HH"]:
# 		print(i)

# max_index = pressure_candidates.index(max(pressure_candidates))
# print(max_index)
# print(path_candidates[max_index])

# # Part 2

minutes_left = 26

class Character:
	def __init__(self):
		# possible statuses: Ready to Move, Ready to Turn On Valve, Moving
		self.status = "Ready to Move"
		self.cur_valve = starting_valve

find_pressure_candidates_elephant(set(), 0, 0, Character(), Character(), [starting_valve], [starting_valve], minutes_left)

pressure_candidates = []
path_candidates = []

def find_pressure_candidates_elephant(opened_valves, pressure_per_min, pressure_released, person,
									  elephant, person_cur_path, elephant_cur_path, minutes_left):
	# If all valves are open, or, minutes left too small to even open current valve
	if len(opened_valves) == len(working_valves) or minutes_left <= 1:
		pressure_candidates.append(pressure_released + pressure_per_min * minutes_left)
		path_candidates.append(cur_path)
		return

	if person.status == "Ready to Move" and elephant.status == "Ready to Move":
		# nested 2 fors selecting where person moves and where elephant moves
		person_cur_valve = person_cur_path[-1]
		elephant_cur_valve = elephant_cur_path[-1]
		for person_valve in working_valves:
			if person_valve != starting_valve and person_valve not in 
		

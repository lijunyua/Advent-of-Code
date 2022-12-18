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
working_valves = set(working_valves)

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
		if valve not in new_opened_valves:
			new_cur_path = copy.copy(cur_path)
			new_cur_path.append(valve)
			minutes_used = valve_distances[cur_valve][valve]
			find_pressure_candidates(new_opened_valves, pressure_per_min, new_cur_path, minutes_left-minutes_used, pressure_released + pressure_per_min * minutes_used)

find_pressure_candidates(set(), 0, [starting_valve], 30, 0)
print(max(pressure_candidates))
max_index = pressure_candidates.index(max(pressure_candidates))
print(path_candidates[max_index])

# Part 2

minutes = 26

# possible character statuses: Ready to Move, Moving, Finished
starting_timeline = {"opened_valves": set(),
					 "pressure_per_min": 0,
					 "pressure_released": 0,
					 "person": {"status": "Ready to Move",
					 			"target_valve": None,
					 			"minutes_till_arrival": 0},
					 "person_cur_path": [starting_valve],
					 "elephant": {"status": "Ready to Move",
					 			  "target_valve": None,
					 			  "minutes_till_arrival": 0},
					 "elephant_cur_path": [starting_valve]}
timelines = [starting_timeline]
for minutes_left in range(minutes, 0, -1):
	new_timelines = []
	timeline_indices_to_be_removed = []
	
	for timeline_index, timeline in enumerate(timelines):
		# release pressure
		timeline["pressure_released"] += timeline["pressure_per_min"]

		opened_valves = timeline["opened_valves"]
		# set difference to get unopened valves
		unopened_valves = working_valves - opened_valves
		person_valve = timeline["person_cur_path"][-1]
		elephant_valve = timeline["elephant_cur_path"][-1]

		# If all valves are open or minutes left too small, put everyone to "Finished":
		if len(opened_valves) == len(working_valves) or minutes_left == 1:
			timeline["person"]["status"] = "Finished"
			timeline["elephant"]["status"] = "Finished"

		# If person/elephant is ready to move, but does not have enough time to
		# go and open another unopened valve (includes any valve the other is trying to open!), put them to "Finished"
		if timeline["person"]["status"] == "Ready to Move":
			if minutes_left <= min([valve_distances[person_valve][key] for key in unopened_valves]) + 1:
				timeline["person"]["status"] = "Finished"
		if timeline["elephant"]["status"] == "Ready to Move":
			if minutes_left <= min([valve_distances[elephant_valve][key] for key in unopened_valves]) + 1:
				timeline["elephant"]["status"] = "Finished"

		person_status = timeline["person"]["status"]
		elephant_status = timeline["elephant"]["status"]

		if person_status == "Ready to Move" and elephant_status == "Ready to Move":
			# When only one unopened valve left, send nearest character to open it
			if len(unopened_valves) == 1:
				cur_target_valve = list(unopened_valves)[0]
				person_distance = valve_distances[person_valve][cur_target_valve]
				elephant_distance = valve_distances[elephant_valve][cur_target_valve]
				if person_distance <= elephant_distance:
					timeline["person"]["status"] = "Moving"
					timeline["person"]["target_valve"] = cur_target_valve
					timeline["person"]["minutes_till_arrival"] = person_distance
					timeline["elephant"]["status"] = "Finished"
				else:
					timeline["elephant"]["status"] = "Moving"
					timeline["elephant"]["target_valve"] = cur_target_valve
					timeline["elephant"]["minutes_till_arrival"] = elephant_distance
					timeline["person"]["status"] = "Finished"
			else:
				for person_target_valve in working_valves:
					for elephant_target_valve in working_valves:
						if (person_target_valve in unopened_valves and elephant_target_valve in unopened_valves and
								person_target_valve != elephant_target_valve):
							new_timeline = copy.deepcopy(timeline)
							new_timeline["person"]["status"] = "Moving"
							new_timeline["person"]["target_valve"] = person_target_valve
							# moved 1 distance in this minute after deciding where to go
							new_timeline["person"]["minutes_till_arrival"] = valve_distances[person_valve][person_target_valve] - 1
							new_timeline["elephant"]["status"] = "Moving"
							new_timeline["elephant"]["target_valve"] = elephant_target_valve
							# moved 1 distance in this minute after deciding where to go
							new_timeline["elephant"]["minutes_till_arrival"] = valve_distances[elephant_valve][elephant_target_valve] - 1
							new_timelines.append(new_timeline)
				timeline_indices_to_be_removed.append(timeline_index)

		if person_status == "Moving" and elephant_status == "Moving":
			person_minutes_till_arrival = timeline["person"]["minutes_till_arrival"]
			elephant_minutes_till_arrival = timeline["elephant"]["minutes_till_arrival"]
			if person_minutes_till_arrival != 0 and elephant_minutes_till_arrival != 0:
				timeline["person"]["minutes_till_arrival"] -= 1
				timeline["elephant"]["minutes_till_arrival"] -= 1
			# When arrived at valve, open valve if it's unopened
			elif person_minutes_till_arrival == 0 and elephant_minutes_till_arrival != 0:
				timeline["elephant"]["minutes_till_arrival"] -= 1
				timeline["person"]["status"] = "Ready to Move"
				target_valve = timeline["person"]["target_valve"]
				timeline["person_cur_path"].append(target_valve)
				# If already opened by the other, don't care wasting this minute, timelines handle this
				if target_valve in unopened_valves:
					timeline["opened_valves"].add(target_valve)
					timeline["pressure_per_min"] += valve_flow_rate[target_valve]
			elif person_minutes_till_arrival != 0 and elephant_minutes_till_arrival == 0:
				timeline["person"]["minutes_till_arrival"] -= 1
				timeline["elephant"]["status"] = "Ready to Move"
				target_valve = timeline["elephant"]["target_valve"]
				timeline["elephant_cur_path"].append(target_valve)
				# If already opened by the other, don't care wasting this minute, timelines handle this
				if target_valve in unopened_valves:
					timeline["opened_valves"].add(target_valve)
					timeline["pressure_per_min"] += valve_flow_rate[target_valve]
			else:
				timeline["person"]["status"] = "Ready to Move"
				person_target_valve = timeline["person"]["target_valve"]
				timeline["person_cur_path"].append(person_target_valve)
				# If already opened by the other, don't care wasting this minute, timelines handle this
				if person_target_valve in unopened_valves:
					timeline["opened_valves"].add(person_target_valve)
					timeline["pressure_per_min"] += valve_flow_rate[person_target_valve]

				timeline["elephant"]["status"] = "Ready to Move"
				elephant_target_valve = timeline["elephant"]["target_valve"]
				timeline["elephant_cur_path"].append(elephant_target_valve)
				# If already opened by the other, don't care wasting this minute, timelines handle this
				if elephant_target_valve in unopened_valves and elephant_target_valve != person_target_valve:
					timeline["opened_valves"].add(elephant_target_valve)
					timeline["pressure_per_min"] += valve_flow_rate[elephant_target_valve]

		if person_status == "Moving" and elephant_status == "Ready to Move":
			person_minutes_till_arrival = timeline["person"]["minutes_till_arrival"]
			if person_minutes_till_arrival != 0:
				timeline["person"]["minutes_till_arrival"] -= 1
			else:
				timeline["person"]["status"] = "Ready to Move"
				person_target_valve = timeline["person"]["target_valve"]
				timeline["person_cur_path"].append(person_target_valve)
				# If already opened by the other, don't care wasting this minute, timelines handle this
				if person_target_valve in unopened_valves:
					timeline["opened_valves"].add(person_target_valve)
					timeline["pressure_per_min"] += valve_flow_rate[person_target_valve]

			for elephant_target_valve in working_valves:
				if elephant_target_valve in unopened_valves:
					new_timeline = copy.deepcopy(timeline)
					new_timeline["elephant"]["status"] = "Moving"
					new_timeline["elephant"]["target_valve"] = elephant_target_valve
					# moved 1 distance in this minute after deciding where to go
					new_timeline["elephant"]["minutes_till_arrival"] = valve_distances[elephant_valve][elephant_target_valve] - 1
					new_timelines.append(new_timeline)
			timeline_indices_to_be_removed.append(timeline_index)

		if person_status == "Ready to Move" and elephant_status == "Moving":
			elephant_minutes_till_arrival = timeline["elephant"]["minutes_till_arrival"]
			if elephant_minutes_till_arrival != 0:
				timeline["elephant"]["minutes_till_arrival"] -= 1
			else:
				timeline["elephant"]["status"] = "Ready to Move"
				elephant_target_valve = timeline["elephant"]["target_valve"]
				timeline["elephant_cur_path"].append(elephant_target_valve)
				# If already opened by the other, don't care wasting this minute, timelines handle this
				if elephant_target_valve in unopened_valves:
					timeline["opened_valves"].add(elephant_target_valve)
					timeline["pressure_per_min"] += valve_flow_rate[elephant_target_valve]

			for person_target_valve in working_valves:
				if person_target_valve in unopened_valves:
					new_timeline = copy.deepcopy(timeline)
					new_timeline["person"]["status"] = "Moving"
					new_timeline["person"]["target_valve"] = person_target_valve
					# moved 1 distance in this minute after deciding where to go
					new_timeline["person"]["minutes_till_arrival"] = valve_distances[person_valve][person_target_valve] - 1
					new_timelines.append(new_timeline)
			timeline_indices_to_be_removed.append(timeline_index)

		if person_status == "Ready to Move" and elephant_status == "Finished":
			for person_target_valve in working_valves:
				if person_target_valve in unopened_valves:
					new_timeline = copy.deepcopy(timeline)
					new_timeline["person"]["status"] = "Moving"
					new_timeline["person"]["target_valve"] = person_target_valve
					# moved 1 distance in this minute after deciding where to go
					new_timeline["person"]["minutes_till_arrival"] = valve_distances[person_valve][person_target_valve] - 1
					new_timelines.append(new_timeline)
			timeline_indices_to_be_removed.append(timeline_index)

		if person_status == "Finished" and elephant_status == "Ready to Move":
			for elephant_target_valve in working_valves:
				if elephant_target_valve in unopened_valves:
					new_timeline = copy.deepcopy(timeline)
					new_timeline["elephant"]["status"] = "Moving"
					new_timeline["elephant"]["target_valve"] = elephant_target_valve
					# moved 1 distance in this minute after deciding where to go
					new_timeline["elephant"]["minutes_till_arrival"] = valve_distances[elephant_valve][elephant_target_valve] - 1
					new_timelines.append(new_timeline)
			timeline_indices_to_be_removed.append(timeline_index)

		if person_status == "Moving" and elephant_status == "Finished":
			person_minutes_till_arrival = timeline["person"]["minutes_till_arrival"]
			if person_minutes_till_arrival != 0:
				timeline["person"]["minutes_till_arrival"] -= 1
			else:
				timeline["person"]["status"] = "Ready to Move"
				person_target_valve = timeline["person"]["target_valve"]
				timeline["person_cur_path"].append(person_target_valve)
				# If already opened by the other, don't care wasting this minute, timelines handle this
				if person_target_valve in unopened_valves:
					timeline["opened_valves"].add(person_target_valve)
					timeline["pressure_per_min"] += valve_flow_rate[person_target_valve]

		if person_status == "Finished" and elephant_status == "Moving":
			elephant_minutes_till_arrival = timeline["elephant"]["minutes_till_arrival"]
			if elephant_minutes_till_arrival != 0:
				timeline["elephant"]["minutes_till_arrival"] -= 1
			else:
				timeline["elephant"]["status"] = "Ready to Move"
				elephant_target_valve = timeline["elephant"]["target_valve"]
				timeline["elephant_cur_path"].append(elephant_target_valve)
				# If already opened by the other, don't care wasting this minute, timelines handle this
				if elephant_target_valve in unopened_valves:
					timeline["opened_valves"].add(elephant_target_valve)
					timeline["pressure_per_min"] += valve_flow_rate[elephant_target_valve]

		if person_status == "Finished" and elephant_status == "Finished":
			pass


	timelines = [timeline for index, timeline in enumerate(timelines) if index not in timeline_indices_to_be_removed]
	timelines.extend(new_timelines)
	print(len(timelines))
	timelines.sort(key=lambda x: x["pressure_released"], reverse=True)
	timelines = timelines[:100000]
	# if minutes_left == 1:
		# break

from operator import attrgetter

print("max")
print(max(timelines, key=lambda item: item["pressure_released"]))
print("first 10")
print(timelines[:10])



# Add pressure_per_min to pressure_released












############################################################################################################################
# Below is my attempt for a recursive approach, but I have to give up since there's so many cases to check.

# minutes_left = 26

# class Character:
# 	def __init__(self):
# 		# possible statuses: Ready to Move, Ready to Turn On Valve, Moving
# 		self.status = "Ready to Move"
# 		# self.cur_valve = starting_valve
# 		# below only relevant when status is Moving
# 		self.target_valve = None
# 		self.minutes_till_arrival = 0

# find_pressure_candidates_elephant(set(), 0, 0, Character(), Character(), [starting_valve], [starting_valve], minutes_left)

# pressure_candidates = []
# path_candidates = []

# def find_pressure_candidates_elephant(opened_valves, pressure_per_min, pressure_released, person,
# 									  elephant, person_cur_path, elephant_cur_path, minutes_left):
# 	# If all valves are open, or, minutes left too small to even open current valve
# 	if len(opened_valves) == len(working_valves) or minutes_left <= 1:
# 		pressure_candidates.append(pressure_released + pressure_per_min * minutes_left)
# 		path_candidates.append(cur_path)
# 		return

# 	if person.status == "Ready to Move" and elephant.status == "Ready to Move":
# 		# nested 2 fors selecting where person moves and where elephant moves
# 		person_cur_valve = person_cur_path[-1]
# 		elephant_cur_valve = elephant_cur_path[-1]
# 		for person_target_valve in working_valves:
# 			for elephant_target_valve in working_valves:
# 				if (person_target_valve != starting_valve and elephant_target_valve != starting_valve and
# 						person_target_valve not in opened_valves and elephant_target_valve not in opened_valves and
# 						person_target_valve != elephant_target_valve):
# 					person_dist = valve_distances[person_cur_valve][person_target_valve]
# 					elephant_dist = valve_distances[elephant_cur_valve][elephant_target_valve]
# 					new_person = copy.copy(person)
# 					new_elephant = copy.copy(elephant)
# 					new_person_cur_path = copy.copy(person_cur_path)
# 					new_elephant_cur_path = copy.copy(elephant_cur_path)
# 					if person_dist < elephant_dist:
# 						new_person.status = "Ready to Turn On Valve"
# 						new_person_cur_path.append(person_target_valve)
# 						new_elephant.status = "Moving"
# 						new_elephant.minutes_till_arrival = person_dist - elephant_dist
# 						find_pressure_candidates_elephant(opened_valves, pressure_per_min, pressure_released,
# 														  new_person, new_elephant, new_person_cur_path,
# 														  new_elephant_cur_path, minutes_left - person_dist)
# 					elif person_dist > elephant_dist:
# 						new_person.status = "Moving"
# 						new_person.minutes_till_arrival = elephant_dist - person_dist
# 						new_elephant.status = "Ready to Turn On Valve"
# 						new_elephant_cur_path.append(elephant_target_valve)
# 						find_pressure_candidates_elephant(opened_valves, pressure_per_min, pressure_released,
# 														  new_person, new_elephant, new_person_cur_path,
# 														  new_elephant_cur_path, minutes_left - person_dist)
# 					else:


				

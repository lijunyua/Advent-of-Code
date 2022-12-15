import re
import numpy as np
import math

fd1 = open("part1-demo-input.txt", "r")
fp = open("puzzle-input.txt", "r")
part1_demo_input = [line.strip() for line in fd1]
puzzle_input = [line.strip() for line in fp]
fd1.close()
fp.close()

selected_input = puzzle_input

sensors = np.array([list(map(int, item[:2])) for item in list(map(lambda x: re.findall('-?[0-9]+', x), selected_input))])
beacons = np.array([list(map(int, item[2:])) for item in list(map(lambda x: re.findall('-?[0-9]+', x), selected_input))])

# # Part 1
if selected_input == part1_demo_input:
	row_number = 10
elif selected_input == puzzle_input:
	row_number = 2000000
num_of_sensors = sensors.shape[0]
distances = np.sum(np.abs(sensors - beacons), axis=1)
distances_x = np.append(distances.reshape(num_of_sensors, 1), np.zeros(num_of_sensors, dtype=int).reshape(num_of_sensors, 1), axis=1)
distances_y = np.append(np.zeros(num_of_sensors, dtype=int).reshape(num_of_sensors, 1), distances.reshape(num_of_sensors, 1), axis=1)
x_min = np.min((sensors - distances_x)[:, 0])
x_max = np.max((sensors + distances_x)[:, 0])
y_min = np.min((sensors - distances_y)[:, 1])
y_max = np.max((sensors + distances_y)[:, 1])


num_of_cols = x_max - x_min + 1
row = np.append(np.arange(x_min, x_max + 1).reshape(num_of_cols, 1), np.ones(num_of_cols, dtype=int).reshape(num_of_cols, 1) * row_number, axis=1)
# print(row)
temp1 = np.repeat(row[np.newaxis, :, :], num_of_sensors, axis=0)
# print(temp1)
temp2 = np.repeat(sensors[:, np.newaxis, :], num_of_cols, axis=1)
# print(sensors)
# print(temp2)
# print(temp1.shape, temp2.shape)
# print(np.sum(np.abs(temp1 - temp2), axis=2).shape)
temp3 = np.sum(np.abs(temp1 - temp2), axis=2)
temp4 = np.repeat(distances[:, np.newaxis], num_of_cols, axis=1)
# print(temp3)
# print(temp4)
temp5 = np.count_nonzero(np.any(temp3 <= temp4, axis=0))

# Work out number of beacons in the row
unique_beacons = np.unique(beacons, axis=0)
# print(unique_beacons)
num_of_beacons_in_row = np.count_nonzero(unique_beacons[:, 1] == row_number)
# print(num_of_beacons_in_row)
result = temp5 - num_of_beacons_in_row
print(result)

# Part 2

coords_to_check = np.zeros(2, dtype='int64').reshape(1, 2)
test = np.ones(2, dtype=int).reshape(1, 2)
# print(np.append(coords_to_check, test, axis=0))


# print(coords_to_check)
for i in range(num_of_sensors):
	sensor_x = sensors[i, 0]
	sensor_y = sensors[i, 1]
	dist = distances[i]
	# print(sensor_x, sensor_y, dist)

	left = np.arange(sensor_x - dist - 1, sensor_x + 1).reshape(-1, 1)
	right = np.arange(sensor_x, sensor_x + dist + 2).reshape(-1, 1)
	top = np.arange(sensor_y - dist - 1, sensor_y + 1).reshape(-1, 1)
	bottom = np.arange(sensor_y, sensor_y + dist + 2).reshape(-1, 1)
	# print(left)
	top_left = np.hstack((left, np.flip(top)))
	bottom_left = np.hstack((left, bottom))
	top_right = np.hstack((np.flip(right), top))
	bottom_right = np.hstack((right, np.flip(bottom)))
	# print(top_left.shape)
	# print(bottom_left.shape)
	coords_to_check = np.vstack((coords_to_check, top_left, bottom_left, top_right, bottom_right))
	# print(top_right.shape)
	# print(bottom_right.shape)

# print(coords_to_check.shape)

for i in range(coords_to_check.shape[0]):
	cur_x = coords_to_check[i, 0]
	cur_y = coords_to_check[i, 1]
	if cur_x >= 0 and cur_x <= 4000000 and cur_y >= 0 and cur_y <= 4000000:
		cur_coords = np.array([cur_x, cur_y]).reshape(1, 2)
		temp1 = np.repeat(cur_coords[:, :], num_of_sensors, axis=0)
		temp2 = np.sum(np.abs(sensors - temp1), axis=1)
		if np.all(temp2 > distances):
			print(cur_x * 4000000 + cur_y)
			break
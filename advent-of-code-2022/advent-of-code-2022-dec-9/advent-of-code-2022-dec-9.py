import numpy as np

fd1 = open("part1-demo-input.txt", "r")
fd2 = open("part2-demo-input.txt", "r")
fp = open("puzzle-input.txt", "r")

part1_demo_input = [line.strip().split(" ") for line in fd1]
part2_demo_input = [line.strip().split(" ") for line in fd2]
puzzle_input = [line.strip().split(" ") for line in fp]

fd1.close()
fd2.close()
fp.close()


##ppp##
#phhhp#
#phthp#
#phhhp#
##ppp##

# Part 1

head_cur_pos = (0, 0)
tail_cur_pos = (0, 0)

tail_history_pos = set()
tail_history_pos.add((0, 0))

direction_dict = {"R": (0, 1), "U": (1, 0), "L": (0, -1), "D": (-1, 0)}

for info in puzzle_input:
	direction = info[0]
	np_move = np.array(direction_dict[direction])
	dist = int(info[1])

	for i in range(dist):
		np_head_cur_pos = np.array(head_cur_pos)
		np_tail_cur_pos = np.array(tail_cur_pos)

		np_head_new_pos = np_head_cur_pos + np_move

		coord_diff = np_head_new_pos - np_tail_cur_pos
		abs_coord_diff = np.abs(coord_diff)

		# head and tail are adjacent
		if np.sum(abs_coord_diff) <= 1 or np.all(abs_coord_diff == 1):
			np_tail_new_pos = np_tail_cur_pos
		
		# head and tail are still on the same row or column
		elif np.any(abs_coord_diff == 0):
			np_tail_new_pos = np_tail_cur_pos + np_move
		
		# tail need to move diagonally
		else:
			np_diagonal_move = np.where(np.abs(coord_diff) > 1, coord_diff // 2, coord_diff)
			np_tail_new_pos = np_tail_cur_pos + np_diagonal_move

		# store new tail position into the set
		tail_history_pos.add(tuple(np_tail_new_pos))

		# update current head and tail positions after they've moved
		head_cur_pos = tuple(np_head_new_pos)
		tail_cur_pos = tuple(np_tail_new_pos)

print(len(tail_history_pos))


# Part 2

num_knots = 10
all_cur_pos = {i:(0, 0) for i in range(num_knots)}

tail_history_pos = set()
tail_history_pos.add((0, 0))

direction_dict = {"R": (0, 1), "U": (1, 0), "L": (0, -1), "D": (-1, 0)}

for info in puzzle_input:
	direction = info[0]
	np_move = np.array(direction_dict[direction])
	dist = int(info[1])

	for i in range(dist):

		for knot_no in range(num_knots-1):

			np_head_cur_pos = np.array(all_cur_pos[knot_no])
			np_tail_cur_pos = np.array(all_cur_pos[knot_no+1])

			if knot_no == 0:
				np_head_new_pos = np_head_cur_pos + np_move
			else:
				np_head_new_pos = np_head_cur_pos

			coord_diff = np_head_new_pos - np_tail_cur_pos
			abs_coord_diff = np.abs(coord_diff)

			# head and tail are adjacent
			if np.sum(abs_coord_diff) <= 1 or np.all(abs_coord_diff == 1):
				np_tail_new_pos = np_tail_cur_pos
			
			# head and tail are still on the same row or column
			elif np.any(abs_coord_diff == 0):
				np_tail_new_pos = np_tail_cur_pos + coord_diff // 2
			
			# tail need to move diagonally
			else:
				np_diagonal_move = np.where(np.abs(coord_diff) > 1, coord_diff // 2, coord_diff)
				np_tail_new_pos = np_tail_cur_pos + np_diagonal_move

			# if current tail is the last knot, store new tail position into the set
			if knot_no == num_knots - 2:
				tail_history_pos.add(tuple(np_tail_new_pos))

			# update current head and tail positions after they've moved
			all_cur_pos[knot_no] = tuple(np_head_new_pos)
			all_cur_pos[knot_no+1] = tuple(np_tail_new_pos)


print(len(tail_history_pos))

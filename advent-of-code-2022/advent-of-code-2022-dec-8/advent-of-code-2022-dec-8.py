f = open("puzzle-input.txt", "r")

tree_list = []
for line in f:
	tree_list.append(list(map(int, list(line.strip()))))

f.close()

num_rows = len(tree_list)
num_cols = len(tree_list[0])

left_visible = [[None for i in range(num_cols)] for j in range(num_rows)]
right_visible = [[None for i in range(num_cols)] for j in range(num_rows)]
up_visible = [[None for i in range(num_cols)] for j in range(num_rows)]
down_visible = [[None for i in range(num_cols)] for j in range(num_rows)]

left_max = [-1 for i in range(num_rows)]
right_max = [-1 for i in range(num_rows)]
up_max = [-1 for i in range(num_cols)]
down_max = [-1 for i in range(num_cols)]

for i in range(num_rows):
	for j in range(num_cols):
		cur = tree_list[i][j]
		if i == 0:
			up_visible[i][j] = True
			up_max[j] = cur
		else:
			if cur > up_max[j]:
				up_visible[i][j] = True
				up_max[j] = cur
			else:
				up_visible[i][j] = False

		if j == 0:
			left_visible[i][j] = True
			left_max[i] = cur
		else:
			if cur > left_max[i]:
				left_visible[i][j] = True
				left_max[i] = cur
			else:
				left_visible[i][j] = False
		
for i in range(num_rows-1, -1, -1):
	for j in range(num_cols-1, -1, -1):
		cur = tree_list[i][j]
		if i == num_rows-1:
			down_visible[i][j] = True
			down_max[j] = cur
		else:
			if cur > down_max[j]:
				down_visible[i][j] = True
				down_max[j] = cur
			else:
				down_visible[i][j] = False

		if j == num_cols-1:
			right_visible[i][j] = True
			right_max[i] = cur
		else:
			if cur > right_max[i]:
				right_visible[i][j] = True
				right_max[i] = cur
			else:
				right_visible[i][j] = False


total_visible = [[None for i in range(num_cols)] for j in range(num_rows)]
total = 0
for i in range(num_rows):
	for j in range(num_cols):
		if (not left_visible[i][j]) and (not right_visible[i][j]) and (not up_visible[i][j]) and (not down_visible[i][j]):
			total_visible[i][j] = False
		else:
			total_visible[i][j] = True
			total += 1

print(total)

# Part 2

left_dist = [[-1 for i in range(num_cols)] for j in range(num_rows)]
right_dist = [[-1 for i in range(num_cols)] for j in range(num_rows)]
up_dist = [[-1 for i in range(num_cols)] for j in range(num_rows)]
down_dist = [[-1 for i in range(num_cols)] for j in range(num_rows)]

for j in range(num_cols):
	col_fill = [0 for i in range(num_rows)]
	col_flag = [1 for i in range(num_rows)]
	for i in range(num_rows-1, 0, -1):
		cur_fill = [int(k >= i) for k in range(num_rows)]
		true_cur_fill = [x & y for x, y in zip(cur_fill, col_flag)]
		col_fill = [x + y for x, y in zip(col_fill, true_cur_fill)]
		change = [int(tree_list[i-1][j] < tree_list[k][j] or i-1 >= k) for k in range(num_rows)]
		col_flag = [x & y for x, y in zip(col_flag, change)]

	for i in range(num_rows):
		up_dist[i][j] = col_fill[i]

# print(up_dist)

for j in range(num_cols):
	col_fill = [0 for i in range(num_rows)]
	col_flag = [1 for i in range(num_rows)]
	for i in range(0, num_rows-1):
		cur_fill = [int(k <= i) for k in range(num_rows)]
		true_cur_fill = [x & y for x, y in zip(cur_fill, col_flag)]
		col_fill = [x + y for x, y in zip(col_fill, true_cur_fill)]
		change = [int(tree_list[i+1][j] < tree_list[k][j] or i+1 <= k) for k in range(num_rows)]
		col_flag = [x & y for x, y in zip(col_flag, change)]

	for i in range(num_rows):
		down_dist[i][j] = col_fill[i]

# print(down_dist)

for i in range(num_rows):
	row_fill = [0 for j in range(num_cols)]
	row_flag = [1 for j in range(num_cols)]
	for j in range(num_cols-1, 0, -1):
		cur_fill = [int(k >= j) for k in range(num_cols)]
		true_cur_fill = [x & y for x, y in zip(cur_fill, row_flag)]
		row_fill = [x + y for x, y in zip(row_fill, true_cur_fill)]
		change = [int(tree_list[i][j-1] < tree_list[i][k] or j-1 >= k) for k in range(num_cols)]
		row_flag = [x & y for x, y in zip(row_flag, change)]

	for j in range(num_cols):
		left_dist[i][j] = row_fill[j]

# print(left_dist)

for i in range(num_rows):
	row_fill = [0 for j in range(num_cols)]
	row_flag = [1 for j in range(num_cols)]
	for j in range(0, num_cols-1):
		cur_fill = [int(k <= j) for k in range(num_cols)]
		true_cur_fill = [x & y for x, y in zip(cur_fill, row_flag)]
		row_fill = [x + y for x, y in zip(row_fill, true_cur_fill)]
		change = [int(tree_list[i][j+1] < tree_list[i][k] or j+1 <= k) for k in range(num_cols)]
		row_flag = [x & y for x, y in zip(row_flag, change)]

	for j in range(num_cols):
		right_dist[i][j] = row_fill[j]

# print(right_dist)

scenic_score = [[-1 for i in range(num_cols)] for j in range(num_rows)]
for i in range(num_rows):
	for j in range(num_cols):
		scenic_score[i][j] = left_dist[i][j] * right_dist[i][j] * up_dist[i][j] * down_dist[i][j]

print(max(map(max, scenic_score)))
import functools

fd1 = open("part1-demo-input.txt", "r")
fp = open("puzzle-input.txt", "r")
part1_demo_input = [line.strip() for line in fd1]
puzzle_input = [line.strip() for line in fp]
fd1.close()
fp.close()

selected_input = puzzle_input


# Part 1

def compare_objects(object1, object2):
	if type(object1) == int and type(object2) == int:
		if object1 == object2:
			return 0
		return -1 if object1 < object2 else 1
	if type(object1) == int and type(object2) == list:
		object1 = [object1]
	if type(object1) == list and type(object2) == int:
		object2 = [object2]
	if not object1 and not object2:
		return 0
	if not object1:
		return -1
	if not object2:
		return 1
	index_1 = 0
	index_2 = 0
	while index_1 < len(object1) and index_2 < len(object2):
		item_1 = object1[index_1]
		item_2 = object2[index_2]
		comparison_result = compare_objects(item_1, item_2)
		if comparison_result == 0:
			index_1 += 1
			index_2 += 1
			continue
		return comparison_result
	if index_1 == len(object1) and index_2 == len(object2):
		return 0
	if index_1 == len(object1):
		return -1
	return 1


indices_sum = 0
for i in range(len(selected_input)):
	if i % 3 == 0:
		first = eval(selected_input[i])
	if i % 3 == 1:
		second = eval(selected_input[i])
		in_right_order = compare_objects(first, second)
		if in_right_order <= 0:
			indices_sum += i // 3 + 1

print(indices_sum)


# Part 2

all_lists = []
for i in range(len(selected_input)):
	if i % 3 != 2:
		all_lists.append(eval(selected_input[i]))

all_lists.append([[2]])
all_lists.append([[6]])

# found in this stack overflow question: https://stackoverflow.com/questions/46851479/python-sort-list-with-two-arguments-in-compare-function
comparator = functools.cmp_to_key(compare_objects)
all_lists.sort(key=comparator)

divider_1 = None
divider_2 = None
for i, item in enumerate(all_lists):
	if item == [[2]]:
		divider_1 = i + 1
	if item == [[6]]:
		divider_2 = i + 1
		break

print(divider_1 * divider_2)
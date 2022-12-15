class File:
	def __init__(self, name, size):
		self.name = name
		self.size = size
class Dir:
	def __init__(self, name, parent, size):
		self.name = name
		self.contents = []
		self.parent = parent
		self.size = size
	def add_content(self, new_object):
		self.contents.append(new_object)

def check_if_exists(cur_dir, name, item_type):
	for item in cur_dir.contents:
		if item.name == name and ((item_type == "dir" and type(item) == Dir) or (item_type == "file" and type(item) == File)):
			return True
	return False

f = open("puzzle-input.txt", "r")

root = Dir("/", None, -1)
root.parent = root
cur_dir = None

for line in f:
	info = line.strip().split(" ")
	if info[0] == '$':
		if info[1] == 'cd':
			if info[2] == '/':
				cur_dir = root
			elif info[2] == '..':
				cur_dir = cur_dir.parent
			else:
				for item in cur_dir.contents:
					if type(item) == Dir and item.name == info[2]:
						cur_dir = item
						break
		if info[1] == 'ls':
			pass
	else:
		if info[0] == "dir":
			if not check_if_exists(cur_dir, info[1], "dir"):
				new_dir = Dir(info[1], cur_dir, -1)
				cur_dir.contents.append(new_dir)
		else:
			if not check_if_exists(cur_dir, info[1], "file"):
				new_file = File(info[1], int(info[0]))
				cur_dir.contents.append(new_file)

# Part 1
small_sum = 0
def calculate_size1(root):
	if root.size == -1:
		global small_sum
		total = 0
		for item in root.contents:
			total += calculate_size1(item)
		root.size = total
		if root.size <= 100000:
			small_sum += root.size
		# print(root.name, root.size)
	return root.size
root_size = calculate_size1(root)
print(small_sum)

# Part 2
candidate = []
def calculate_size2(root):
	global root_size
	if type(root) == Dir:
		for item in root.contents:
			calculate_size2(item)
			if 70000000 - root_size + root.size >= 30000000:
				candidate.append(root.size)
calculate_size2(root)
print(min(candidate))

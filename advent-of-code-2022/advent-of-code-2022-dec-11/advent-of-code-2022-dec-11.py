import numpy as np
from abc import ABC, abstractmethod

fd1 = open("part1-demo-input.txt", "r")
f = open("puzzle-input.txt", "r")
part1_demo_input = [line.strip() for line in fd1]
puzzle_input = [line.strip() for line in f]
fd1.close()
f.close()

selected_input = puzzle_input

def read_monkey(monkey_info):
	return {
			"Items": list(map(int, monkey_info[1].split(": ")[1].split(", "))),
			"Operation": monkey_info[2].split(" ")[-2:],
			"Test": [int(monkey_info[3].split(" ")[-1]), int(monkey_info[4].split(" ")[-1]), int(monkey_info[5].split(" ")[-1])],
			"Inspections": 0
		   }

def read_info(selected_input):
	info = {}
	monkey_counter = 0
	line_counter = 0
	while line_counter < len(selected_input):
		info[monkey_counter] = read_monkey(selected_input[monkey_counter*7:monkey_counter*7+6])
		line_counter += 7
		monkey_counter += 1

	# Optimize the Operation field
	for i in range(monkey_counter):
		if info[i]["Operation"][1] != "old":
			info[i]["Operation"][1] = int(info[i]["Operation"][1])

	return info, monkey_counter


# Part 1

info, num_of_monkeys = read_info(selected_input)

num_of_rounds = 20
for i in range(num_of_rounds):
	for cur_monkey in range(num_of_monkeys):
		cur_operation = info[cur_monkey]["Operation"]
		cur_test = info[cur_monkey]["Test"]
		result = -1
		for cur_item in info[cur_monkey]["Items"]:
			info[cur_monkey]["Inspections"] += 1
			if cur_operation[1] == "old":
				result = int((cur_item ** 2) / 3)
			elif cur_operation[0] == "+":
				result = int((cur_item + cur_operation[1]) / 3)
			elif cur_operation[0] == "*":
				result = int((cur_item * cur_operation[1]) / 3)

			if result % cur_test[0] == 0:
				monkey_to_throw = cur_test[1]
			else:
				monkey_to_throw = cur_test[2]
			info[monkey_to_throw]["Items"].append(result)

		info[cur_monkey]["Items"] = []

monkey_inspections = [info[i]["Inspections"] for i in range(num_of_monkeys)]
monkey_inspections.sort(reverse=True)
print(monkey_inspections[0] * monkey_inspections[1])


# Part 2

info, num_of_monkeys = read_info(selected_input)
num_of_rounds = 10000

class Operation(ABC):
	@abstractmethod
	def perform_operation(*args):
		pass

class Addition(Operation):
	def __init__(self, operand2):
		self.operand2 = operand2
	def perform_operation(self, operand1):
		return operand1 + self.operand2

class Multiplication(Operation):
	def __init__(self, operand2):
		self.operand2 = operand2
	def perform_operation(self, operand1):
		return operand1 * self.operand2

class Square(Operation):
	def perform_operation(self, operand):
		return np.power(operand, 2)

operations = [info[i]["Operation"] for i in range(num_of_monkeys)]

operation_objects = []
for item in operations:
	if item[1] == "old":
		operation_objects.append(Square())
	elif item[0] == "+":
		operation_objects.append(Addition(item[1]))
	elif item[0] == "*":
		operation_objects.append(Multiplication(item[1]))

class Item:
	primes = np.array([info[i]["Test"][0] for i in range(num_of_monkeys)])
	operations = operation_objects
	tests = [info[i]["Test"][1:] for i in range(num_of_monkeys)]
	def __init__(self, worry_level, held_by_monkey_no):
		self.mods = np.array(worry_level % Item.primes)
		self.held_by_monkey_no = held_by_monkey_no
	def perform_operation(self):
		cur_operation = Item.operations[self.held_by_monkey_no]
		self.mods = cur_operation.perform_operation(self.mods) % Item.primes
	def test_and_throw_to_other_monkey(self):
		monkeys_to_throw_to = Item.tests[self.held_by_monkey_no]
		if self.mods[self.held_by_monkey_no] == 0:
			self.held_by_monkey_no = monkeys_to_throw_to[0]
		else:
			self.held_by_monkey_no = monkeys_to_throw_to[1]


all_items = []

for monkey_no in range(num_of_monkeys):
	for worry_level in info[monkey_no]["Items"]:
		all_items.append(Item(worry_level, monkey_no))

all_rounds_inspections_summary = [0 for i in range(num_of_monkeys)]
for i in range(num_of_rounds):

	for monkey_no in range(num_of_monkeys):
		for item in all_items:
			if monkey_no == item.held_by_monkey_no:
				all_rounds_inspections_summary[monkey_no] += 1
				item.perform_operation()
				item.test_and_throw_to_other_monkey()
			elif monkey_no < item.held_by_monkey_no:
				break
		all_items.sort(key=lambda item: item.held_by_monkey_no, reverse=False)

all_rounds_inspections_summary.sort(reverse=True)
print(all_rounds_inspections_summary[0] * all_rounds_inspections_summary[1])
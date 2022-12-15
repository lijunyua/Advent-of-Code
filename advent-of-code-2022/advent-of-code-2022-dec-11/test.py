import numpy as np
from abc import ABC, abstractmethod

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
		return operand1 * operand2

class Square(Operation):
	def perform_operation(operand):
		return np.pow(operand, 2)

operations = [Addition(3), Multiplication(4), Square()]
print(operations[0].perform_operation(2))
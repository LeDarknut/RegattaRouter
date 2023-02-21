import math

class Vector :

	def __init__(self, dx, dy):
		self.dx = dx
		self.dy = dy

	def norm(self) :
		return (self.dx ** 2 + self.dy ** 2) ** 0.5

	def __add__(self, operand):
		return Vector(self.dx + operand.dx, self.dy + operand.dy)

	def __mul__(self, operand):
		if isinstance(operand, Vector):
			return self.dx * operand.dx + self.dy * operand.dy
		else :
			return Vector(self.dx * operand, self.dy * operand)

	def __rmul__(self, operand):
		if isinstance(operand, Vector):
			return self.dx * operand.dx + self.dy * operand.dy
		else :
			return Vector(self.dx * operand, self.dy * operand)

	def normalize(self):
		invn = (self.dx ** 2 + self.dy ** 2) ** -0.5
		self.dx *= invn
		self.dy *= invn

	def angle(self):
		if self.dx == 0 and self.dy == 0:
			return 0
		a = math.acos(self.dx / self.norm())
		if self.dy < 0 :
			a = -a
		return a

class Point :

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def move(self, vector : Vector) :
		self.x += vector.dx
		self.y += vector.dy

	def __add__(self, operand):
		return Point(self.x + operand.dx, self.y + operand.dy)
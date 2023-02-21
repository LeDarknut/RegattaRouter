import math

class Vector :

	#Vector object

	#dx : horizontal component
	#dy : vertical component

	def __init__(self, dx : float, dy : float):
		self.dx = dx
		self.dy = dy

	@classmethod
	def fromPair(cls, pair):
		return cls(pair[0], pair[1])

	@classmethod
	def fromPoint(cls, point):
		return cls(point.x, point.y)

	def __add__(self, operand):
		#Vector addition

		return Vector(self.dx + operand.dx, self.dy + operand.dy)

	def __mul__(self, operand):
		#Vector dot product or scaling

		if isinstance(operand, Vector):
			return self.dx * operand.dx + self.dy * operand.dy
		else :
			return Vector(self.dx * operand, self.dy * operand)

	def __rmul__(self, operand):
		#Vector dot product or scaling

		if isinstance(operand, Vector):
			return self.dx * operand.dx + self.dy * operand.dy
		else :
			return Vector(self.dx * operand, self.dy * operand)

	def norm(self) :
		#Get vector's length

		return (self.dx ** 2 + self.dy ** 2) ** 0.5

	def scale(self, factor):
		#Scale the vector

		self.dx *= factor
		self.dy *= factor

	def dotproduct(self, vector):
		#Vector dot product

		return self.dx * vector.dx + self.dy * vector.dy

	def normalize(self):
		#Scale the vector to a length of 1

		invn = (self.dx ** 2 + self.dy ** 2) ** -0.5
		self.dx *= invn
		self.dy *= invn

	def angle(self):
		#Get vector's trigonometric angle

		if self.dx == 0 and self.dy == 0:
			return 0
		a = math.acos(self.dx / self.norm())
		if self.dy < 0 :
			a = -a
		return a

class Point :

	#Point object

	#x : abscisse
	#y : ordinate

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def move(self, vector : Vector) :
		#Move the point by a vector

		self.x += vector.dx
		self.y += vector.dy

	def __add__(self, vector):
		#Return point moved by a vector

		return Point(self.x + vector.dx, self.y + vector.dy)
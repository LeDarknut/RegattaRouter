import math
import random

class Vector :

	#Vector object

	#x : horizontal component
	#y : vertical component

	def __init__(self, x : float, y : float):
		self.x = x
		self.y = y

	@classmethod
	def fromPair(cls, pair):
		return cls(pair[0], pair[1])

	@classmethod
	def fromAngle(cls, angle, norm = 1):
		return cls(norm * math.cos(angle), norm * math.sin(angle))

	@classmethod
	def fromRandom(cls, w, h):
		return cls(random.random() * w, random.random() * h)

	def __add__(self, b):
		return Vector(self.x + b.x, self.y + b.y)

	def __iadd__(self, b):
		self.x += b.x
		self.y += b.y

	def __sub__(self, b):
		return Vector(self.x - b.x, self.y - b.y)

	def __isub__(self, b):
		self.x -= b.x
		self.y -= b.y

	def __neg__(self):
		return Vector(-self.x, -self.y)

	def __mul__(self, b):
		return Vector(self.x * b, self.y * b)

	def __rmul__(self, b):
		return Vector(self.x * b, self.y * b)

	def __imul__(self, b):
		self.x *= b
		self.y *= b

	def __truediv__(self, b):
		return Vector(self.x / b, self.y / b)

	def __itruediv__(self, b):
		self.x /= b
		self.y /= b

	def __mod__(self, b):
		#Set a.norm() to b
		return self * (b / self.norm())

	def __imod__(self, b):
		#Set a.norm() to b
		self *= (b / self.norm())

	def __inv__(self):
		#Set a.norm() to 1/a.norm()
		return self % (1 / self.norm())

	def __pow__(self, b):
		#Set a.norm() to a.norm() ** b
		return self % (self.square() ** (b * 0.5))

	def __ipow__(self, b):
		#Set a.norm() to a.norm() ** b
		self %= (self.square() ** (b * 0.5))

	def __or__(self, b):
		#Dot product a.b
		return self.x * b.x + self.y * b.y

	def __xor__(self, b):
		#Cosine of the a/b angle
		return (self.x * b.x + self.y * b.y) / math.sqrt(self.square() * b.square())

	def __lshift__(self, b):
		#Project b onto a
		return self * ((self | b) / self.square())

	def __ilshift__(self, b):
		#Project b onto a
		self *= ((self | b) / self.square())

	def __rshift__(self, b):
		#Project a onto b
		return b * ((self | b) / b.square())

	def __irshift__(self, b):
		#Project a onto b
		self = b * ((self | b) / b.square())

	def __eq__(self, b):
		#a == b
		return (self.x == b.x and self.y == b.y)

	def __ne__(self, b):
		#a != b
		return (self.x != b.x or self.y != b.y)

	def __lt__(self, b):
		#a.norm() < b.norm()
		return (self.square() < b.square())

	def __le__(self, b):
		#a.norm() <= b.norm()
		return (self.square() <= b.square())

	def __gt__(self, b):
		#a.norm() > b.norm()
		return (self.square() > b.square())

	def __ge__(self, b):
		#a.norm() >= b.norm()
		return (self.square() >= b.square())

	def square(self):
		#a.norm() ** 2
		return (self.x ** 2 + self.y ** 2)

	def norm(self):
		return math.sqrt(self.square())

	def slope(self):
		return self.y / self.x

	def coslope(self):
		#1/a.slope()
		return self.x / self.y

	def angle(self):
		if self.x == 0 and self.y == 0:
			return 0
		a = math.acos(self.x / self.norm())
		if self.y < 0 :
			a = -a
		return a

	def logged(self, b):
		#Set a.norm() to log_b(a.norm())
		return self % (0.5 * math.log(a.square(), b))

	def log(self, b):
		#Set a.norm() to log_b(a.norm())
		self %= (0.5 * math.log(a.square(), b))

	def exped(self, b):
		#Set a.norm() to log_b(a.norm())
		return self % (b ** a.norm())

	def exp(self, b):
		#Set a.norm() to log_b(a.norm())
		self %= (b ** a.norm())

	def rounded(self):
		return Vector(round(self.x), round(self.y))

	def round(self):
		self.x = round(self.x)
		self.y = round(self.y)

	def floored(self):
		return Vector(math.floor(self.x), math.floor(self.y))

	def floor(self):
		self.x = math.floor(self.x)
		self.y = math.floor(self.y)

	def ceiled(self):
		return Vector(math.ceil(self.x), math.ceil(self.y))

	def ceil(self):
		self.x = math.ceil(self.x)
		self.y = math.ceil(self.y)

	def absed(self):
		return Vector(abs(self.x), abs(self.y))

	def abs(self):
		self.x = abs(self.x)
		self.y = abs(self.y)

	def swapped(self):
		#(y, x)
		return Vector(self.y, self.x)

	def swap(self):
		#(y, x)
		self.x, self.y = self.y, self.x

	def vflipped(self):
		#(x, -y)
		return Vector(self.x, -self.y)

	def vflip(self):
		#(x, -y)
		self.y = -self.y

	def hflipped(self):
		#(-x, y)
		return Vector(-self.x, self.y)

	def hflip(self):
		#(-x, y)
		self.x = -self.x

	def pair(self):
		#(x, y)
		return (self.x, self.y)

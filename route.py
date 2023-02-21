from geometry import *

class Route:

	#Route object : a succession of points in space

	#trace : list of points
	#moves : list of vectors separating trace's points
	
	def __init__(self, start : Point, moves = []):
		self.trace = [start]
		self.moves = moves
		for vector in self.moves :
			self.trace.append(self.trace[-1] + vector)
	
	def move(self, vector : Vector):
		#Compute next point

		self.moves.append(vector)
		self.trace.append(self.trace[-1] + vector)

	def current(self):
		#Get last point

		return self.trace[-1]

	def peek(self, vector : Vector):
		#Get next point without saving

		return self.trace[-1] + vector

	def length(self):
		#Get length of the path

		s = 0
		if len(self.moves) > 0 :
			for vector in self.moves :
				s += vector.norm()

		return s

	def average(self):
		#Get average length of the segments

		if len(self.moves) > 0 :
			return self.length() / len(self.moves)
		else:
			return 0

	def export(self, f):
		#Get scaled and rounded path

		return [(round(point.x * f), round(point.y * f)) for point in self.trace]

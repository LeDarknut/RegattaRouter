from geometry import *

class Route:

	#Route object : a succession of points in space

	#trace : list of points
	#moves : list of vectors separating trace's points
	
	def __init__(self, start : Vector, moves = []):
		self.trace = [start]
		self.moves = moves
		for vector in self.moves :
			self.trace.append(self.trace[-1] + vector)
	
	def move(self, vector : Vector):
		#Compute next point

		self.moves.append(vector)
		self.trace.append(self.trace[-1] + vector)

	def get(self, t):
		#Get position at time (with linear interpolation)

		assert t >= 0         , "negative time"
		assert t <= self.t - 1, "time overflow"

		if isinstance(t, (numpy.floating, float)) :
			ft = math.floor(t)
			dt = t - ft
			return self.trace[ft] + dt * self.moves[ft]

		else :
			return self.trace[t]

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

		return [(point * f).rounded().pair() for point in self.trace]

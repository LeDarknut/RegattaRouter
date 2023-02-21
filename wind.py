import math
import numpy
import pickle

class WindSpaceTime :

	#WindSpaceTime object : 3-dimentional grid representing the evolution of winds through space and time
	
	#t : duration of the time grid
	#w : width of the spatial grid
	#h : height of the spatial grid
	#table : the grid table[t][x][y] = [dx, dy]

	def __init__(self, t, w, h, table = None) :
		
		if table is None :
			table = numpy.zeros(shape=(t,w,h,2))
		
		self.t = t
		self.w = w
		self.h = h
		self.table = table

	@classmethod
	def fromFile(cls, filename) :
		#Get WindSPaceTime compiled from grib
		
		return pickle.load(open("data/compiled/{0}.bin".format(filename), "rb"))
		
	def windspace(self, t) :
		#Get WindSpace object from time (with linear interpolation)

		assert t >= 0         , "negative time"
		assert t <= self.t - 1, "time overflow"

		if type(t) == float :
		
			ft = math.floor(t)
			ct = math.ceil(t)
			dt = t - ft

			return WindSpace(self.w, self.h, (1 - dt) * self.table[ft] + dt * self.table[ct])

		else :

			return WindSpace(self.w, self.h, self.table[t])
			
			
	def wind(self, t, x, y) :
		#Get Wind object from time and position (with trilinear interpolation)

		assert t >= 0         , "negative time"
		assert t <= self.t - 1, "time overflow"
		assert x >= 0         , "negative abscisse"
		assert x <= self.w - 1, "abscisse overflow"
		assert y >= 0         , "negative ordinate"
		assert y <= self.h - 1, "ordinate overflow"

		if type(t) == float or type(x) == float or type(y) == float :
		
			ft = math.floor(t)
			ct = math.ceil(t)
			dt = t - ft
			
			fx = math.floor(x)
			cx = math.ceil(x)
			dx = x - fx
			
			fy = math.floor(y)
			cy = math.ceil(y)
			dy = y - fy
			
			lerpfxfy = (1-dt) * self.table[ft][fx][fy] + dt * self.table[ct][fx][fy]
			lerpfxcy = (1-dt) * self.table[ft][fx][cy] + dt * self.table[ct][fx][cy]
			lerpcxfy = (1-dt) * self.table[ft][cx][fy] + dt * self.table[ct][cx][fy]
			lerpcxcy = (1-dt) * self.table[ft][cx][cy] + dt * self.table[ct][cx][cy]
			
			lerpfx = (1-dy) * lerpfxfy + dy * lerpfxcy
			lerpcx = (1-dy) * lerpcxfy + dy * lerpcxcy
			
			return Vector.fromPair((1-dx) * lerpfx + dx * lerpcx)

		else :

			return Vector.fromPair(self.table[t][x][y])

	def land(self, x, y) :
		#Check if there is land at position

		assert x >= 0         , "negative abscisse"
		assert x <= self.w - 1, "abscisse overflow"
		assert y >= 0         , "negative ordinate"
		assert y <= self.h - 1, "ordinate overflow"

		if type(x) == float or type(y) == float :
		
			fx = math.floor(x)
			cx = math.ceil(x)
			
			fy = math.floor(y)
			cy = math.ceil(y)

			return (numpy.isnan(self.table[0][fx][fy][0]) or
					numpy.isnan(self.table[0][fx][cy][0]) or
					numpy.isnan(self.table[0][cx][fy][0]) or
					numpy.isnan(self.table[0][cx][cy][0]))

		else :

			return numpy.isnan(self.table[0][x][y][0])
		
class WindSpace :

	#WindSpace object : 2-dimentional grid representing the evolution of wind through space

	#w : width of the spatial grid
	#h : height of the spatial grid
	#table : the grid table[x][y] = [dx, dy]
	
	def __init__(self, w, h, table = None) :
		
		if table is None :
			table = numpy.zeros(shape=(w,h,2))
		
		self.w = w
		self.h = h
		self.table = table
		
	def wind(self, x, y) :
		#Get Wind object from position (with bilinear interpolation)

		assert x >= 0         , "negative abscisse"
		assert x <= self.w - 1, "abscisse overflow"
		assert y >= 0         , "negative ordinate"
		assert y <= self.h - 1, "ordinate overflow"

		if type(x) == float or type(y) == float :
		
			fx = math.floor(x)
			cx = math.ceil(x)
			dx = x - fx
			
			fy = math.floor(y)
			cy = math.ceil(y)
			dy = y - fy
			
			lerpfx = (1-dy) * self.table[fx][fy] + dy * self.table[fx][cy]
			lerpcx = (1-dy) * self.table[cx][fy] + dy * self.table[cx][cy]
			
			return Vector.fromPair((1-dx) * lerpfx + dx * lerpcx)

		else :

			return Vector.fromPair(self.table[x][y])

	def land(self, x, y) :
		#Check if there is land at position

		assert x >= 0         , "negative abscisse"
		assert x <= self.w - 1, "abscisse overflow"
		assert y >= 0         , "negative ordinate"
		assert y <= self.h - 1, "ordinate overflow"

		if type(x) == float or type(y) == float :
		
			fx = math.floor(x)
			cx = math.ceil(x)
			
			fy = math.floor(y)
			cy = math.ceil(y)

			return (numpy.isnan(self.table[fx][fy][0]) or
					numpy.isnan(self.table[fx][cy][0]) or
					numpy.isnan(self.table[cx][fy][0]) or
					numpy.isnan(self.table[cx][cy][0]))

		else :

			return numpy.isnan(self.table[x][y][0])
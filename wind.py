import math
import numpy
import pickle

def load(filename) :
	
	return pickle.load(open("data/compiled/{0}.bin".format(filename), "rb"))

class WindSpaceTime :
	
	def __init__(self, t, w, h, table = None) :
		
		if type(table) != numpy.ndarray :
			
			table = numpy.zeros(shape=(t,w,h,2))
		
		self.t = t
		self.w = w
		self.h = h
		self.table = table
		
	def windspace(self, t) :
		
		ft = math.floor(t)
		ct = math.ceil(t)

		dt = t - ft
		
		assert ft >= 0, "negative time"
		assert ct <= self.t - 1, "time overflow"
		
		if dt == 0 :
		
			return WindSpace(self.w, self.h, self.table[ft])
			
		else :
			
			return WindSpace(self.w, self.h, (1 - dt) * self.table[ft] + dt * self.table[ct])
			
	def wind(self, t, x, y) :

		if type(t) == float or type(x) == float or type(y) == float :
		
			ft = math.floor(t)
			ct = math.ceil(t)

			dt = t - ft
			
			assert ft >= 0, "negative time"
			assert ct <= self.t - 1, "time overflow"
			
			fx = math.floor(x)
			cx = math.ceil(x)

			dx = x - fx
			
			assert fx >= 0, "negative abscisse"
			assert cx <= self.w - 1, "abscisse overflow"
			
			fy = math.floor(y)
			cy = math.ceil(y)

			dy = y - fy
			
			assert fy >= 0, "negative ordinate"
			assert cy <= self.h - 1, "ordinate overflow"
			
			lerpfxfy = (1-dt) * self.table[ft][fx][fy] + dt * self.table[ct][fx][fy]
			lerpfxcy = (1-dt) * self.table[ft][fx][cy] + dt * self.table[ct][fx][cy]
			lerpcxfy = (1-dt) * self.table[ft][cx][fy] + dt * self.table[ct][cx][fy]
			lerpcxcy = (1-dt) * self.table[ft][cx][cy] + dt * self.table[ct][cx][cy]
			
			lerpfx = (1-dy) * lerpfxfy + dy * lerpfxcy
			lerpcx = (1-dy) * lerpcxfy + dy * lerpcxcy
			
			vect = (1-dx) * lerpfx + dx * lerpcx
			
			return Wind(vect[0],vect[1])

		else :

			assert t >= 0, "negative time"
			assert t <= self.t - 1, "time overflow"
			assert x >= 0, "negative abscisse"
			assert x <= self.w - 1, "abscisse overflow"
			assert y >= 0, "negative ordinate"
			assert y <= self.h - 1, "ordinate overflow"

			vect = self.table[t][x][y]

			return Wind(vect[0],vect[1])

	def land(self, x, y) :

		if type(x) == float or type(y) == float :
		
			fx = math.floor(x)
			cx = math.ceil(x)
			
			assert fx >= 0, "negative abscisse"
			assert cx <= self.w - 1, "abscisse overflow"
			
			fy = math.floor(y)
			cy = math.ceil(y)
			
			assert fy >= 0, "negative ordinate"
			assert cy <= self.h - 1, "ordinate overflow"

			return (numpy.isnan(self.table[0][fx][fy][0]) or
					numpy.isnan(self.table[0][fx][cy][0]) or
					numpy.isnan(self.table[0][cx][fy][0]) or
					numpy.isnan(self.table[0][cx][cy][0]))

		else :

			assert x >= 0, "negative abscisse"
			assert x <= self.w - 1, "abscisse overflow"
			assert y >= 0, "negative ordinate"
			assert y <= self.h - 1, "ordinate overflow"

			return numpy.isnan(self.table[0][x][y][0])
		
class WindSpace :
	
	def __init__(self, w, h, table = False) :
		
		if type(table) != numpy.ndarray :
			
			table = numpy.zeros(shape=(w,h,2))
		
		self.w = w
		self.h = h
		self.table = table
		
	def wind(self, x, y) :

		if type(x) == float or type(y) == float :
		
			fx = math.floor(x)
			cx = math.ceil(x)

			dx = x - fx
			
			assert fx >= 0, "negative abscisse"
			assert cx <= self.w - 1, "abscisse overflow"
			
			fy = math.floor(y)
			cy = math.ceil(y)

			dy = y - fy
			
			assert fy >= 0, "negative ordinate"
			assert cy <= self.h - 1, "ordinate overflow"
			
			lerpfx = (1-dy) * self.table[fx][fy] + dy * self.table[fx][cy]
			lerpcx = (1-dy) * self.table[cx][fy] + dy * self.table[cx][cy]
			
			vect = (1-dx) * lerpfx + dx * lerpcx
			
			return Wind(vect[0],vect[1])

		else :

			assert x >= 0, "negative abscisse"
			assert x <= self.w - 1, "abscisse overflow"
			assert y >= 0, "negative ordinate"
			assert y <= self.h - 1, "ordinate overflow"

			vect = self.table[x][y]

			return Wind(vect[0],vect[1])

	def land(self, x, y) :

		if type(x) == float or type(y) == float :
		
			fx = math.floor(x)
			cx = math.ceil(x)
			
			assert fx >= 0, "negative abscisse"
			assert cx <= self.w - 1, "abscisse overflow"
			
			fy = math.floor(y)
			cy = math.ceil(y)
			
			assert fy >= 0, "negative ordinate"
			assert cy <= self.h - 1, "ordinate overflow"

			return (numpy.isnan(self.table[fx][fy][0]) or
					numpy.isnan(self.table[fx][cy][0]) or
					numpy.isnan(self.table[cx][fy][0]) or
					numpy.isnan(self.table[cx][cy][0]))

		else :

			assert x >= 0, "negative abscisse"
			assert x <= self.w - 1, "abscisse overflow"
			assert y >= 0, "negative ordinate"
			assert y <= self.h - 1, "ordinate overflow"

			return numpy.isnan(self.table[x][y][0])
		
		
class Wind :
	
	def __init__(self, x = 0, y = 0) :
		
		self.x = x
		self.y = y
		
	def __str__(self) :
		
		return "({:.1f},{:.1f})".format(self.x, self.y)
		


import math
import numpy as np
import pickle

def load(filename) :
	
	return pickle.load(open("wst/{0}.bin".format(filename), "rb"))

class WindSpaceTime :
	
	def __init__(self, t, w, h, table = None) :
		
		if type(table) != np.ndarray :
			
			table = np.zeros(shape=(t,w,h,2))
		
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
		
	
		
		
class WindSpace :
	
	def __init__(self, w, h, table = False) :
		
		if type(table) != np.ndarray :
			
			table = np.zeros(shape=(w,h,2))
		
		self.w = w
		self.h = h
		self.table = table
		
	def wind(self, x, y) :
		
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
		
		
class Wind :
	
	def __init__(self, x = 0, y = 0) :
		
		self.x = x
		self.y = y
		
	def __str__(self) :
		
		return "({:.1f},{:.1f})".format(self.x, self.y)
		


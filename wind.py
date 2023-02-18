import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animate
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
		
	def animation(self, time, Q, spacestep, timestep):
			
		U, V = self.windspace((time * timestep) % (self.t - 1)).listUV(spacestep)
		
		Q.set_UVC(U, V)
		
	def show(self, timestep = 0.1, spacestep = 1) :
		
		X, Y = self.windspace(0).listXY(spacestep)
		U, V = self.windspace(0).listUV(spacestep)
		L = self.windspace(0).mapL()
				
		fig, ax = plt.subplots(1,1)
		fig.set_figwidth(10)
		fig.set_figheight(10 * self.h / self.w)
		Q = ax.quiver(X, Y, U, V, color="red", headwidth=1, minlength=0, scale=1000)
		ax.imshow(L, cmap='hot', interpolation='spline36', alpha=0.5, origin="lower")
		
		anim = animate.FuncAnimation(fig, self.animation, fargs=(Q, spacestep, timestep), interval=100, blit=False)
		fig.tight_layout()
		plt.show()	
			
		
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
		
	def listXY(self, spacestep = 1) :
		
		X = np.zeros((math.ceil(self.w / spacestep) * math.ceil(self.h / spacestep)))
		Y = np.zeros((math.ceil(self.w / spacestep) * math.ceil(self.h / spacestep)))
		
		i = 0
	
		for x in range(0, self.w, spacestep) :
			
			for y in range(0, self.h, spacestep) :

				X[i] = x
				Y[i] = y
				
				i += 1
				
		return X, Y
		
	def listUV(self, spacestep = 1) :
		
		U = np.zeros((math.ceil(self.w / spacestep) * math.ceil(self.h / spacestep)))
		V = np.zeros((math.ceil(self.w / spacestep) * math.ceil(self.h / spacestep)))
		
		i = 0
	
		for x in range(0, self.w, spacestep) :
			
			for y in range(0, self.h, spacestep) :
				
				if not(np.isnan(self.table[x][y][0])) :

					U[i] = self.table[x][y][0]
					V[i] = self.table[x][y][1]
				
				i += 1
				
		return U, V
		
	def mapL(self) :
		
		L = np.zeros((self.h, self.w))
		
		i = 0
	
		for x in range(0, self.w) :
			
			for y in range(0, self.h) :

				L[y][x] = not(np.isnan(self.table[x][y][0]))
				
				i += 1
				
		return L
		
	def show(self, spacestep = 1) :
		
		X, Y = self.listXY(spacestep)
		U, V = self.listUV(spacestep)
		L = self.mapL()
		
		
		fig, ax = plt.subplots(1,1)
		fig.set_figwidth(10)
		fig.set_figheight(10 * self.h / self.w)
		Q = ax.quiver(X, Y, U, V, color="red", headwidth=1, minlength=0, scale=1000)
		ax.imshow(L, cmap='hot', interpolation='spline36', alpha=0.5, origin="lower")
		fig.tight_layout()
		plt.show()
		
class Wind :
	
	def __init__(self, x = 0, y = 0) :
		
		self.x = x
		self.y = y
		
	def __str__(self) :
		
		return "({:.1f},{:.1f})".format(self.x, self.y)

import math
import numpy as np
import pickle
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

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
		
	def show(self, timestep = 0.1, spacestep = 1, trajectory = [], csea = (29,162,216), cland = (77,107,83), cwind = (6,66,115), ctraj = (180,6,66)) :
		
		pygame.init()
		pygame_info = pygame.display.Info()
		dw = pygame_info.current_w
		dh = pygame_info.current_h
		
		f = math.floor(min(dw / self.w, dh / self.h))
		
		window = pygame.display.set_mode((f * self.w, f * self.h))
		
		trajectory = [(round(p[0] * f), round(p[1] * f)) for p in trajectory]
		
		running = True
		
		landmap = pygame.Surface((f * self.w, f * self.h))
		landmap.fill(csea)
		
		if len(trajectory) > 0 :
				
			pygame.draw.aalines(landmap, ctraj, False, trajectory)
		
		for x in range(0, self.w) :
			
			for y in range(0, self.h) :

				if np.isnan(self.table[0][x][y][0]) :
					
					pygame.draw.rect(landmap, cland, (f * x, f * y, f, f))
					
				else :
					
					if (x > 0 and x < self.w - 1 and y > 0 and y < self.h - 1 and np.isnan(self.table[0][x - 1][y][0]) and np.isnan(self.table[0][x + 1][y][0]) and np.isnan(self.table[0][x][y - 1][0]) and np.isnan(self.table[0][x][y + 1][0])) :
						
						pygame.draw.rect(landmap, cland, (f * x, f * y, f, f))
						
					else :
						
						
						if x > 0 and np.isnan(self.table[0][x - 1][y][0]) :
							
							if y > 0 and np.isnan(self.table[0][x][y - 1][0]) :
							
								pygame.draw.polygon(landmap, cland, ((f * x, f * y), (f * x, f * (y + 1) - 2), (f * (x + 1) - 2, f * y)))
								
							if y < self.h - 1 and np.isnan(self.table[0][x][y + 1][0]) :
							
								pygame.draw.polygon(landmap, cland, ((f * x, f * (y + 1)), (f * (x + 1) - 1, f * (y + 1)), (f * x, f * y + 1)))
								
						if x < self.w - 1 and np.isnan(self.table[0][x + 1][y][0]) :
							
							if y > 0 and np.isnan(self.table[0][x][y - 1][0]) :
							
								pygame.draw.polygon(landmap, cland, ((f * (x + 1), f * (y + 1) - 1), (f * (x + 1), f * y ), (f * x + 1, f * y)))
								
							if y < self.h - 1 and np.isnan(self.table[0][x][y + 1][0]) :
							
								pygame.draw.polygon(landmap, cland, ((f * (x + 1), f * y), (f * (x + 1), f * (y + 1)), (f * x, f * (y + 1))))
		
		step = 0
							
		while running :
			
			t = step * timestep
			
			if t > self.t - 1 :
				
				running = False
				
				break
			
			window.blit(landmap, (0, 0))

			events = pygame.event.get()
			
			for event in events :
					
				if (event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)) :
					running = False
			
			ws = self.windspace(t)
			
			for x in range(0, self.w, spacestep) :
			
				for y in range(0, self.h, spacestep) :

					if not(np.isnan(ws.table[x][y][0])) :
						
						ax = round(f * (x + 0.5))
						ay = round(f * (y + 0.5))
						
						bx = ax + round(f * ws.table[x][y][0] * 0.3)
						by = ay + round(f * ws.table[x][y][1] * 0.3)
						
						pygame.draw.aaline(window, cwind, (ax, ay), (bx, by))
						pygame.draw.line(window, cwind, (ax - 1, ay), (ax + 1, ay))
						pygame.draw.line(window, cwind, (ax, ay - 1), (ax, ay + 1))
				
			if len(trajectory) > step :
				
				pygame.draw.circle(window, ctraj, trajectory[step], 5)
		
			step += 1
		
			pygame.display.flip()
			
		pygame.quit()
			
		
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
		
	def show(self, spacestep = 1, trajectory = [], csea = (29,162,216), cland = (77,107,83), cwind = (6,66,115), ctraj = (180,6,66)) :
		
		pygame.init()
		pygame_info = pygame.display.Info()
		dw = pygame_info.current_w
		dh = pygame_info.current_h
		
		f = math.floor(min(dw / self.w, dh / self.h))
		
		window = pygame.display.set_mode((f * self.w, f * self.h))
		
		trajectory = [(round(p[0] * f), round(p[1] * f)) for p in trajectory]
		
		running = True
		
		landmap = pygame.Surface((f * self.w, f * self.h))
		landmap.fill(csea)
		
		if len(trajectory) > 0 :
				
			pygame.draw.aalines(landmap, ctraj, False, trajectory)
		
		for x in range(0, self.w) :
			
			for y in range(0, self.h) :

				if np.isnan(self.table[x][y][0]) :
					
					pygame.draw.rect(landmap, cland, (f * x, f * y, f, f))
					
				else :
					
					if (x > 0 and x < self.w - 1 and y > 0 and y < self.h - 1 and np.isnan(self.table[x - 1][y][0]) and np.isnan(self.table[x + 1][y][0]) and np.isnan(self.table[x][y - 1][0]) and np.isnan(self.table[x][y + 1][0])) :
						
						pygame.draw.rect(landmap, cland, (f * x, f * y, f, f))
						
					else :
						
						
						if x > 0 and np.isnan(self.table[x - 1][y][0]) :
							
							if y > 0 and np.isnan(self.table[x][y - 1][0]) :
							
								pygame.draw.polygon(landmap, cland, ((f * x, f * y), (f * x, f * (y + 1) - 2), (f * (x + 1) - 2, f * y)))
								
							if y < self.h - 1 and np.isnan(self.table[x][y + 1][0]) :
							
								pygame.draw.polygon(landmap, cland, ((f * x, f * (y + 1)), (f * (x + 1) - 1, f * (y + 1)), (f * x, f * y + 1)))
								
						if x < self.w - 1 and np.isnan(self.table[x + 1][y][0]) :
							
							if y > 0 and np.isnan(self.table[x][y - 1][0]) :
							
								pygame.draw.polygon(landmap, cland, ((f * (x + 1), f * (y + 1) - 1), (f * (x + 1), f * y ), (f * x + 1, f * y)))
								
							if y < self.h - 1 and np.isnan(self.table[x][y + 1][0]) :
							
								pygame.draw.polygon(landmap, cland, ((f * (x + 1), f * y), (f * (x + 1), f * (y + 1)), (f * x, f * (y + 1))))
							
		while running :
			
			window.blit(landmap, (0, 0))

			events = pygame.event.get()
			
			for event in events :
					
				if (event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)) :
					running = False
			
			for x in range(0, self.w, spacestep) :
				
				for y in range(0, self.h, spacestep) :

					if not(np.isnan(self.table[x][y][0])) :
						
						ax = round(f * (x + 0.5))
						ay = round(f * (y + 0.5))
						
						bx = ax + round(f * self.table[x][y][0] * 0.3)
						by = ay + round(f * self.table[x][y][1] * 0.3)
						
						pygame.draw.aaline(window, cwind, (ax, ay), (bx, by))
						pygame.draw.line(window, cwind, (ax - 1, ay), (ax + 1, ay))
						pygame.draw.line(window, cwind, (ax, ay - 1), (ax, ay + 1))

			pygame.display.flip()
			
		pygame.quit()
		
class Wind :
	
	def __init__(self, x = 0, y = 0) :
		
		self.x = x
		self.y = y
		
	def __str__(self) :
		
		return "({:.1f},{:.1f})".format(self.x, self.y)
		
if __name__ == "__main__" :
	
	import random

	wst = load("MediteraneanSea")
	traj = []
	x,y = (random.randrange(0, wst.w), random.randrange(0, wst.h))
	angle = 2 * random.random() * math.pi
	
	for i in range(10 * wst.t) :
		
		traj.append((x, y))
		
		x += math.cos(angle)
		y += math.sin(angle)
		
		if random.randrange(0, 10) == 0 :
		
			angle += random.random() * 2 * (random.random() - 0.5) * math.pi
		
	wst.show(0.1, 3, traj)

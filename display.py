import math
import numpy

from wind import WindSpaceTime, WindSpace
from route import Route
from geometry import Vector

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame



def showWindSpaceTime(wst, timestep = 0.1, spacestep = 1, route = None):
	#Display a run of the WindSpaceTime object with a route

	csea=(157, 219, 255)
	cland=(130, 167, 117)
	cwind=(59, 114, 124)
	ctraj=(100, 81, 59)
	cboat=(176, 95, 102)
	
	pygame.init()
	pygame_info = pygame.display.Info()
	dw = pygame_info.current_w
	dh = pygame_info.current_h
	
	f = math.floor(min(dw / wst.w, dh / wst.h))
	
	window = pygame.display.set_mode((f * wst.w, f * wst.h))
	
	running = True
	
	landmap = pygame.Surface((f * wst.w, f * wst.h))

	drawSea(landmap, csea)
	drawLands(landmap, wst.windspace(0), f, cland)
	drawPoints(landmap, wst.windspace(0), spacestep, f, cwind)
	drawRoute(landmap, route, f, ctraj)

	step = 0
	
	while running:
		
		t = step * timestep
		
		if t > wst.t - 1:
			step, t = 0, 0
		
		window.blit(landmap, (0, 0))
		
		events = pygame.event.get()
		
		for event in events:
			
			if (event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
				running = False

		drawWinds(window, wst.windspace(t), spacestep, f, cwind)

		drawBoat(window, route, step, f, cboat)
		
		step += 1
		
		pygame.display.flip()
	
	pygame.quit()

def showWindSpace(ws, spacestep = 1, route = None):
	#Display a run of the WindSpaceTime object with a route

	csea=(157, 219, 255)
	cland=(130, 167, 117)
	cwind=(59, 114, 124)
	ctraj=(100, 81, 59)
	cboat=(176, 95, 102)

	pygame.init()
	pygame_info = pygame.display.Info()
	dw = pygame_info.current_w
	dh = pygame_info.current_h
	
	f = math.floor(min(dw / wst.w, dh / wst.h))
	
	window = pygame.display.set_mode((f * wst.w, f * wst.h))
	
	running = True
	
	landmap = pygame.Surface((f * wst.w, f * wst.h))

	drawSea(landmap, csea)
	drawLands(landmap, wst.windspace(0), f, cland)
	drawPoints(landmap, wst.windspace(0), spacestep, f, cwind)
	drawRoute(landmap, route, f, ctraj)
	
	while running:
		
		window.blit(landmap, (0, 0))
		
		events = pygame.event.get()
		
		for event in events:
			
			if (event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
				running = False

		drawWinds(window, wst.windspace(t), spacestep, f, cwind)

		pygame.display.flip()
	
	pygame.quit()

def drawSea(surface, color) :
	#Draw the sea onto a pygame surface
	surface.fill(color)

def drawLands(surface, ws, f, color) :
	#Draw the lands onto a pygame surface

	for x in range(0, ws.w):
		
		for y in range(0, ws.h):
			
			if ws.land(x, y):
				
				pygame.draw.rect(surface, color, (f * x, f * y, f, f))
			
			else:
				
				if ((x <= 0        or ws.land(x - 1, y)) and
					(x >= ws.w - 1 or ws.land(x + 1, y)) and
					(y <= 0        or ws.land(x, y - 1)) and 
					(y >= ws.h - 1 or ws.land(x, y + 1))):
					
					pygame.draw.rect(surface, color, (f * x, f * y, f, f))
				
				else:
					
					if x > 0 and ws.land(x - 1, y):
						
						if y > 0 and ws.land(x, y - 1):
							pygame.draw.polygon(surface, color,
												((f * x, f * y), (f * x, f * (y + 1) - 2), (f * (x + 1) - 2, f * y)))
						
						if y < ws.h - 1 and ws.land(x, y + 1):
							pygame.draw.polygon(surface, color, (
							(f * x, f * (y + 1)), (f * (x + 1) - 1, f * (y + 1)), (f * x, f * y + 1)))
					
					if x < ws.w - 1 and ws.land(x + 1, y):
						
						if y > 0 and ws.land(x, y - 1):
							pygame.draw.polygon(surface, color, (
							(f * (x + 1), f * (y + 1) - 1), (f * (x + 1), f * y), (f * x + 1, f * y)))
						
						if y < ws.h - 1 and ws.land(x, y + 1):
							pygame.draw.polygon(surface, color, (
							(f * (x + 1), f * y), (f * (x + 1), f * (y + 1)), (f * x, f * (y + 1))))

def drawPoints(surface, ws, spacestep, f, color) :

	for x in range(0, ws.w, spacestep):
			
		for y in range(0, ws.h, spacestep):

			vect = ws.table[x][y]
			
			if not (numpy.isnan(vect[0])):

				ax = round(f * (x + 0.5))
				ay = round(f * (y + 0.5))
				
				bx = ax + round(f * vect[0] * 0.3)
				by = ay + round(f * vect[1] * 0.3)
				
				pygame.draw.line(surface, color, (ax - 1, ay), (ax + 1, ay))
				pygame.draw.line(surface, color, (ax, ay - 1), (ax, ay + 1))

def drawRoute(surface, route, f, color) :
	#Draw a route onto a pygame surface

	if len(route.trace) > 0:
		pygame.draw.aalines(surface, color, False, route.export(f))

def drawWinds(surface, ws, spacestep, f, color) :
	#Draw the winds onto a pygame surface

	for x in range(0, ws.w, spacestep):
			
		for y in range(0, ws.h, spacestep):

			vect = ws.table[x][y]
			
			if not (numpy.isnan(vect[0])):

				ax = round(f * (x + 0.5))
				ay = round(f * (y + 0.5))
				
				bx = ax + round(f * vect[0] * 0.3)
				by = ay + round(f * vect[1] * 0.3)
				
				pygame.draw.aaline(surface, color, (ax, ay), (bx, by))

def drawBoat(surface, route, step, f, color, r = 6) :
	#Draw a boat onto a pygame surface

	if step > len(route.moves) - 1:
		return

	vect = (route.moves[step] ** 0.5) * f * 8
	
	shyvect = vect.absed()
	
	if shyvect.x < shyvect.y :
		
		shyvect.swap()

	(shyvect + 2 * Vector(r + 1, r + 1)).ceiled().pair()
	
	C = numpy.zeros((shyvect + 2 * Vector(r + 1, r + 1)).ceiled().pair())
	
	for x in range(0, 2 * r) :
		
		for y in range(0, 2 * r) :
			
			d = math.sqrt((x - r) ** 2 + (y - r) ** 2)
			
			if d < r :
			
				C[x, y] = min(255, round(255 * (r - d)))
	
	Ox, Oy = r, r
	
	if shyvect.square() > r ** 2 :
		
		inv = 1 / (shyvect.square())
		
		slope = shyvect.slope()
		
		proj = math.sqrt(1 - shyvect.y ** 2 * inv)
		
		x = 0
				
		while x <= C.shape[0] - 1 :
		
			py = r + round(shyvect.y - (shyvect.x - (x - r)) * slope)
			
			y = min(C.shape[1] - 1, py + r)
			
			while True :
				
				t = 1 - ((x - r) * shyvect.x + (y - r) * shyvect.y) * inv
				
				if t <= 1 :
				
					d = proj * abs((x - r) * slope - (y - r))
				
					if (r - 1) * t >= d - 1 :
					
						C[x, y] = 255 - round((255 - C[x, y]) * max(0, d - (r - 1) * t))
						
						y -= 1
						
						continue
						
				if y < py :
						
					break
					
				else :
					
					y -= 1
					
					continue

			x += 1
		
		if abs(vect.x) < abs(vect.y) :
			
			C = numpy.transpose(C)
			
		if vect.x < 0 :
			
			C = numpy.flipud(C)
			
			Ox = C.shape[0] - 1 - r
			
		if vect.y < 0 :
			
			C = numpy.fliplr(C)
			
			Oy = C.shape[1] - 1 - r
		
	arrow = pygame.Surface((C.shape[0], C.shape[1])).convert_alpha()

	for x in range(C.shape[0]) :

		for y in range(C.shape[1]) :

			arrow.set_at((x, y), (color[0], color[1], color[2], C[x, y]))

	surface.blit(arrow, (route.trace[step].x * f - Ox, route.trace[step].y * f - Oy))
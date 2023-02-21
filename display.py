import math
import numpy
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from wind import WindSpaceTime, WindSpace
from route import Route


def show_wst(wst: WindSpaceTime, timestep=0.1, spacestep=1, route=None, csea=(157, 219, 255), cland=(130, 167, 117),
			 cwind=(59, 114, 124), cboat=(176, 95, 102)):
	
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
	drawRoute(landmap, route, f, cboat)

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


def show_ws(ws: WindSpace, spacestep=1, route=None, csea=(157, 219, 255), cland=(130, 167, 117),
			cwind=(59, 114, 124), cboat=(176, 95, 102)):
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
	drawRoute(landmap, route, f, cboat)
	
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
	surface.fill(color)

def drawLands(surface, ws : WindSpace, f, color) :

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

def drawRoute(surface, route : Route, f, color) :

	if len(route.trace) > 0:
		pygame.draw.aalines(surface, color, False, route.export(f))

def drawWinds(surface, ws : WindSpace, spacestep, f, color) :

	for x in range(0, ws.w, spacestep):
			
		for y in range(0, ws.h, spacestep):

			vect = ws.table[x][y]
			
			if not (numpy.isnan(vect[0])):

				ax = round(f * (x + 0.5))
				ay = round(f * (y + 0.5))
				
				bx = ax + round(f * vect[0] * 0.3)
				by = ay + round(f * vect[1] * 0.3)
				
				pygame.draw.aaline(surface, color, (ax, ay), (bx, by))
				pygame.draw.line(surface, color, (ax - 1, ay), (ax + 1, ay))
				pygame.draw.line(surface, color, (ax, ay - 1), (ax, ay + 1))

def drawBoat(surface, route : Route, step, f, color) :

	if len(route.trace) > step:
		point = route.trace[step]
		pygame.draw.circle(surface, color, (round(point.x * f), round(point.y * f)), 5)


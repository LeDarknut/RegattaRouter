import math
import numpy
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from wind import WindSpaceTime, WindSpace


def show_wst(wst: WindSpaceTime, timestep=0.1, spacestep=1, route=None, csea=(157, 219, 255), cland=(130, 167, 117),
			 cwind=(59, 114, 124), cboat=(176, 95, 102)):
	
	pygame.init()
	pygame_info = pygame.display.Info()
	dw = pygame_info.current_w
	dh = pygame_info.current_h
	
	f = math.floor(min(dw / wst.w, dh / wst.h))
	
	window = pygame.display.set_mode((f * wst.w, f * wst.h))
	
	if route is None:
		route = []
	else:
		route = route.round(f)
	
	running = True
	
	landmap = pygame.Surface((f * wst.w, f * wst.h))
	landmap.fill(csea)
	
	for x in range(0, wst.w):
		
		for y in range(0, wst.h):
			
			if wst.land(x, y):
				
				pygame.draw.rect(landmap, cland, (f * x, f * y, f, f))
			
			else:
				
				if ((x <= 0         or wst.land(x - 1, y)) and
					(x >= wst.w - 1 or wst.land(x + 1, y)) and
					(y <= 0         or wst.land(x, y - 1)) and 
					(y >= wst.h - 1 or wst.land(x, y + 1))):
					
					pygame.draw.rect(landmap, cland, (f * x, f * y, f, f))
				
				else:
					
					if x > 0 and wst.land(x - 1, y):
						
						if y > 0 and wst.land(x, y - 1):
							pygame.draw.polygon(landmap, cland,
												((f * x, f * y), (f * x, f * (y + 1) - 2), (f * (x + 1) - 2, f * y)))
						
						if y < wst.h - 1 and wst.land(x, y + 1):
							pygame.draw.polygon(landmap, cland, (
							(f * x, f * (y + 1)), (f * (x + 1) - 1, f * (y + 1)), (f * x, f * y + 1)))
					
					if x < wst.w - 1 and wst.land(x + 1, y):
						
						if y > 0 and wst.land(x, y - 1):
							pygame.draw.polygon(landmap, cland, (
							(f * (x + 1), f * (y + 1) - 1), (f * (x + 1), f * y), (f * x + 1, f * y)))
						
						if y < wst.h - 1 and wst.land(x, y + 1):
							pygame.draw.polygon(landmap, cland, (
							(f * (x + 1), f * y), (f * (x + 1), f * (y + 1)), (f * x, f * (y + 1))))
	
	if len(route) > 0:
		pygame.draw.aalines(landmap, cboat, False, route)

	step = 0
	
	while running:
		
		t = step * timestep
		
		if t > wst.t - 1:
			running = False
			
			break
		
		window.blit(landmap, (0, 0))
		
		events = pygame.event.get()
		
		for event in events:
			
			if (event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
				running = False
		
		ws = wst.windspace(t)
		
		for x in range(0, wst.w, spacestep):
			
			for y in range(0, wst.h, spacestep):
				
				if not (wst.land(x, y)):
					ax = round(f * (x + 0.5))
					ay = round(f * (y + 0.5))
					
					bx = ax + round(f * ws.table[x][y][0] * 0.3)
					by = ay + round(f * ws.table[x][y][1] * 0.3)
					
					pygame.draw.aaline(window, cwind, (ax, ay), (bx, by))
					pygame.draw.line(window, cwind, (ax - 1, ay), (ax + 1, ay))
					pygame.draw.line(window, cwind, (ax, ay - 1), (ax, ay + 1))
		
		if len(route) > step:
			pygame.draw.circle(window, cboat, route[step], 5)
		
		step += 1
		
		pygame.display.flip()
	
	pygame.quit()


def show_ws(ws: WindSpace, spacestep=1, route=None, csea=(157, 219, 255), cland=(130, 167, 117),
			cwind=(59, 114, 124), cboat=(176, 95, 102)):
	pygame.init()
	pygame_info = pygame.display.Info()
	dw = pygame_info.current_w
	dh = pygame_info.current_h
	
	f = math.floor(min(dw / ws.w, dh / ws.h))
	
	window = pygame.display.set_mode((f * ws.w, f * ws.h))

	if route is None:
		route = []
	else:
		route = route.round(f)
	
	running = True
	
	landmap = pygame.Surface((f * ws.w, f * ws.h))
	landmap.fill(csea)
	
	if len(route) > 0:
		pygame.draw.aalines(landmap, cboat, False, route)
	
	for x in range(0, ws.w):
		
		for y in range(0, ws.h):
			
			if numpy.isnan(ws.table[x][y][0]):
				
				pygame.draw.rect(landmap, cland, (f * x, f * y, f, f))
			
			else:
				
				if ((x <= 0         or numpy.isnan(ws.table[x - 1][y][0])) and
                    (x >= wst.w - 1 or numpy.isnan(ws.table[x + 1][y][0])) and
                    (y <= 0         or numpy.isnan(ws.table[x][y - 1][0])) and 
                    (y >= wst.h - 1 or numpy.isnan(ws.table[x][y + 1][0]))):
					
					pygame.draw.rect(landmap, cland, (f * x, f * y, f, f))
				
				else:
					
					if x > 0 and numpy.isnan(ws.table[x - 1][y][0]):
						
						if y > 0 and numpy.isnan(ws.table[x][y - 1][0]):
							pygame.draw.polygon(landmap, cland,
												((f * x, f * y), (f * x, f * (y + 1) - 2), (f * (x + 1) - 2, f * y)))
						
						if y < ws.h - 1 and numpy.isnan(ws.table[x][y + 1][0]):
							pygame.draw.polygon(landmap, cland, (
							(f * x, f * (y + 1)), (f * (x + 1) - 1, f * (y + 1)), (f * x, f * y + 1)))
					
					if x < ws.w - 1 and numpy.isnan(ws.table[x + 1][y][0]):
						
						if y > 0 and numpy.isnan(ws.table[x][y - 1][0]):
							pygame.draw.polygon(landmap, cland, (
							(f * (x + 1), f * (y + 1) - 1), (f * (x + 1), f * y), (f * x + 1, f * y)))
						
						if y < ws.h - 1 and numpy.isnan(ws.table[x][y + 1][0]):
							pygame.draw.polygon(landmap, cland, (
							(f * (x + 1), f * y), (f * (x + 1), f * (y + 1)), (f * x, f * (y + 1))))
	
	while running:
		
		window.blit(landmap, (0, 0))
		
		events = pygame.event.get()
		
		for event in events:
			
			if (event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
				running = False
		
		for x in range(0, ws.w, spacestep):
			
			for y in range(0, ws.h, spacestep):
				
				if not (numpy.isnan(ws.table[x][y][0])):
					ax = round(f * (x + 0.5))
					ay = round(f * (y + 0.5))
					
					bx = ax + round(f * ws.table[x][y][0] * 0.3)
					by = ay + round(f * ws.table[x][y][1] * 0.3)
					
					pygame.draw.aaline(window, cwind, (ax, ay), (bx, by))
					pygame.draw.line(window, cwind, (ax - 1, ay), (ax + 1, ay))
					pygame.draw.line(window, cwind, (ax, ay - 1), (ax, ay + 1))
		
		pygame.display.flip()
	
	pygame.quit()
import math
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import numpy

def arrow(pu, pv) :
	
	u, v = abs(pu), abs (pv)
	
	if u < v :
		
		u, v = v, u
	
	C = numpy.zeros((math.ceil(u + 3.5), math.ceil(v + 3.5)))
	
	C[2][2] = 255
	C[1][2] = 255
	C[2][1] = 255
	C[3][2] = 255
	C[2][3] = 255
	C[1][1] = 178
	C[1][3] = 178
	C[3][3] = 178
	C[3][1] = 178
	
	Ox, Oy = 2, 2
	
	if u ** 2 + v ** 2 > 4 :
		
		inv = 1 / (u ** 2 + v ** 2)
		
		slope = v/u
		
		proj = math.sqrt(1 - v ** 2 * inv)
		
		x = 2
		
		while x <= C.shape[0] - 1 :
		
			py = 2 + round(v - (u - (x - 2)) * slope)
			
			y = py
			
			while True :
				
				if y > C.shape[1] - 1 :
					
					break
				
				t = 1 - ((x - 2) * u + (y - 2) * v) * inv
				
				if t > 1 :
					
					break
				
				d = proj * abs((x - 2) * slope - (y - 2))
				
				if t < d - 1 :
					
					break
					
				C[x, y] = 255 - round((255 - C[x, y]) * max(0, d - t))
						
				y += 1
				
			y = py - 1
			
			while True :
				
				t = 1 - ((x - 2) * u + (y - 2) * v) * inv
				
				if t > 1 :
					
					break
				
				d = proj * abs((x - 2) * slope - (y - 2))
				
				if t < d - 1 :
					
					break
					
				C[x, y] = 255 - round((255 - C[x, y]) * max(0, d - t))
				
				y -= 1
			
			x += 1
		
		if abs(pu) < abs(pv) :
			
			C = numpy.transpose(C)
			
		if pu < 0 :
			
			C = numpy.flipud(C)
			
			Ox = C.shape[0] - 3
			
		if pv < 0 :
			
			C = numpy.fliplr(C)
			
			Oy = C.shape[1] - 3
		
	return C, (Ox, Oy)
	

pygame.init()
pygame_info = pygame.display.Info()
dw = pygame_info.current_w
dh = pygame_info.current_h

cx, cy = round(dw / 2), round(dh / 2)

window = pygame.display.set_mode((dw, dh))

running = True
cl = pygame.time.Clock()

while running :
			
	window.fill(0)

	events = pygame.event.get()
	
	for event in events :
			
		if (event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)) :
			running = False
			
	mx, my = pygame.mouse.get_pos()
	
	u, v = mx - cx, my - cy
	
	C, O = arrow(u, v)
	
	for x in range(C.shape[0]) :
		
		for y in range(C.shape[1]) :
			
			window.set_at((cx + (x - O[0]), cy + (y - O[1])), (C[x][y], 0, 0))

	cl.tick(30)
	pygame.display.flip()
	
pygame.quit()
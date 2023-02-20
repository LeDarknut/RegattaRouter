import math
import numpy as np
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from wind import WindSpaceTime, WindSpace


def show_wst(wst: WindSpaceTime, timestep=0.1, spacestep=1, trajectory=None, csea=(29, 162, 216), cland=(77, 107, 83),
             cwind=(6, 66, 115), ctraj=(180, 6, 66)):
    pygame.init()
    pygame_info = pygame.display.Info()
    dw = pygame_info.current_w
    dh = pygame_info.current_h
    
    f = math.floor(min(dw / wst.w, dh / wst.h))
    
    window = pygame.display.set_mode((f * wst.w, f * wst.h))
    
    if trajectory is None:
        trajectory = []
    else:
        trajectory = trajectory.round(f)
    
    running = True
    
    landmap = pygame.Surface((f * wst.w, f * wst.h))
    landmap.fill(csea)
    
    if len(trajectory) > 0:
        pygame.draw.aalines(landmap, ctraj, False, trajectory)
    
    for x in range(0, wst.w):
        
        for y in range(0, wst.h):
            
            if np.isnan(wst.table[0][x][y][0]):
                
                pygame.draw.rect(landmap, cland, (f * x, f * y, f, f))
            
            else:
                
                if (x > 0 and x < wst.w - 1 and y > 0 and y < wst.h - 1 and np.isnan(
                        wst.table[0][x - 1][y][0]) and np.isnan(wst.table[0][x + 1][y][0]) and np.isnan(
                        wst.table[0][x][y - 1][0]) and np.isnan(wst.table[0][x][y + 1][0])):
                    
                    pygame.draw.rect(landmap, cland, (f * x, f * y, f, f))
                
                else:
                    
                    if x > 0 and np.isnan(wst.table[0][x - 1][y][0]):
                        
                        if y > 0 and np.isnan(wst.table[0][x][y - 1][0]):
                            pygame.draw.polygon(landmap, cland,
                                                ((f * x, f * y), (f * x, f * (y + 1) - 2), (f * (x + 1) - 2, f * y)))
                        
                        if y < wst.h - 1 and np.isnan(wst.table[0][x][y + 1][0]):
                            pygame.draw.polygon(landmap, cland, (
                            (f * x, f * (y + 1)), (f * (x + 1) - 1, f * (y + 1)), (f * x, f * y + 1)))
                    
                    if x < wst.w - 1 and np.isnan(wst.table[0][x + 1][y][0]):
                        
                        if y > 0 and np.isnan(wst.table[0][x][y - 1][0]):
                            pygame.draw.polygon(landmap, cland, (
                            (f * (x + 1), f * (y + 1) - 1), (f * (x + 1), f * y), (f * x + 1, f * y)))
                        
                        if y < wst.h - 1 and np.isnan(wst.table[0][x][y + 1][0]):
                            pygame.draw.polygon(landmap, cland, (
                            (f * (x + 1), f * y), (f * (x + 1), f * (y + 1)), (f * x, f * (y + 1))))
    
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
                
                if not (np.isnan(ws.table[x][y][0])):
                    ax = round(f * (x + 0.5))
                    ay = round(f * (y + 0.5))
                    
                    bx = ax + round(f * ws.table[x][y][0] * 0.3)
                    by = ay + round(f * ws.table[x][y][1] * 0.3)
                    
                    pygame.draw.aaline(window, cwind, (ax, ay), (bx, by))
                    pygame.draw.line(window, cwind, (ax - 1, ay), (ax + 1, ay))
                    pygame.draw.line(window, cwind, (ax, ay - 1), (ax, ay + 1))
        
        if len(trajectory) > step:
            pygame.draw.circle(window, ctraj, trajectory[step], 5)
        
        step += 1
        
        pygame.display.flip()
    
    pygame.quit()


def show_ws(ws: WindSpace, spacestep=1, trajectory=None, csea=(29, 162, 216), cland=(77, 107, 83), cwind=(6, 66, 115),
         ctraj=(180, 6, 66)):
    pygame.init()
    pygame_info = pygame.display.Info()
    dw = pygame_info.current_w
    dh = pygame_info.current_h
    
    f = math.floor(min(dw / ws.w, dh / ws.h))
    
    window = pygame.display.set_mode((f * ws.w, f * ws.h))

    if trajectory is None:
        trajectory = []
    else:
        trajectory = trajectory.round(f)
    
    running = True
    
    landmap = pygame.Surface((f * ws.w, f * ws.h))
    landmap.fill(csea)
    
    if len(trajectory) > 0:
        pygame.draw.aalines(landmap, ctraj, False, trajectory)
    
    for x in range(0, ws.w):
        
        for y in range(0, ws.h):
            
            if np.isnan(ws.table[x][y][0]):
                
                pygame.draw.rect(landmap, cland, (f * x, f * y, f, f))
            
            else:
                
                if (x > 0 and x < ws.w - 1 and y > 0 and y < ws.h - 1 and np.isnan(
                        ws.table[x - 1][y][0]) and np.isnan(ws.table[x + 1][y][0]) and np.isnan(
                        ws.table[x][y - 1][0]) and np.isnan(ws.table[x][y + 1][0])):
                    
                    pygame.draw.rect(landmap, cland, (f * x, f * y, f, f))
                
                else:
                    
                    if x > 0 and np.isnan(ws.table[x - 1][y][0]):
                        
                        if y > 0 and np.isnan(ws.table[x][y - 1][0]):
                            pygame.draw.polygon(landmap, cland,
                                                ((f * x, f * y), (f * x, f * (y + 1) - 2), (f * (x + 1) - 2, f * y)))
                        
                        if y < ws.h - 1 and np.isnan(ws.table[x][y + 1][0]):
                            pygame.draw.polygon(landmap, cland, (
                            (f * x, f * (y + 1)), (f * (x + 1) - 1, f * (y + 1)), (f * x, f * y + 1)))
                    
                    if x < ws.w - 1 and np.isnan(ws.table[x + 1][y][0]):
                        
                        if y > 0 and np.isnan(ws.table[x][y - 1][0]):
                            pygame.draw.polygon(landmap, cland, (
                            (f * (x + 1), f * (y + 1) - 1), (f * (x + 1), f * y), (f * x + 1, f * y)))
                        
                        if y < ws.h - 1 and np.isnan(ws.table[x][y + 1][0]):
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
                
                if not (np.isnan(ws.table[x][y][0])):
                    ax = round(f * (x + 0.5))
                    ay = round(f * (y + 0.5))
                    
                    bx = ax + round(f * ws.table[x][y][0] * 0.3)
                    by = ay + round(f * ws.table[x][y][1] * 0.3)
                    
                    pygame.draw.aaline(window, cwind, (ax, ay), (bx, by))
                    pygame.draw.line(window, cwind, (ax - 1, ay), (ax + 1, ay))
                    pygame.draw.line(window, cwind, (ax, ay - 1), (ax, ay + 1))
        
        pygame.display.flip()
    
    pygame.quit()
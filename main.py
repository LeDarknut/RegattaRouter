import math
import random
import wind
from display import show_wst
from route import Route

wst = wind.load("MediteraneanSea")
route = Route((random.randrange(0, wst.w), random.randrange(0, wst.h)))
angle = 2 * random.random() * math.pi

for i in range(10 * wst.t):
    
    route.add_point(angle)
    
    if random.randrange(0, 10) == 0:
        angle += random.random() * 2 * (random.random() - 0.5) * math.pi

show_wst(wst, 0.05, 3, route)

import math
import random
from geometry import Vector, Point
from wind import *
from display import showWindSpaceTime
from route import Route

wst = WindSpaceTime.fromFile("MediteraneanSea")
route = Route(Point(random.randrange(0, wst.w), random.randrange(0, wst.h)))
angle = 2 * random.random() * math.pi

for i in range(10 * wst.t):
    
    route.move(Vector(math.cos(angle), math.sin(angle)))
    
    if random.randrange(0, 10) == 0:
        angle += random.random() * 2 * (random.random() - 0.5) * math.pi

showWindSpaceTime(wst, 0.05, 3, route)

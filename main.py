import math
import random
from geometry import Vector
from wind import *
from display import showWindSpaceTime
from route import Route

wst = WindSpaceTime.fromFile("Sargasso")
route = Route(Vector.fromRandom(wst.w, wst.h))
angle = 2 * random.random() * math.pi
speed = 1

timediv = 10
spacediv = 2

for i in range(timediv * wst.t):
    
    route.move(Vector.fromAngle(angle, speed / spacediv))
    
    if random.randrange(0, 5) == 0:
        angle += random.random() * (random.random() - 0.5) * math.pi
        speed += random.random() * (random.random() - 0.5)

showWindSpaceTime(wst, 1 / timediv, 3, route)

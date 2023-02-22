import math
import random
from geometry import Vector
from wind import *
from display import showWindSpaceTime
from route import Route

wst = WindSpaceTime.fromFile("Sargasso")
route = Route(Vector(wst.w // 3, wst.h // 3) + Vector.fromRandom(wst.w // 4, wst.h // 4))
angle = 2 * random.random() * math.pi
speed = 1

timediv = 10
spacediv = 2

t = 0

for i in range(timediv * wst.t):

    pos = route.current()

    pos.x = min(wst.w - 1, max(0, pos.x))
    pos.y = min(wst.h - 1, max(0, pos.y))

    if wst.land(pos.x, pos.y) :

        route.move(Vector(0, 0))

    else :

        route.move(wst.wind(t, pos.x, pos.y) * 0.05)

    t = min(t + 1 / timediv, wst.t - 1)

showWindSpaceTime(wst, 1 / timediv, 3, route)

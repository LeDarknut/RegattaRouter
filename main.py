import math
import random

from display import showWindSpaceTime, showWindSpace
from wind import WindSpaceTime, WindSpace
from route import Route
from geometry import Vector, rad, deg
from boat import Boat

timeunit = 21600    #6h in seconds
spaceunit = 27830   #0.25° of the earth in meters

wst = WindSpaceTime.fromFile("Sargasso")
boat = Boat.fromFile("Imoca60")
timediv = 10

start = Vector(100, 150)
goal = Vector(150, 10)

route = Route(start)

def downwind(route) :

	t = 0

	for i in range(timediv * wst.t - 1):

		pos = route.current()

		if wst.land(pos.x, pos.y) or wst.wind(t, pos.x, pos.y) == Vector(0, 0) :

			route.move(Vector(0, 0))

		else :

			wind = wst.wind(t, pos.x, pos.y)

			sail = boat.sail(wind, wind) * (timeunit / timediv) / spaceunit

			if not route.peek(sail).inrange(0, wst.w - 1, 0, wst.h - 1) :

				route.move(Vector(0, 0))

			else :

				route.move(sail)

		t = min(t + 1 / timediv, wst.t - 1)

def perpendicular(route) :

	t = 0

	for i in range(timediv * wst.t - 1):

		pos = route.current()

		if wst.land(pos.x, pos.y) or wst.wind(t, pos.x, pos.y) == Vector(0, 0) :

			route.move(Vector(0, 0))

		else :

			wind = wst.wind(t, pos.x, pos.y)

			sail = boat.sail(wind.rotated(rad(90)), wind) * (timeunit / timediv) / spaceunit

			if not route.peek(sail).inrange(0, wst.w - 1, 0, wst.h - 1) :

				route.move(Vector(0, 0))

			else :

				route.move(sail)

		t = min(t + 1 / timediv, wst.t - 1)

def fastest(route) :

	t = 0

	bord = 0

	for i in range(timediv * wst.t - 1):

		pos = route.current()

		if wst.land(pos.x, pos.y) or wst.wind(t, pos.x, pos.y) == Vector(0, 0) :

			route.move(Vector(0, 0))

		else :

			wind = wst.wind(t, pos.x, pos.y)

			maxSpeed = 0
			maxAngle = 0

			for angle in range(0, 180, 5) :

				speed = boat.speed(Vector.fromAngle(rad(bord + angle)), wind)

				if speed <= maxSpeed :

					continue

				dest = route.peek(boat.sail(Vector.fromAngle(rad(bord + angle)), wind) * (timeunit / timediv) / spaceunit)

				if (not dest.inrange(0, wst.w - 1, 0, wst.h - 1)) or wst.land(dest.x, dest.y) :

					continue

				maxSpeed = speed
				maxAngle = bord + angle

			if maxSpeed < 0.2 :

				bord += 180

			sail = boat.sail(Vector.fromAngle(rad(maxAngle)), wind) * (timeunit / timediv) / spaceunit

			if not route.peek(sail).inrange(0, wst.w - 1, 0, wst.h - 1) :

				route.move(Vector(0, 0))

			else :

				route.move(sail)

		t = min(t + 1 / timediv, wst.t - 1)

def greedy(route) :

	t = 0

	for i in range(timediv * wst.t - 1):

		pos = route.current()

		direction = goal - pos

		if direction.norm() < 1 :

			break

		if wst.land(pos.x, pos.y) or wst.wind(t, pos.x, pos.y) == Vector(0, 0) :

			route.move(Vector(0, 0))

		else :

			wind = wst.wind(t, pos.x, pos.y)

			maxSpeed = 0
			maxAngle = 0

			for angle in range(-80, 80, 1) :

				sail = boat.sail(direction.rotated(rad(angle)), wind) * (timeunit / timediv) / spaceunit

				speed = sail | direction

				if speed <= maxSpeed :

					continue

				dest = route.peek(sail)

				if (not dest.inrange(0, wst.w - 1, 0, wst.h - 1)) or wst.land(dest.x, dest.y) :

					continue

				maxSpeed = speed
				maxAngle = angle

			sail = boat.sail(direction.rotated(rad(maxAngle)), wind) * (timeunit / timediv) / spaceunit

			if not route.peek(sail).inrange(0, wst.w - 1, 0, wst.h - 1) :

				route.move(Vector(0, 0))

			else :

				route.move(sail)

		t = min(t + 1 / timediv, wst.t - 1)

greedy(route)

showWindSpaceTime(wst, 1 / timediv, 3, route)

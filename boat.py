import math
import numpy
import pickle

from geometry import Vector

class Boat :

	#Boat object : Compute wind interaction

	#r : the number of wind speed data points
	#s : the step between each wind speed point
	#table : the data

	def __init__(self, windrange, windstep, table = None) :

		self.r = windrange
		self.s = windstep
		if table is None :
			table = numpy.zeros((181, self.r))
		self.table = table

	@classmethod
	def fromFile(cls, filename) :
		#Get Polar compiled

		table = pickle.load(open("data/bin/polar/{0}.bin".format(filename), "rb"))

		return cls(table.shape[1], 0.5144, table)

	def speed(self, direction, wind) :

		a = 180 * (1 - math.acos(wind ^ direction) / math.pi)
		m = wind.norm()

		m /= self.s

		assert m >= 0         , "negative windspeed"

		if m > self.r - 1 :
			m = self.r - 1

		while a < -180 :
			a += 360
		while a > 180 :
			a -= 360

		a = abs(a)

		fa = math.floor(a)
		ca = math.ceil(a)
		da = a - fa

		fm = math.floor(m)
		cm = math.ceil(m)
		dm = m - fm

		lerpfa = (1-dm) * self.table[fa][fm] + dm * self.table[fa][cm]
		lerpca = (1-dm) * self.table[ca][fm] + dm * self.table[ca][cm]

		return (1-da) * lerpfa + da * lerpca


	def sail(self, direction, wind) :
		return direction % self.speed(direction, wind)
import json
import numpy
import pickle

polar = numpy.zeros((181, 71))

with open("polar/imoca60.csv", "r") as csv :

	for line in csv.readlines() :
		
		line = line.split(",")
		
		windspeed = int(line[0][1:-1])
		angle = int(line[2][1:-1])
		speed = float(line[3][1:-2]) * 0.5144
		
		if speed > polar[angle][windspeed] :
			
			polar[angle][windspeed] = speed
			
pickle.dump(polar, open("bin/polar/imoca60.bin", "wb"))
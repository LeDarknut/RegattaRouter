import os
import pickle
import wind

def comp(name) :
	
	v = os.popen("wgrib2 subgrib/{0}/land.grb -grid".format(name)).read().split("\n")
	
	dim = v[1][v[1].index("(") + 1:v[1].index(")")].split(" x ")
	
	w = int(dim[0])
	h = int(dim[1])
	
	W = int(v[3].split(".")[0].split(" ")[-1])
	E = int(v[3].split(".")[1].split(" ")[-1])
	S = int(v[2].split(".")[0].split(" ")[-1])
	N = int(v[2].split(".")[1].split(" ")[-1])

	files = sorted(os.listdir("subgrib/{0}".format(name)))[:-1]

	L = wind.np.zeros((w, h))

	os.popen("wgrib2 subgrib/{0}/land.grb -csv land.csv".format(name)).read()

	with open("land.csv", "r") as csv :
		
		for line in csv.readlines() :
			
			field = line.split(",")
			
			lon = round((((float(field[4]) + 360) % 360) - W) * 4)
			lat = round((((float(field[5]) + 360) % 360) - S) * 4)
			val = float(field[6])
			L[lon][lat] = val
			
				
	os.unlink("land.csv")

	wst = wind.WindSpaceTime(len(files), w, h)

	for t,f in enumerate(files) :
			
		os.popen("wgrib2 subgrib/{0}/{1} -csv wind.csv".format(name, f)).read()

		with open("wind.csv", "r") as csv :
			
			for line in csv.readlines() :
				
				field = line.split(",")
			
				n = field[2][1]
				lon = round((float(field[4]) + 360 - W) % 360 * 4)
				lat = round((float(field[5]) + 360 - S) % 360 * 4)
				val = float(field[6])
				
				if n == "U" :
					
					if L[lon][lat] > 0.5 :
						
						wst.table[t][lon][lat][0] = wind.np.nan
						
					else :
					
						wst.table[t][lon][lat][0] = val
					
				elif n == "V" :
					
					if L[lon][lat] > 0.5 :
						
						wst.table[t][lon][lat][1] = wind.np.nan
						
					else :
					
						wst.table[t][lon][lat][1] = val
		
		print(f[:-4])
			
	pickle.dump(wst, open("wst/{0}.bin".format(name), "wb"))
	
	os.unlink("wind.csv")

if __name__ == "__main__" :
	
	comp("Sargasso")
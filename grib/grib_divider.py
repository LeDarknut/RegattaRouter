import os
from datetime import datetime

def divide(name, T0, T1, W, E, S, N) :
	
	assert E > W, "Longitude range is negative"
	assert N > S, "Latitude range is negative"
	
	while W < 0 :
		
		W += 360
		E += 360
	
	T0 = T0.strftime("%Y_%m_%d_%H")
	T1 = T1.strftime("%Y_%m_%d_%H")

	files = ["land"] + sorted([n[:-4] for n in os.listdir("grib") if T0 <= n and T1 >= n and n != "land.grb"])
		
	if not(os.path.exists("subgrib/" + name)) :

		os.mkdir("subgrib/" + name)

	for f in files :
			
		os.popen("wgrib2 grib/{0}.grb -small_grib {1}:{2} {3}:{4} subgrib/{5}/{0}.grb".format(f, W, E, S, N, name)).read()
		
		print(f)
		
	return name
		
if __name__ == "__main__" :
	
	divide("MediteraneanSea", datetime.strptime("2023/01/01", "%Y/%m/%d"), datetime.now(), -12, 41, 26, 48)
	
	
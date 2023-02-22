import requests
import bs4

def get(url) :
	
	req = requests.get(url)
	
	bs = bs4.BeautifulSoup(req.content.decode('utf-8'), 'html.parser')
	
	return bs

for day in get("https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl").find_all("tr")[::-1] :

	gfs = day.find("a", href=True).decode_contents()[4:]
	
	for hour in get("https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?dir=%2Fgfs.{0}".format(gfs)).find_all("tr")[::-1] :
		
		time = hour.find("a", href=True).decode_contents()

		req = requests.get("https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?dir=%2Fgfs.{0}%2F{1}%2Fatmos&file=gfs.t{1}z.pgrb2.0p25.f000&lev_10_m_above_ground=on&var_UGRD=on&var_VGRD=on&leftlon=0&rightlon=360&toplat=90&bottomlat=-90".format(gfs, time))

		with open("wind/global/{0}_{1}_{2}_{3}.grb".format(gfs[0:4], gfs[4:6], gfs[6:8], time), "wb") as f :
		
			f.write(req.content)
			
		print("{0}_{1}_{2}_{3}".format(gfs[0:4], gfs[4:6], gfs[6:8], time))
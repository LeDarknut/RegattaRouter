import requests
import json

year = 2016

def get(url) :
	
	req = requests.get(url)
	
	data = json.loads(req.content.decode('utf-8'))
	
	return data
	
for boat in get("https://jieter.github.io/orc-data/site/index.json") :
	
	if boat[0][:3] != "FRA" :
		continue
	
	try :
	
		data = get("https://jieter.github.io/orc-data/site/data/{0}.json".format(boat[0]))
		
	except :
		
		continue
		
	name = data["sailnumber"][data["sailnumber"].index("/") + 1:]
	
	polar = data["vpp"]
	del polar["beat_angle"]
	del polar["beat_vmg"]
	del polar["run_angle"]
	del polar["run_vmg"]
	del polar["speeds"]
	
	with open("polar/{0}.json".format(name), "w") as f :
		
		f.write(json.dumps(polar))
		
	print(name)
		
	
import utils
import json
import time
import os
import sys
def benchmark(algo):
	minersfile = open("miners.txt", "r")
	configfile = open("config_example.json", "r")
	appdatafile = open("appdata.json", "rw+")
	appdata = appdatafile.read()
	if not appdata:
		appdata = {}
	config = json.load(configfile.read())
	miners = json.load(minersfile.read())
	for algo in miners["supported-algos"]:
		best = ["", 0]
		for miner in miners["supported-algos"][algo]:
			if miners["miners"][miner]["api"]:
				utils.startminer(miner, miners["miners"][miner]["start"], algo, config)
				time.sleep(300)
				hashrate = utils.apiHashrate(miner)[0]
				if hashrate > best[1]:
					best[1] = hashrate
					best[0] = miner
				if sys.platform.startswith("win"):
					os.system("Taskkill /IM " + miner + ".exe /F")
				else:
					os.system("pkill " + miner)
			else:
				if algo in miners["miners"][miner]["best"]:
					best = [miner, 99999999]
		appdata["benchmark-data"][algo] = best
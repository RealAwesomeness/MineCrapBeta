import requests
import benchmark
import json
import os
import sys
import time
from pathlib import Path
def main():
    appdatafile = open("appdata.txt", "rw+")
    minersfile = open("miners.txt", "r")
    try:
        print("Loading config...")
        configfile = open("config.txt", "r")
    except:
        print("FATAL ERROR : Unable to open config! Try to create a config based on the example which is named ccnfig_example.txt.")
        quit
    config = json.loads(configfile.read())
    miners = json.loads(minersfile.read())
    if appdatafile.read() == "" or "--benchmark" in sys.argv: #check for first run or requested rebenchmark
        appdata = {}
        print("Benchmarking algos...")
        for algo in minerjson["supported-algos"]:
			result = benchmark.benchmark(algo) #benchmark an algo if it is supported
			appdata["benchmark-data"]["hashrate"][algo] = result["hashrate"]
			appdata["benchmark-data"]["power"][algo] = result["power"]
        appdatafile.write(json.dumps(appdata))
    appdata = json.loads(appdatafile.read())
    print("Getting the best profit miner...")
    best = requests.post("minecrap.dankepool.org", data = {appdata["benchmark-data"]})
	appdatafile.close()
	minersfile.close()
	configfile.close()
	miner = appdata["benchmark-data"][best]["miner"]
	if sys.platform.startswith("win"):
		
	else:
		startminer(miner, miners[miner]["start"], best, config) #passes the miner, start line syntax, the algo to use (will be able to use coin soon™), and the config
		while True:
			tmp = os.popen("ps -Af").read()
			if appdata["benchmark-data"]["miner"] not in tmp[:]:
				print("Miner crashed! Restarting...")
				startminer(miner, miners[miner]["start"], best, config)
			else:
				print(getStats(miner))
			time.sleep(5)
def startminer(miner, start, algo, config) :
	start = start.replace("ALGO", algo)
	start = start.replace("ADDRESS", config[algo]["address"])
	start = start.replace("POOL", config[algo]["pool"])
	start = start.replace("PORT", config[algo]["port"]
	if sys.platform.startswith("win"):
		start = miner + "\\" + miner + ".exe" + start
	else:
		start = "./" + miner + "/" + miner + start
	os.system(start)
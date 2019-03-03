import requests
import benchmark
import json
import os
import sys
import time
from pathlib import Path
import utils
import subprocess
import requests
def main():
    appdatafile = open("appdata.json", "rw+")
    minersfile = open("miners.json", "rw+")
    try:
        print("Loading config...")
        configfile = open("config.json", "r")
    except:
        utils.createconfig()
    config = json.loads(configfile.read())
    miners = json.loads(minersfile.read())
    if appdatafile.read() == "" or "--benchmark" in sys.argv: #check for first run or requested rebenchmark
        appdata = {}
        print("Benchmarking algos...")
        for algo in miners["supported-algos"]:
			result = benchmark.benchmark(algo) #benchmark an algo if it is supported
			appdata["benchmark-data"]["hashrate"][algo] = result["hashrate"]
			appdata["benchmark-data"]["power"][algo] = result["power"]
        appdatafile.write(json.dumps(appdata))
    appdata = json.loads(appdatafile.read())
	supportedalgos = []
	for algo in miners["supported-algos"]:
		supportedalgos.append(algo)
    print("Getting the best profit miner...")
    best = requests.post("minecrap.dankepool.org", data = json.dumps({appdata["benchmark-data"]}))
	bestalgo = ""
	found = False
	for algo in best:
		if algo in supportalgos and not found:
			bestalgo = algo
			found = True
	appdatafile.close()
	minersfile.close()
	configfile.close()
	miner = appdata["benchmark-data"][best][0]
	if sys.platform.startswith("win"):
		utils.startminer(miner, miners["miners"][miner]["start"])
		while True:
			s = subprocess.check_output('tasklist', shell=True)
			if appdata["benchmark-data"][best]["miner"] not in s:
				print("Miner crashed! Restarting...")
				utils.startminer(miner, miners["miners"][miner]["start"], best, config)
			else:
				print(getStats(miner))
			time.sleep(5)
	else:
		utils.startminer(miner, miners[miner]["start"], best, config) #passes the miner, start line syntax, the algo to use (will be able to use coin soon™), and the config
		while True:
			tmp = os.popen("ps -Af").read()
			if appdata["benchmark-data"][best]["miner"] not in tmp:
				print("Miner crashed! Restarting...")
				utils.startminer(miner, miners["miners"][miner]["start"], best, config)
			else:
				print(getStats(miner))
			time.sleep(5)

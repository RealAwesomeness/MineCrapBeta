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
    appdatafilewrite = open("appdata.json", "w+")
    appdatafileread = open("appdata.json", "r")
    minersfile = open("miners.json", "r")
    if "--create-config" in sys.argv:
        utils.createconfig()
    print("Loading config...")
    configfile = open("config.json", "r")
    try:
        config = configfile.read()
    except:
        utils.createconfig()
    configfile = open("config.json", "r")
    config = configfile.read()
    miners = json.loads(minersfile.read())
    appdata = json.loads(appdatafileread.read())
    if not appdatafileread or "--benchmark" in sys.argv: #check for first run or requested rebenchmark
        appdata = {}
        print("Benchmarking algos...")
        for algo in miners["supported-algos"]:
            result = benchmark.benchmark(algo) #benchmark an algo if it is supported
            appdata["benchmark-data"]["hashrate"][algo] = result["hashrate"]
            appdata["benchmark-data"]["power"][algo] = result["power"]
        appdatafilewrite.write(json.dumps(appdata))
    supportedalgos = []
    for algo in miners["supported-algos"]:
        supportedalgos.append(algo)
    print("Getting the best profit miner...")
    best = requests.post("minecrap.dankepool.org:8080", data = json.dumps({appdata["benchmark-data"]}))
    bestalgo = ""
    found = False
    for algo in best:
        if algo in supportalgos and not found:
            bestalgo = algo
            found = True
    appdatafileread.close()
    appdatafilewrite.close()
    minersfile.close()
    configfile.close()
    miner = appdata["benchmark-data"][bestalgo][0]
    #What you see below this is really stupid. I'll fix this in future updates but for now it's here so ethereum mining will work right.
    if miner == "ethminer":
        address = config["addresses"]["ethereum"]
    else:
        address = config["addresses"]["ethereum"]
    if sys.platform.startswith("win"):
        utils.startminer(miner, miners["miners"][miner]["start"], bestalgo, config)
        while True:
            s = subprocess.check_output('tasklist', shell=True)
            if appdata["benchmark-data"][best]["miner"] not in s:
                print("Miner crashed! Restarting...")
                utils.startminer(miner, miners["miners"][miner]["start"], bestalgo, config)
            else:
                hashrate = utils.apiHashrate(miner)
                print("Mining " + bestalgo + " at " + str(hashrate[0]) + hashrate[1] + "/s")
            time.sleep(5)
    else:
        utils.startminer(miner, miners[miner]["start"], bestalgo, config) #passes the miner, start line syntax, the algo to use (will be able to use coin soon™), and the config
        while True:
            tmp = os.popen("ps -Af").read()
            if appdata["benchmark-data"][best]["miner"] not in tmp:
                print("Miner crashed! Restarting...")
                utils.startminer(miner, miners["miners"][miner]["start"], bestalgo, config)
            else:
                hashrate = utils.apiHashrate(miner)
                print("Mining " + bestalgo + " at " + str(hashrate[0]) + hashrate[1] + "/s")
            time.sleep(5)
main()
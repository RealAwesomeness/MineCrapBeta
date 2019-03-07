import utils
import json
import time
import os
import sys
def benchmark(algo):
    minersfile = open("miners.json", "r")
    configfile = open("config_example.json", "r")
    appdatafile = open("appdata.json", "r+")
    appdata = appdatafile.read()
    if not appdata:
        appdata = {}
    else:
        appdata = json.loads(appdata)
    appdatafile.close()
    appdatafile = open("appdata.json", "w")
    config = json.loads(configfile.read())
    miners = json.loads(minersfile.read())
    for algo in miners["supported-algos"]:
        best = ["", 0]
        for miner in miners["supported-algos"][algo]:
            if miners["miners"][miner]["api"]:
                #What you see below this is really stupid. I'll fix this in future updates but for now it's here so ethereum mining will work right.
                if miner == "ethminer":
                    address = config["addresses"]["ethereum"]
                else:
                    address = config["addresses"]["ethereum"]
                utils.startminer(miner, miners["miners"][miner]["start"], algo, config, address)
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
    appdatafile.write(json.dumps(appdata))
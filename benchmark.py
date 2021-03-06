import utils
import json
import time
import os
import sys
def benchmark(algo):
    minersfile = open("miners.json", "r")
    configfile = open("config.json", "r")
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
    appdata["benchmark-data"] = {}
    for algo in miners["supported-algos"]:
        best = ["", 0]
        for miner in miners["supported-algos"][algo]:
            if miners["miners"][miner]["api"]:
                start = utils.startminer(miner, miners["miners"][miner]["start"], algo, config)
                if start!=False : #prevents the miner from being stupid and waiting for a miner that doesnt support an algo to average out its hashrate
                    time.sleep(30)
                    hashrate = utils.apiHashrate(miner)[0]
                    if hashrate > best[1]:
                        best[1] = hashrate
                        best[0] = miner
                    #except:
                        #print("API call failed - miner probably crashed")
                    start.terminate()
            elif algo in miners["miners"][miner]["best"]:
                 best = [miner, 99999999]
        appdata["benchmark-data"][algo] = best
    appdatafile.write(json.dumps(appdata))
    appdatafile.close()

import sys
import os
import json
import requests
import socket
from urllib.request import urlopen
def startminer(miner, start, algo, config, address):
    thewae = os.path.dirname(os.path.abspath(__file__))
    start = start.replace("ALGO", algo)
    start = start.replace("ADDRESS", address)
    found = False
    for pool in config["pools"]:
        if algo in config["pools"][pool]["algorithms"] and not found: #uses first pool with selected algorithm supported
            print("im here")
            print(config["pools"][pool])
            start = start.replace("POOL", config["pools"][pool]["url"])
            start = start.replace("PORT", config["pools"][pool]["algorithms"][algo]["port"])
            found = True
    if found: #checks if the miner can actually mine the algorithm
        if sys.platform.startswith("win"):
            start = thewae + "\\" miner + "\\" + miner + ".exe" + start
        else:
            start = "./" + miner + "/" + miner + start
        os.system(start)
        return True
    else:
        return False
def createconfig():
    configfile = open("config.json", "w+")
    configexample = open("config_example.json", "r")
    config = json.loads(configexample.read())
    for address in config["addresses"]:
         config["addresses"][address] = input("What is your " + str(address) + " address? ")
    getOut = False
    config["pools"] = {}
    newpool = "ipsum lorem"
    while newpool:
        newpool = str(input("Enter a pool URL - including the subdomain but without http/https - leave this empty to exit : "))
        config["pools"][newpool] = {}
        config["pools"][newpool]["url"] = newpool
        algo = "ipsum lorem"
        type = input("What kind of pool is this (i.e. yiimp, NOMP)? If you don't know leave this empty.")
        if type.lower() == "yiimp":
            config = yiimpalgos(newpool, config)
        elif type.lower() == "nomp":
            config = nompalgos(newpool, config)
        else:
            config["pools"][newpool]["algorithms"] = {}
            while algo:
                algo = input("Enter an algo this pool supports. If there aren't anymore just press enter : ")
                port = input("Enter the port for this algo : ")
                if algo:
                    config["pools"][newpool]["algorithms"][algo] = {}
                    config["pools"][newpool]["algorithms"][algo]["port"] = port
    configfile.write(json.dumps(config))
def yiimpalgos(url, config):
    try:
        status = urlopen("http://" + url + "/api/status")
    except:
        status = urlopen("https://" + url + "/api/status")
    status = json.loads(status.read())
    config["pools"][url]["algorithms"] = {}
    for algo in status:
        config["pools"][url]["algorithms"][algo] = {}
        config["pools"][url]["algorithms"][algo]["port"] = status[algo]["port"]
    return config
def nompalgos(url, config):
    port = input("What port is the api located on?")
    algo = input("What algo is this NOMP pool for?")
    try:
        status = urlopen("http://" + url + ":" + port + "/stats")
    except:
        status = urlopen("https://" + url + ":" + port + "/stats")
    status = json.loads(status.read())
    status = json.loads(requests.get(url + ":" + port + "/stats"))
    config["pools"][url]["algorithms"] = {}
    config["pools"][url]["algorithms"][algo] = {}
    config["pools"][url]["algorithms"][algo]["port"] = status["config"]["ports"][0]["port"]
    return config
def apiHashrate(miner): #returns hashrate for eth in mh and all others in kh
    if miner=="ccminer":
        return [ccminerapi("summary"), "kh"]
    if miner=="ethminer":
        return [int(json.loads(requests.get("127.0.0.1:6969", data = {
  "id": 1,
  "jsonrpc": "2.0",
  "method": "miner_getstat1"
}))["result"][2].split(";")[0])/10, "mh"]
def ccminerapi(command):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("127.0.0.1", 6969)
    try:
        sock.connect((server_address))
        print ("Connected to ccminer API")
        sock.sendall(command)
        data = sock.recv(4096)
        data = data.replace('|\x00','')
        data_split = data.split(';')
        keys = []
        values = []
        for item in data_split:
            item_split = item.split('=')
            keys.append(item_split[0])
            values.append(item_split[1])
        api_json = {}
        i = 0
        while i < len(keys):
            api_json[keys[i]] = values[i]
            i+=1
    except Exception as err:
        api_json = {}
        if command == 'summary':
            api_json['KHS'] = 'crashed'
        
    return api_json

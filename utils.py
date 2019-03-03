import sys
import os
import json
import requests
import socket
def startminer(miner, start, algo, config):
	start = start.replace("ALGO", algo)
	start = start.replace("ADDRESS", config["addresses"]["bitcoin"])
	start = start.replace("WORKER", config["workername"])
	found = False
	for pool in config["pools"]:
		temppath = config["pools"][pool]
		if algo in temppath["algorithms"] and not Found: #uses first pool with selected algorithm supported
			if temppath["algorithms"][algo]["subdomain"]:
				start = start.replace("POOL", temppath["url"])
				start = start.replace("SUBDOMAIN", temppath["algorithms"][algo]["subdomain"] + ".")
				start = start.replace("PORT", temppath["algorithms"][algo]["port"])
				found = True
			else:
				start = start.replace("POOL", temppath["url"])
				start = start.replace("SUBDOMAIN", "")
				start = start.replace("PORT", temppath[algo]["port"])
				found = True
	if sys.platform.startswith("win"):
		start = miner + ".exe\\" + miner + ".exe" + start
	else:
		start = "./" + miner + "/" + miner + start
	os.system(start)
def createconfig():
	configfile = open("config.json", "w+")
	configexample = open("config_example.json", "r")
	config = json.load(configexample.read())
	for address in addresses:
		addresses[address] = input("What is your " + str(address) + " address? ")
	getOut = False
	while not getOut:
		newpool = input("Enter a pool URL - including the subdomain.")
		config["pools"][newpool]["url"] = newpool
		algo = "ipsum lorem"
		type = input("What kind of pool is this (i.e. yiimp, NOMP)? If you don't know leave this empty.")
		if type.lower() == "yiimp":
			config = yiimpalgos(newpool, config)
		if type.lower() == "nomp":
			config = nompalgos(newpool, config)
		while not algo:
			algo = input("Enter an algo this pool supports. If there aren't anymore just press enter : ")
			port = input("Enter the port for this algo : ")
			if not algo:
				config["pools"][newpool]["algorithms"][algo]["port"] = port
def yiimpalgos(url, config):
	status = json.loads(requests.get(url + "/api/status"))
	for algo in status:
		config["pools"][newpool]["algorithms"][algo]["port"] = status[algo]["port"]
	return config
def nompalgos(url, config):
	port = input("What port is the api located on?")
	algo = input("What algo is this NOMP pool for?")
	status = json.loads(requests.get(url + ":" + port + "/stats")
	config["pools"][newpool]["algorithms"][algo]["port"] = status["config"]["ports"][0]["port"]
def apiHashrate(miner): #returns hashrate for eth in mh and all others in kh
	if miner=="ccminer":
		return [ccminerapi("summary"), "kh"]
	if miner=="ethminer";
		return [int(json.loads(requests.post("127.0.0.1:6969", data = {
  "id": 1,
  "jsonrpc": "2.0",
  "method": "miner_getstat1"
}))["result"][2].split";"[0])/10, "mh"]
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
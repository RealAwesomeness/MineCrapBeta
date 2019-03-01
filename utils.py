import sys
import os
import json
def startminer(miner, start, algo, config):
	start = start.replace("ALGO", algo)
	start = start.replace("ADDRESS", config["addresses"]["bitcoin"])
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
		start = miner + "\\" + miner + ".exe" + start
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
		newpool = input("Enter a pool URL (Don't enter the subdomain!)")
		config["pools"][newpool]["url"] = newpool
		algo = "ipsum lorem"
		while not algo:
			algo = input("Enter an algo this pool supports. If there aren't anymore just press enter : ")
			subdomain = input("Enter the subdomain this is located on if applicable (Press enter if it's not). If you don't know what that is, search it up : ")
			port = input("Enter the port for this algo : ")
			if not algo:
				config["pools"][newpool]["algorithms"][algo]["port"] = port
				config["pools"][newpool]["algorithms"][algo]["subdomain"] = subdomain + "."

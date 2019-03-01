import sys
import os
def startminer(miner, start, algo, config) :
	start = start.replace("ALGO", algo)
	start = start.replace("ADDRESS", config["addresses"]["bitcoin"])
	found = False
	for pool in config["pools"]:
		if algo in pool["algorithms"] and not Found: #uses first pool with selected algorithm supported
			if pool["algorithms"][algo]["subdomain"]:
				start = start.replace("POOL", pool["url"])
				start = start.replace("SUBDOMAIN", pool["algorithms"][algo]["subdomain"] + ".")
				start = start.replace("PORT", pool["algorithms"][algo]["port"])
				found = True
			else:
				start = start.replace("POOL", pool["url"])
				start = start.replace("SUBDOMAIN", "")
				start = start.replace("PORT", pool[algo]["port"])
				found = True
	if sys.platform.startswith("win"):
		start = miner + "\\" + miner + ".exe" + start
	else:
		start = "./" + miner + "/" + miner + start
	os.system(start)

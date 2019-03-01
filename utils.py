import sys
import os
def startminer(miner, start, algo, config) :
	start = start.replace("ALGO", algo)
	start = start.replace("ADDRESS", config["addresses"]["bitcoin"])
	start = start.replace("POOL", config[algo]["pool"])
	start = start.replace("PORT", config[algo]["port"]
	if sys.platform.startswith("win"):
		start = miner + "\\" + miner + ".exe" + start
	else:
		start = "./" + miner + "/" + miner + start
	os.system(start)

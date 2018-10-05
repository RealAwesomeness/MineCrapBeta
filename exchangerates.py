import json
import sys
#credit to cmallory183#7302 for the exchange bot code - I modified the code for local use
def getVariance(prevday, lastval):
	variance = float(((lastval - prevday) / (prevday)) * 100)
	return float(variance)
def getJsonFromTradeOgre():
	url = 'https://tradeogre.com/api/v1/markets'
	response = None
	try:
		with aiohttp.request('GET', url) as result:
			if result.status == 200:
				temp = None
				temp = result.json()

				#required for json as a list of dict
				response = json.dumps(temp)
	except:
		response = None
	return response

def getJsonFromStocksExchange():
	url = 'https://app.stocks.exchange/api2/ticker'
	response = None
	try:
		with aiohttp.get(url) as result:
			if result.status == 200:
				response = result.json()
	except:
		response = None
	return response

def getJsonFromCryptoBridge():
	url = 'https://api.crypto-bridge.org/api/v1/ticker'
	response = None
	try:
		with aiohttp.get(url) as result:
			if result.status == 200:
				response = result.json()
	except:
		response = None
	return response

def getJsonFromCoinGecko():
	url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=btc'
	response = None
	try:
		with aiohttp.request('GET', url) as result:
			if result.status == 200:
				temp = None
				temp = result.json()

				#required for json as a list of dict
				response = json.dumps(temp)
	except:
		response = None
	return response

def getJsonFromSouthXchange(coin):
	url = 'https://www.southxchange.com/api/price/{0}/BTC'.format(coin)
	response = ""
	try:
		with aiohttp.get(url) as result:
			if result.status == 200:
				response = result.json()
	except:
		return	None
	return response

def getJsonFromCryptopia(coin):
	url = 'https://www.cryptopia.co.nz/api/GetMarket/{0}_BTC'.format(coin)
	response = ""
	try:
		with aiohttp.get(url) as result:
			if result.status == 200:
				response = result.json()
	except:
		return	None
	return response

def getJsonFromGraviex(coin):
	url = 'https://graviex.net//api/v2/tickers/{0}btc'.format(coin)
	response = ""
	try:
		with aiohttp.get(url) as result:
			if result.status == 200:
				response = result.json()
	except:
		return	None
	return response

def getJsonFromCrex(coin):
	url = 'https://api.crex24.com/v2/public/tickers?instrument={0}-BTC'.format(coin)
	response = ""
	try:
		with aiohttp.get(url) as result:
			if result.status == 200:
				response = result.json()
	except:
		return	None
	return response
exchanges=[]
def to(coin):
	"""to(coin) to get info on coin from TradeOgre"""
	exchanges.append(to)
	jsonResult = getJsonFromTradeOgre()
	if jsonResult != None:
		found = False
		coin = 'BTC-' + coin.upper()
		#json is returned from TradeOgre in non-standard format which python see it as a list of dict
		#use json.loads to parse json into a list of strings and then enumerate dict using key/value pairs
		temp = json.loads(jsonResult)
		for data in temp:
			for key, value in data.items():
				if key == coin:
					messageResponse = {}
					messageResponse["last"] = float(value['price'])
					messageResponse["buy"] = float(value['bid'])
					messageResponse["sell"] = float(value['ask'])
					messageResponse["24hvariance"] = float(((float(value['price']) - float(value['initialprice'])) / float(value['initialprice'])) * 100)
					messageResponse["found"] = True
					found=True
					break
		if found==False:
			messageResponse["found"] = False
	return (json.dumps(messageResponse))
		
	
def cb(coin):
	"""cb(coin) to get info on coin from Crypto-Bridge"""
	exchanges.append(cb)
	jsonResult = getJsonFromCryptoBridge()
	if jsonResult != None:
		found = False
		coin = coin + "_BTC"
		for entry in jsonResult:
			if str(entry["id"]).upper() == coin.upper():
				messageResponse = {}
				messageResponse["last"] = entry["last"]
				messageResponse["buy"] = entry["bid"]
				messageResponse["sell"] = entry["ask"]
				messageResponse["24hvariance"] = None
				messageResponse["found"] = True
				found=True
				break
		if found==False:
			messageResponse["found"] = False
	return (json.dumps(messageResponse))
	
	
def se(coin):
	"""se(coin) to get info on coin from Stocks.Exchange"""
	exchanges.append(se)
	jsonResult = getJsonFromStocksExchange()
	if jsonResult != None:
		found = False
		coin = coin + '_BTC'
		for entry in jsonResult:
			print(str(entry['market_name']).upper())
			if str(entry['market_name']).upper() == coin.upper():
				messageResponse = {}
				messageResponse["last"] = float(entry['last'])
				messageResponse["buy"] = float(entry['bid'])
				messageResponse["sell"] = float(entry['ask'])
				messageResponse["24hvariance"] = getVariance(float(entry['lastDayAgo']), float(entry['last']))
				messageResponse["found"] = True
				found=True
				break
		if found==False:
			messageResponse["found"] = False
		
	
def sx(coin):
	"""sx(coin) to get info on coin from SouthXchange"""
	exchanges.append(sx)
	jsonResult = getJsonFromSouthXchange(coin)
	messageResponse={}
	if len(jsonResult) == 0 or jsonResult == None:
		messageResponse["found"] = False
		return
	messageResponse["last"] = jsonResult['Last']
	messageResponse["buy"] = jsonResult['Bid']
	messageResponse["sell"] = jsonResult['Ask']
	messageResponse["24variance"] = jsonResult['Variation24Hr']
	messageResponse["found"] = True
		
	
def ct(coin):
	"""ct(coin) to get info on coin from Cryptopia"""
	exchanges.append(ct)
	jsonResult = getJsonFromCryptopia(coin)
	if jsonResult != None:
		if jsonResult['Data'] == None:
			messageResponse = '```Sorry, your coin was not found on Cryptopia.```'
		else:
			messageResponse = '```'
			messageResponse += 'Data provided by Cryptopia | https://www.cryptopia.co.nz \n'
			messageResponse += '{0}_BTC pairing from Cryptopia'.format(coin.upper()) + '\n'
			messageResponse += '{0:20}:\t{1:.8f}\n'.format('Last Value', jsonResult['Data']['LastPrice'])
			messageResponse += '{0:20}:\t{1:.8f}\n'.format('Buying Value', jsonResult['Data']['BidPrice'])
			messageResponse += '{0:20}:\t{1:.8f}\n'.format('Selling Value', jsonResult['Data']['AskPrice'])
			messageResponse += '{0:20}:\t{1:.2f}%'.format('24hr Variation', jsonResult['Data']['Change'])
			messageResponse += '```'
	elif jsonResult == None:
		messageResponse = '```Could not connect to Cryptopia.  Wait and try again.```'
	
	
def gv(coin):
	"""gv(coin) to get info on coin from Graviex"""
	exchanges.append(gv)
	jsonResult = getJsonFromGraviex(coin)
	if jsonResult != None:
		try:
			messageResponse = '```'
			messageResponse += 'Data provided by Graviex | https://graviex.net \n'
			messageResponse += '{0}_BTC pairing from Graviex'.format(coin.upper()) + '\n'
			messageResponse += '{0:20}:\t{1:.8f}\n'.format('Last Value', float(jsonResult['ticker']['last']))
			messageResponse += '{0:20}:\t{1:.8f}\n'.format('Buying Value', float(jsonResult['ticker']['buy']))
			messageResponse += '{0:20}:\t{1:.8f}\n'.format('Selling Value', float(jsonResult['ticker']['sell']))
			messageResponse += '{0:20}:\t{1:.2f}%'.format('24hr Variation', round(float(jsonResult['ticker']['change']) * 100,2))
			messageResponse += '```'
		except:
			messageResponse = '```Sorry, your coin was not found on Graviex.```'
			print(traceback.format_exc())
	elif jsonResult == None:
		messageResponse = '```Could not connect to Graviex.  Wait and try again.```'
	
	
def cx(coin):
	"""cx(coin) to get info on coin from Crex24"""
	exchanges.append(cx)
	# Coin must be passed in uppercase, otherwise API will not find it
	jsonResult = getJsonFromCrex(coin.upper())
	if jsonResult != None:
		print('json string: ' + str(jsonResult))
		try:
			messageResponse = '```'
			messageResponse += 'Data provided by Crex24 | https://crex24.com \n'
			messageResponse += '{0}_BTC pairing from Crex24'.format(coin.upper()) + '\n'
			messageResponse += '{0:20}:\t{1:.8f}\n'.format('Last Value', float(jsonResult[0]['last']))
			messageResponse += '{0:20}:\t{1:.8f}\n'.format('Buying Value', float(jsonResult[0]['bid']))
			messageResponse += '{0:20}:\t{1:.8f}\n'.format('Selling Value', float(jsonResult[0]['ask']))
			messageResponse += '{0:20}:\t{1:.2f}%'.format('24hr Variation', float(jsonResult[0]['percentChange']))
			messageResponse += '```'
		except:
			messageResponse = '```Sorry, your coin was not found on Crex24.```'
			print(traceback.format_exc())
	elif jsonResult == None:
		messageResponse = '```Could not connect to Crex24.  Wait and try again.```'
def main():
	information={}
	for exchange in exchanges :
		information[str(exchange)]=exchange(sys.argv[1]) #uses the first arg as the coin
	print(json.dumps(information))

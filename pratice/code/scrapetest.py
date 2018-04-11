#scrape
from coinmarketcap import Market
coinmarketcap = Market()
bla = coinmarketcap.ticker("bitcoin")

#conv to dict
blastr = bla[0]

#test printing all
#print(blastr.keys())
#print(blastr.values())
#print(blastr.items())

"""THE SHIT I NEED"""
print("Price = $" + blastr["price_usd"])

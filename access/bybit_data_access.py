import sys, json, urllib.request
sys.path.append(".")

from models.symbol import Symbol
from access.access_base import bybit_config


def get_bybit_perps():
    with urllib.request.urlopen(bybit_config["linear_instruments_url"]) as url:
        data = json.load(url)["result"]["list"]
        
    perps = []
    
    for perp in data:
        symbol = Symbol()
        
        symbol.Name        = perp["symbol"]
        symbol.BaseCoin    = perp["baseCoin"]
        symbol.QuoteCoin   = perp["quoteCoin"]
        symbol.Exchange    = "BYBIT"
        symbol.ChannelType = "linear"
        
        perps.append(symbol)
        
    return perps

# GET: 
bybit_perps = get_bybit_perps()
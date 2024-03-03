from access.bybit_access.bybit_perp_contracts import get_bybit_perps
from access.bybit_access.bybit_stream_reader import get_stream

bybit_perp_symbols = get_bybit_perps()

symbols = []

def get_symbols():
    for symbol in bybit_perp_symbols:
        symbols.append(f"{symbol.Base}{symbol.Quote}")
    return symbols

def get_perps_stream(interval:int, sleep_secs:float):
    get_stream(get_symbols(), interval, sleep_secs)
    

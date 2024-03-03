from access.access_base.csv_reader import get_file_data
from domain.dtos.symbol_dto import SymbolDto


def get_bybit_perps():
    file_data = get_file_data("bybit_entities\\bybit_symbols.csv")

    symbols = []

    for row in file_data:
        symbol = SymbolDto()
        symbol.Base = row[0]
        symbol.Quote = "USDT"
        symbol.Exchange = "BYBIT"
        symbol.ChannelType = "linear"
        
        symbols.append(symbol)

    return symbols
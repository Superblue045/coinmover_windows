from pybit.unified_trading import WebSocket
from time import sleep

ws = WebSocket(
    testnet = False,
    channel_type = "linear",
)

def handle_message(message):
    print(message)

def get_orderbook(symbol:(str,list), debth:int):
    ws.orderbook_stream(debth, symbol, handle_message)

    while True:
        sleep(15)
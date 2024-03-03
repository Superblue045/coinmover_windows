from pybit.unified_trading import WebSocket
from time import sleep

sleep_time : float = 0.0

ws = WebSocket(
    testnet      = False,
    channel_type = "linear"
)
    
def handle_message(message):
    print(message)

def get_stream(symbol:(str,list), interval:int, sleep_secs:float): # type: ignore
    sleep_time = sleep_secs
    
    ws.kline_stream(
    interval = interval,
    symbol   = symbol,
    callback = handle_message
    )

    while True:
        sleep(sleep_time)

from tradingview_ta import TA_Handler, Interval

crypto_screener = "crypto"
target_exchange = "BYBIT"
target_interval = Interval.INTERVAL_4_HOURS

link = TA_Handler(
    symbol   = "LINKUSDT.P",
    screener = crypto_screener,
    exchange = target_exchange,
    interval = target_interval
)

data_context = link.get_analysis().indicators
rsi_data = data_context["RSI"]

print(rsi_data)
print("{:.2f}".format(round(float(rsi_data / 2), 2)))
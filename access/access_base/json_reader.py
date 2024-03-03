import sys
import json

config_path = f"{sys.path[0]}\\configurations\\"

bybit_config     = json.load(open(f"{config_path}bybit_config.json"))
emoji_config     = json.load(open(f"{config_path}emoji_config.json"))
message_config   = json.load(open(f"{config_path}message_config.json"))
telegram_config  = json.load(open(f"{config_path}telegram_config.json"))


print("endpoint : " + bybit_config["endpoint"])
print("apiKey : " + bybit_config["api_key"])
print("apiSecret : " + bybit_config["api_secret"])



# Iterating through the json
# list
for i in bybit_config['emp_details']:
    print(i)
 
# Closing file
f.close()



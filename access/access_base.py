import os, json


config_path = f"{os.getcwd()}\\config\\"

bybit_config     = json.load(open(f"{config_path}bybit_config.json"))
emoji_config     = json.load(open(f"{config_path}emoji_config.json"))
telegram_config  = json.load(open(f"{config_path}telegram_config.json"))

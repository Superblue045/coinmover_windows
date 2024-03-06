#!/usr/bin/env python
# coding: utf-8

# In[ ]:
# Created by elmontagne
### author:  elmontagne
### discord: j.b.elmontagne#3234
### site:    https://github.com/elmontagne/coinmover_bybit

import configparser
import os.path
import time
from uuid import uuid4

import requests
from logzero import logger
from pybit import spot, usdt_perpetual, HTTP


class Bybit:
    """Bybit API"""

    api_url = "https://api.bybit.com/"
    session = None
    old_pnl = 0
    pnl = 0
    wallet = {}
    balance = 0
    used_margin = 0
    profit = 0
    margin = 0
    liq_long = 0
    liq_short = 0

    def __init__(self, config):
        self.config = config["bybit_coinmover"]
        self.botname = self.config["botname"]
        self.sleeptime = self.config["sleeptime"]
        self.sleeptimeliq = self.config["sleeptimeliq"]
        self.api_key = self.config["apikey"]
        self.api_secret = self.config["apisecret"]
        self.discord_webhook = self.config["discord_webhook"]
        self.max_margin = int(self.config["maxmargin"])
        self.percentage_move = int(self.config["percentage_move"])

        if os.path.isfile("status") and os.stat("status").st_size > 0:
            logger.debug("Loading status file")
            with open("status", "r", encoding="UTF-8") as pnl_file:
                self.old_pnl = float(pnl_file.readline())

    def start_session(self):
        """Start a session with the API"""
        logger.debug("Starting ByBit session")
        self.session = HTTP(
            self.api_url, api_key=self.api_key, api_secret=self.api_secret
        )

    def refresh_balance(self):
        """Refresh the balance from the API"""
        self.wallet = self.session.get_wallet_balance(coin="USDT")
        self.balance = float(self.wallet["result"]["USDT"]["equity"])
        self.pnl = float(self.wallet["result"]["USDT"]["cum_realised_pnl"])
        self.used_margin = float(self.wallet["result"]["USDT"]["used_margin"])
        self.margin = self.used_margin / self.balance * 100

        with open("status", "w", encoding="UTF-8") as pnl_file:
            pnl_file.write(str(self.pnl))

    def has_profit(self):
        """Check if the bot has profit"""
        if self.old_pnl != 0 and self.pnl > self.old_pnl:
            self.profit = self.pnl - self.old_pnl
            return True
        else:
            self.profit = 0
            return False

    def can_transfert(self):
        """Check if the bot can transfer money"""
        return self.margin <= self.max_margin

    def transfer(self):
        """Transfer the money from the bot to SPOT"""
        totransfer = self.profit * self.percentage_move / 100
        transfer = round(totransfer,2)
        logger.info("Transferring %s to SPOT", transfer)

        self.session.create_internal_transfer(
            transfer_id=str(uuid4()),
            coin="USDT",
            amount=str(round(transfer, 2)),
            from_account_type="CONTRACT",
            to_account_type="SPOT",
        )

        status_message = (
            f"**Account:** {self.botname} " "\n"
            f"**Transfer**: SUCCESS " "\n"
            f"**TotalBalance:** {self.balance}" "\n"
            f"**Profit:** {self.profit} " "\n"
            f"**Transferred:** {transfer} TO SPOT"
        )
        self.notify_discord(status_message)
        self.old_pnl = self.pnl

    def notify_discord(self, message):
        """Notify the discord webhook"""
        data = {"content": message}
        if self.discord_webhook != "":
            result = requests.post(self.discord_webhook, json=data)

            if result.status_code != 200 or result.status_code != 204:
                logger.error("Discord webhook error: %s", result.text)

def spot_balance():
    config = configparser.ConfigParser()
    config.read("config.ini")

    bybit_spot = spot.HTTP(
    endpoint = "https://api.bybit.com",
    api_key = config.get('bybit_coinmover', 'apikey'),
    api_secret = config.get('bybit_coinmover', 'apisecret')
    )

    balance = bybit_spot.get_wallet_balance()
    balance = balance['result']['balances']

    for i in range(len(balance)):
        if balance[i]['coinName'] == 'USDT':
            break

    balance = float(balance[i]['free'])

    return balance

def liquidation_check():
    config = configparser.ConfigParser()
    config.read("config.ini")

    liq_distance = float(config.get('bybit_coinmover', 'liqdistance'))

    bybit_derivatives = usdt_perpetual.HTTP(
    endpoint = "https://api.bybit.com",
    api_key = config.get('bybit_coinmover', 'apikey'),
    api_secret = config.get('bybit_coinmover', 'apisecret')
    )

    positions = bybit_derivatives.my_position()['result']

    for i in range(len(positions)):
        if float(positions[i]['data']['size']) > 0:
            sym = positions[i]['data']['symbol']
            liq_price = float(positions[i]['data']['liq_price'])

            price = bybit_derivatives.query_kline(symbol = sym, interval = 1, from_time = int(time() - 60))['result'][0]['close']
            price = float(price)

            if ((liq_price / price) < (1 + liq_distance)) and ((liq_price / price) > (1 - liq_distance)):
                transfer_spot_to_derivatives()

def transfer_spot_to_derivatives():
    config = configparser.ConfigParser()
    config.read("config.ini")

    transfer_amount = config.get('bybit_coinmover', 'transferamount')

    session = HTTP('https://api.bybit.com/', api_key = config.get('bybit_coinmover', 'apikey'), api_secret = config.get('bybit_coinmover', 'apisecret'))

    session.create_internal_transfer(
        transfer_id=str(uuid4()),
        coin="USDT",
        amount=str(float(int(spot_balance() * float(transfer_amount) * 10000)) / 10000),
        from_account_type="SPOT",
        to_account_type="CONTRACT",
    )

def coinmover():
    """Main function that manage the movement of money from the bot to SPOT"""
    config = configparser.ConfigParser()
    config.read("config_bybit.ini")

    bybit = Bybit(config)
    bybit.start_session()

    sleeptime = int(bybit.sleeptime) * 60
    sleeptimeliq = int(bybit.sleeptimeliq) * 60

    counter = int(sleeptime / sleeptimeliq)

    while True:
        if counter == int(sleeptime / sleeptimeliq):
            currenttime = time.localtime()
            timenow = time.strftime("%I:%M:%S %p", currenttime)


            logger.info("%s Checking...", timenow)
            bybit.refresh_balance()
            # logger.info("Old balance: ",old_pnl)

            logger.info("Current balance: %s", bybit.balance)
            logger.info("Current PNL: %s", bybit.pnl)

            if bybit.has_profit():
                logger.info("We made profit")
                if bybit.can_transfert():
                    bybit.transfer()
                else:
                    status_message = (
                        "**TRANSFER**: FAILED **REASON:** Above maximum defined margin"
                    )
                    bybit.notify_discord(status_message)

            else:
                logger.info("No profit this times")
                status_message = (
                    f"**Account**: {bybit.botname}" "\n"
                    f"**Transfer**: No profit this time: {bybit.profit} " "\n"
                    f"**Current balance**: {bybit.balance}" "\n"
                    f"**Current PNL**: {bybit.pnl}" "\n"
                    
                )
                bybit.notify_discord(status_message)
            logger.info("Sleeping for %s seconds", sleeptime)        
            logger.info("Liquidation Check Sleeping for %s seconds", sleeptimeliq)
            logger.info("----------------------------------------")

            counter = -1

        liquidation_check()

        counter += 1
        time.sleep(sleeptimeliq)


if __name__ == "__main__":
    logger.info("Starting coinmover")
    coinmover()

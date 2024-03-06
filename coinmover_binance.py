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
from binance.client import Client

recv_window = 5000

class BinanceBot:
    """Binance API"""

    client = None
    old_pnl = 0
    pnl = 0
    balance = 0
    profit = 0
    margin = 0

    def __init__(self, config):
        self.config = config["binance_coinmover"]
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

    def start_client(self):
        """Start a client session"""
        logger.debug("Starting Binance client")
        self.client = Client(self.api_key, self.api_secret)
        print(self.api_key, ", ", self.api_secret)

    def refresh_balance(self):
        """Refresh the balance from the API"""
        account_info = self.client.futures_account()
        print(account_info)
        self.pnl = float(account_info['totalUnrealizedProfit'])
        self.margin = float(account_info['totalMaintMargin'])

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

    def can_transfer(self):
        """Check if the bot can transfer money"""
        return self.margin <= self.max_margin

    def transfer(self):
        """Transfer the money from the bot to SPOT"""
        to_transfer = self.profit * self.percentage_move / 100
        transfer = round(to_transfer, 2)
        logger.info("Transferring %s to SPOT", transfer)

        try:
            transfer_response = self.client.futures_account_transfer(
                asset='USDT',
                amount=transfer,
                type=2,
            )

            # Check if transfer was successful
            if transfer_response['tranId']:
                logger.info("Transfer successful")
                status_message = (
                    f"**Account:** {self.botname} " "\n"
                    f"**Transfer**: SUCCESS " "\n"
                    f"**TotalBalance:** {self.balance}" "\n"
                    f"**Profit:** {self.profit} " "\n"
                    f"**Transferred:** {transfer} TO SPOT"
                )
                self.notify_discord(status_message)
                self.old_pnl = self.pnl
            else:
                logger.error("Transfer failed")
                status_message = (
                    f"**Account:** {self.botname} " "\n"
                    f"**Transfer**: FAILED " "\n"
                    f"**TotalBalance:** {self.balance}" "\n"
                    f"**Profit:** {self.profit} " "\n"
                    f"**Transferred:** {transfer} TO SPOT"
                )
                self.notify_discord(status_message)
        except Exception as e:
            logger.error("Transfer failed: %s", str(e))
            status_message = (
                f"**Account:** {self.botname} " "\n"
                f"**Transfer**: FAILED " "\n"
                f"**TotalBalance:** {self.balance}" "\n"
                f"**Profit:** {self.profit} " "\n"
                f"**Transferred:** {transfer} TO SPOT"
            )
            self.notify_discord(status_message)

    def notify_discord(self, message):
        """Notify the discord webhook"""
        data = {"content": message}
        if self.discord_webhook != "":
            result = requests.post(self.discord_webhook, json=data)
            if result.status_code != 200 or result.status_code != 204:
                logger.error("Discord webhook error: %s", result.text)

client = Client(api_key='BacTG5Afw2fqJDFDqSo4bI446acVTNr9sOoKRrl6cogxZzeFMjAi6YXSArYJFD5F', api_secret='YZQMW4lSY2ZRnBKlMQuTsoILXkFxAqNywj95WlIagBnCt2DN2gkRRwOgeF9YqHG2')

def spot_balance():
    account_info = client.get_account()

    for balance in account_info['balances']:
        if balance['asset'] == 'USDT':
            return float(balance['free'])

    return 0.0

def liquidation_check():
    positions = client.futures_position_information()

    config = configparser.ConfigParser()
    config.read("config.ini")
    liq_distance = float(config.get('binance_coinmover', 'liqdistance'))

    for position in positions:
        if float(position['positionAmt']) > 0:
            symbol = position['symbol']
            liq_price = float(position['liquidationPrice'])

            ticker = client.get_ticker(symbol=symbol)
            price = float(ticker['lastPrice'])

            distance = abs(liq_price - price) / liq_price

            if distance < liq_distance:
                transfer_spot_to_futures()

def transfer_spot_to_futures():
    config = configparser.ConfigParser()
    config.read("config.ini")
    transfer_amount = float(config.get('binance_coinmover', 'transferamount'))

    response = client.futures_account_transfer(asset='USDT', amount=transfer_amount, type=2)

    if 'tranId' in response:
        print("Transfer successful")
    else:
        print("Transfer failed")

def coinmover():
    """Main function that manage the movement of money from the bot to SPOT"""
    config = configparser.ConfigParser()
    config.read("config.ini")

    binance_bot = BinanceBot(config)
    binance_bot.start_client()

    sleeptime = int(binance_bot.sleeptime) * 60
    sleeptimeliq = int(binance_bot.sleeptimeliq) * 60

    counter = int(sleeptime / sleeptimeliq)

    while True:
        if counter == int(sleeptime / sleeptimeliq):
            currenttime = time.localtime()
            timenow = time.strftime("%I:%M:%S %p", currenttime)

            logger.info("%s Checking...", timenow)
            binance_bot.refresh_balance()

            logger.info("Current balance: %s", binance_bot.balance)
            logger.info("Current PNL: %s", binance_bot.pnl)

            if binance_bot.has_profit():
                logger.info("We made profit")
                if binance_bot.can_transfer():
                    binance_bot.transfer()
                else:
                    status_message = (
                        "**TRANSFER**: FAILED **REASON:** Above maximum defined margin"
                    )
                    binance_bot.notify_discord(status_message)
            else:
                logger.info("No profit this time")
                status_message = (
                    f"**Account**: {binance_bot.botname}" "\n"
                    f"**Transfer**: No profit this time: {binance_bot.profit} " "\n"
                    f"**Current balance**: {binance_bot.balance}" "\n"
                    f"**Current PNL**: {binance_bot.pnl}" "\n"
                )
                binance_bot.notify_discord(status_message)
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

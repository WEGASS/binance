import datetime
import math
import time
import requests
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager

client = Client(input('API '), input('SECRET '))


class Account:
    def __init__(self, balance, btc_qty, average_price):
        self.balance = balance
        self.btc_qty = btc_qty
        self.average_price = average_price

def buy(price, qty, account):
    account.balance -= price * qty
   # account.balance -= 0.00075*(price * qty)
    account.btc_qty += qty
    account.average_price = (account.btc_qty * account.average_price + qty * price) / (account.btc_qty + qty)


def sell(price, qty, account):
    account.balance += price * qty
  #  account.balance -= 0.00075*(price * qty)
    account.btc_qty -= qty

def get_ticker(coin1="BTC", coin2="RUB"):
    last_price = client.get_ticker(symbol=f'{coin1}{coin2}')['lastPrice']
    last_price = round(float(last_price), 2)
    print(f'BITCOIN PRICE {last_price}')
    print(f'{datetime.datetime.now()}')
    return last_price


def calc_change(chg, account):
    change = (chg - account.average_price) / account.average_price * 100
    if change > 1 and account.btc_qty > 0.00001:
        qty = account.btc_qty * 0.2
        sell(chg, qty, account)
        print(f'[-] SELLED {qty} btc for {chg}\nTOTAL BTC: {account.btc_qty}')
        print(f'BALANCE: {account.balance}\nAVERAGE: {account.average_price}')
        print(f'TOTAL BALANCE: {account.btc_qty * chg + account.balance}')
        print(f'BITCOIN PRICE: {chg}\n')
    elif change < -1 and account.balance > 0.1:
        qty = account.balance/chg * 0.5
        buy(chg, qty, account)
        print(f'[+] BOUGHT {qty} btc for {chg}\nTOTAL BTC: {account.btc_qty}')
        print(f'BALANCE: {account.balance}\nAVERAGE: {account.average_price}')
        print(f'TOTAL BALANCE: {account.btc_qty * chg + account.balance}')
        print(f'BITCOIN PRICE: {chg}\n')
    else:
        print(f'BALANCE: {account.balance}')
        print(f'TOTAL BALANCE: {account.btc_qty * chg + account.balance}\nAVERAGE: {account.average_price}')
        print(f'BITCOIN PRICE: {chg}\n')

def main():
    firstprice = get_ticker()
    WEGAS = Account(10000, 0, firstprice)
    buy(firstprice, 5000 / firstprice, WEGAS)
    while True:
        calc_change(get_ticker(), WEGAS)
        time.sleep(30)
    # print(get_ticker())



if __name__ == '__main__':
    main()
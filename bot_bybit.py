import ccxt
import dontshare_config
import time
import requests

# connecting to the cex
bybit = ccxt.bybit(
    {
        "enableRateLimit": True,
        "apiKey": dontshare_config.API_KEY,
        "secret": dontshare_config.API_SECRET,
    }
)

symbol = "BTC/USDT"


def get_bid_ask():
    btc_bybit_book = bybit.fetch_order_book("BTC/USDT")
    btc_bid = btc_bybit_book["bids"][0][0]
    btc_ask = btc_bybit_book["asks"][0][0]
    return btc_bid, btc_ask


while True:

    # connecting to the coingecko
    respBtc = requests.get(
        "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    )
    responseBtc = respBtc.json()
    btc_price = responseBtc["bitcoin"]["usd"]

    respUsdt = requests.get(
        "https://api.coingecko.com/api/v3/simple/price?ids=tether&vs_currencies=usd"
    )
    responseUsdt = respUsdt.json()
    usdt_price = responseUsdt["tether"]["usd"]

    btc_usdt = btc_price / usdt_price
    print(btc_usdt)
    balance = bybit.fetch_balance()
    existing_order = bybit.fetch_open_orders
    bybit.cancel_all_orders("BTC/USDT")

    balance = bybit.fetch_balance()

    usdt_bal = balance["USDT"]["free"]
    btc_bal = balance["BTC"]["free"]

    bid_buy = get_bid_ask()[0]  # btc_bid
    bid_sell = get_bid_ask()[1]

    vol_buy = 0.5 * usdt_bal / bid_buy
    vol_sell = 0.5 * btc_bal
    bid_buy = round(bid_buy, 2)
    bid_sell = round(bid_sell, 2)

    btc_bal_usd_eqv = btc_bal * btc_usdt

    # placing buy and sell limit order
    order_buy = bybit.create_limit_buy_order(symbol, vol_buy, bid_buy)
    order_sell = bybit.create_limit_sell_order(symbol, vol_sell, bid_sell)

    currentTime = time.time()
    print(f"the best bid: {get_bid_ask()[0]}, the best ask: {get_bid_ask()[1]}")
    print(f"We just made orders at bid: {bid_buy}, and ask: {bid_sell}")
    print("//**********************************************************************//")
    print(" ")
    print("//**********************************************************************//")
    time.sleep(2.5)

from ast import Return
from multiprocessing.reduction import recv_handle
from multiprocessing.reduction import recv_handle
import robin_stocks.robinhood as rh
from datetime import datetime
from tradingview_ta import TA_Handler, Interval, Exchange
import tradingview_ta
import sched
import time
infinite=1
rh.authentication.login(username='gamespsych@gmail.com', password='Diablo71913', expiresIn=86400, scope='internal', by_sms=True, store_session=True, mfa_code=None, pickle_name='')
enteredTrade = False
while infinite==1:
    balance = float(rh.profiles.load_account_profile(info='buying_power'))
    print('Your available balance is:')
    print(balance)
    buying_power=balance * 0.95
    numtrades=0
    # Get 5 minute bar data for Ford stock
    #historical_quotes = rh.stocks.get_stock_historicals(inputSymbols='F', interval='5minute', span='day')
    price=rh.crypto.get_crypto_quote(symbol='DOGE', info=None)
    print('The current price is:')
    print(price['bid_price'])
    stock_price=float(price['bid_price'])
    handler = TA_Handler(
        symbol='DOGEUSD',
        exchange='binance',
        screener='crypto',
        interval='5m',
        timeout=None
    )
    analysis = handler.get_analysis()
    rsi=float(analysis.indicators["RSI"])
    print("The current RSI is:")
    print(rsi)
    crypto_balance=rh.crypto.get_crypto_positions(info='quantity_available')
    crypto=crypto_balance[0]
    crypto_bal=float(crypto)
    if enteredTrade == False and crypto_bal == 0:
        if rsi<=35:
            print("Buying RSI is below 35!")
            stock_amount=buying_power/stock_price
            stock_buy = round(stock_amount, 1)
            print('amout of stock to purchase')
            print(stock_buy)
            buy_order=rh.orders.order_buy_crypto_by_quantity(symbol='DOGE', quantity=stock_buy, timeInForce='gtc', jsonify=True)
            print(buy_order)
            enteredTrade = True

    if enteredTrade == True:
        if rsi>59:
            print("Selling RSI is above 60!")
            crypto_balance=rh.crypto.get_crypto_positions(info='quantity_available')
            crypto=crypto_balance[0]
            crypto_bal=float(crypto)
            sell_order=rh.orders.order_sell_crypto_by_quantity(symbol='DOGE', quantity=crypto_bal, timeInForce='gtc', jsonify=True)
            print(sell_order)
            enteredTrade = False
            numtrades = numtrades +1
            balance=float(rh.profiles.load_account_profile(info='buying_power'))
    time.sleep(60)
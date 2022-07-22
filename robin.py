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
rh.authentication.login(username='username', password='Password', expiresIn=86400, scope='internal', by_sms=True, store_session=True, mfa_code=None, pickle_name='')
enteredTrade = False
while infinite==1:
    balance = float(rh.profiles.load_account_profile(info='buying_power'))
    print('Your available balance is:')
    print(balance)
    buying_power=balance * 0.95
    numtrades=0
    price=rh.crypto.get_crypto_quote(symbol='DOGE', info=None)
    print('The current price is:')
    print(price['bid_price'])
    stock_price=float(price['bid_price'])
    stock_price=round(stock_price,6)
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
    macd=float(analysis.indicators["MACD.macd"])
    print('MACD is:')
    print(macd)
    if enteredTrade == False and buying_power > 5:
        if macd<-0.0001:
            print("Buying! MACD is favorable")
            stock_amount=buying_power/stock_price
            stock_buy = round(stock_amount, 1)
            print('Amount to purchase:')
            print(stock_buy)
            #buy_order=rh.orders.order_buy_crypto_by_quantity(symbol='DOGE', quantity=stock_buy, timeInForce='gtc', jsonify=True)
            buy_order=rh.orders.order_buy_crypto_limit(symbol='DOGE',quantity=stock_buy,limitPrice=stock_price,timeInForce='gtc', jsonify=True)
            print(buy_order)
            enteredTrade = True  
            time.sleep(600)

        if rsi<=35:
            print("Buying! RSI is below 35!")
            stock_amount=buying_power/stock_price
            stock_buy = round(stock_amount, 1)
            print('Amount to purchase:')
            print(stock_buy)
            #buy_order=rh.orders.order_buy_crypto_by_quantity(symbol='DOGE', quantity=stock_buy, timeInForce='gtc', jsonify=True)
            buy_order=rh.orders.order_buy_crypto_limit(symbol='DOGE',quantity=stock_buy,limitPrice=stock_price,timeInForce='gtc', jsonify=True)
            print(buy_order)
            enteredTrade = True
            time.sleep(600)

    if enteredTrade == True:
        print('Listing for sell at 1% profit')
        crypto_balance=rh.crypto.get_crypto_positions(info='quantity_available')
        crypto=crypto_balance[0]
        crypto_bal=float(crypto)
        cryptoSell=stock_price * 0.01
        sellOrder=stock_price + cryptoSell
        sellOrder=round(sellOrder,3)
        print('Selling:')
        print(crypto_bal)
        print("at:")
        print(sellOrder)
        sell_order=rh.orders.order_sell_crypto_limit(symbol='DOGE',quantity=crypto_bal,limitPrice=sellOrder,timeInForce='gtc', jsonify=True)
        print(sell_order)
        enteredTrade = False
        numtrades = numtrades + 1
        balance=float(rh.profiles.load_account_profile(info='buying_power'))
        #if rsi>59:
            #print("Selling RSI is above 60!")
            #crypto_balance=rh.crypto.get_crypto_positions(info='quantity_available')
            #crypto=crypto_balance[0]
            #crypto_bal=float(crypto)
            #sell_order=rh.orders.order_sell_crypto_by_quantity(symbol='DOGE', quantity=crypto_bal, timeInForce='gtc', jsonify=True)
            #print(sell_order)
            #enteredTrade = False
            #numtrades = numtrades +1
            #balance=float(rh.profiles.load_account_profile(info='buying_power'))
    time.sleep(60)

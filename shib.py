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
rh.authentication.login(username='username', password='password', expiresIn=86400, scope='internal', by_sms=True, store_session=True, mfa_code=None, pickle_name='')
enteredTrade = False
while infinite==1:
    try:
        balance = float(rh.profiles.load_account_profile(info='buying_power'))
        print('Your available balance is:')
        print(balance)
        buying_power=balance * 0.95
    except:
        print("Unable to connect to Robinhood API to retrieve your balance")
    numtrades=0
    try:
        price=rh.crypto.get_crypto_quote(symbol='ADA', info=None)
        print('The current price is:')
        print(price['bid_price'])
        stock_price=float(price['bid_price'])
        stock_price=round(stock_price,6)
    except:
        print("Unable to connect to the Robinhood API to retrieve a price")
    try:
        handler = TA_Handler(
            symbol='ADAUSD',
            exchange='coinbase',
            screener='crypto',
            interval='5m',
            timeout=None
        )
        analysis = handler.get_analysis()
        rsi=float(analysis.indicators["RSI"])
        print("The current 5m RSI is:")
        print(rsi)
    except:
        print("Unable to connect to the Tradingview API to get TA")
    try:
        crypto_balance=rh.crypto.get_crypto_positions(info='quantity_available')
        crypto=crypto_balance[0]
        crypto_bal=float(crypto)
    except:
        print("Unable to connect to Robinhood to retrieve your balance")
    try:
        macd=float(analysis.indicators["MACD.macd"])
        print('MACD is:')
        print(macd)
    except:
        print("Unable to connect to the Tradingview API to retrieve MACD")
    try:
         handler = TA_Handler(
            symbol='ADAUSD',
            exchange='coinbase',
            screener='crypto',
            interval='5m',
            timeout=None
        )
    except:
        print("Unable to connect to the Tradingview API to get TA")
    onedanalysis = handler.get_analysis()
    onedrsi=float(onedanalysis.indicators["RSI"])
    print("The current 1d RSI is:")
    print(onedrsi)
    if enteredTrade == False and buying_power > 5:
        if macd<-0.0001 and onedrsi < 55:
            print("Buying! MACD is favorable")
            stock_amount=buying_power/stock_price
            stock_buy = round(stock_amount, 1)
            print('Amount to purchase:')
            print(stock_buy)
            #buy_order=rh.orders.order_buy_crypto_by_quantity(symbol='ADA', quantity=stock_buy, timeInForce='gtc', jsonify=True)
            try:
                buy_order=rh.orders.order_buy_crypto_limit(symbol='ADA',quantity=stock_buy,limitPrice=stock_price,timeInForce='gtc', jsonify=True)
                print(buy_order)
                time.sleep(600)
            except:
                print("Unable to connect to Robinhood to send the buy order")
            enteredTrade = True 
            
            

        if rsi<=35 and onedrsi < 55:
            print("Buying! RSI is below 35!")
            stock_amount=buying_power/stock_price
            stock_buy = round(stock_amount, 1)
            print('Amount to purchase:')
            print(stock_buy)
            #buy_order=rh.orders.order_buy_crypto_by_quantity(symbol='ADA', quantity=stock_buy, timeInForce='gtc', jsonify=True)
            try:
                buy_order=rh.orders.order_buy_crypto_limit(symbol='ADA',quantity=stock_buy,limitPrice=stock_price,timeInForce='gtc', jsonify=True)
                print(buy_order)
            except:
                print("Unable to connect to Robinhood to submit the buy order")
            enteredTrade = True
            time.sleep(600)
            try:
                crypto_balance=rh.crypto.get_crypto_positions(info='quantity_available')
                crypto=crypto_balance[0]
                crypto_bal=float(crypto)
            except:
                print("Unable to connect to Robinhood to retrieve your balance")

    if enteredTrade == True:        
        try:
                crypto_balance=rh.crypto.get_crypto_positions(info='quantity_available')
                crypto=crypto_balance[0]
                crypto_bal=float(crypto)
        except:
                print("Unable to connect to Robinhood to retrieve your balance")
        if crypto_bal < 10:
                try:
                    rh.orders.cancel_all_crypto_orders()
                    enteredTrade = False
                    time.sleep(6)
                except:
                    print("Cannot connect to Robinhood to cancel orders.")
                
    if enteredTrade == True:
        print('Listing for sell at 1% profit')
        try:
            crypto_balance=rh.crypto.get_crypto_positions(info='quantity_available')
            crypto=crypto_balance[0]
            crypto_bal=float(crypto)
            crypto_bal = round(crypto_bal, 2)
            crypto_bal = crypto_bal - 0.01
            cryptoSell=stock_price * 0.01
            sellOrder=stock_price + cryptoSell
            sellOrder=round(sellOrder,3)
        except:
            print("Unable to connect to Robinhood to get the price we need to sell at")
        print('Selling:')
        print(crypto_bal)
        print("at:")
        print(sellOrder)
        try:
            sell_order=rh.orders.order_sell_crypto_limit(symbol='ADA',quantity=crypto_bal,limitPrice=sellOrder,timeInForce='gtc', jsonify=True)
            print(sell_order)
            enteredTrade = False
            numtrades = numtrades + 1
            balance=float(rh.profiles.load_account_profile(info='buying_power'))
        except:
            print("Unable to connect to Robinhood to send the sell order")
        #if rsi>59:
            #print("Selling RSI is above 60!")
            #crypto_balance=rh.crypto.get_crypto_positions(info='quantity_available')
            #crypto=crypto_balance[0]
            #crypto_bal=float(crypto)
            #sell_order=rh.orders.order_sell_crypto_by_quantity(symbol='ADA', quantity=crypto_bal, timeInForce='gtc', jsonify=True)
            #print(sell_order)
            #enteredTrade = False
            #numtrades = numtrades +1
            #balance=float(rh.profiles.load_account_profile(info='buying_power'))
    time.sleep(60)

import json, config
import datetime
from flask import Flask, request, jsonify, render_template
from binance.client import Client
from binance.enums import *

app = Flask(__name__)

client = Client(config.API_KEY, config.API_SECRET, tld='us')

# def order(symbol, positionSide, side, timestamp, order_type=ORDER_TYPE_MARKET):
#     try:
#         print(f"sending order {order_type} - {symbol} {positionSide} {side} ")
#         order = client.futures_create_order(
#             symbol=symbol,              # BTCUSDT
#             positionSide=positionSide,  # LONG, SHORT
#             side=side,                  # BUY, SELL
#             type=order_type,            # MARKET
#             timestamp=timestamp)        # time
#     except Exception as e:
#         print("an exception occured - {}".format(e))
#         return False
#
#     return order

def order(symbol, side, timestamp, order_type=ORDER_TYPE_MARKET):
    try:
        print(f"sending order {order_type} - {symbol} {side} ")
        order = client.futures_create_order(
            symbol=symbol,              # BTCUSDT
            side=side,                  # BUY, SELL
            type=order_type,            # MARKET
            timestamp=timestamp)        # time
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return order


@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    #print(request.data)
    data = json.loads(request.data)

    if data['passphrase'] != config.WEBHOOK_PASSPHRASE:
        return {
            "code": "error",
            "message": "Nice try, invalid passphrase"
        }

    side = data['strategy']['order_action'].upper() #BUY, SELL
    positionSide = data['strategy']['market_position'].upper() #LONG, SHORT
    #timestamp =  data['bar']['time']
    timestamp = datetime.datetime.now().timestamp()
    print(timestamp)
    # order_response = order("BTCUSDT", positionSide, side, timestamp)
    order_response = order("BTCUSDT", side, timestamp)

    if order_response:
        return {
            "code": "success",
            "message": "order executed"
        }
    else:
        print("order failed")

        return {
            "code": "error",
            "message": "order failed"
        }
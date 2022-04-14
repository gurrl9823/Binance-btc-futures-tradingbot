# import json, config
# import datetime
# from flask import Flask, request, jsonify, render_template
# from binance.client import Client
# from binance.enums import *
#
# app = Flask(__name__)
#
# client = Client(config.API_KEY, config.API_SECRET, tld='us')
#
# # def order(symbol, positionSide, side, timestamp, order_type=ORDER_TYPE_MARKET):
# #     try:
# #         print(f"sending order {order_type} - {symbol} {positionSide} {side} ")
# #         order = client.futures_create_order(
# #             symbol=symbol,              # BTCUSDT
# #             positionSide=positionSide,  # LONG, SHORT
# #             side=side,                  # BUY, SELL
# #             type=order_type,            # MARKET
# #             timestamp=timestamp)        # time
# #     except Exception as e:
# #         print("an exception occured - {}".format(e))
# #         return False
# #
# #     return order
#
# def order(symbol, side, positionSide, type):
#     try:
#         print(f"sending order {type} - {symbol} {side} ")
#         order = client.futures_create_order(
#             symbol=symbol,              # BTCUSDT
#             side=side,                  # BUY, SELL
#             positionSide=positionSide,  # LONG, SHORT
#             type=type)                  # MARKET
#     except Exception as e:
#         print("an exception occured - {}".format(e))
#         return False
#
#     return order
#
#
# @app.route('/')
# def welcome():
#     return render_template('index.html')
#
# @app.route('/webhook', methods=['POST'])
# def webhook():
#     #print(request.data)
#     data = json.loads(request.data)
#
#     if data['passphrase'] != config.WEBHOOK_PASSPHRASE:
#         return {
#             "code": "error",
#             "message": "Nice try, invalid passphrase"
#         }
#
#     side = data['strategy']['order_action'].upper() #BUY, SELL
#     positionSide = data['strategy']['market_position'].upper() #LONG, SHORT
#     type = 'MARKET'
#     quantity = 0.04
#     order_response = order("BTCUSDT", side, positionSide, type)
#
#     if order_response:
#         return {
#             "code": "success",
#             "message": "order executed"
#         }
#     else:
#         print("order failed")
#
#         return {
#             "code": "error",
#             "message": "order failed"
#         }


import json, config
from flask import Flask, request, jsonify, render_template
from binance.client import Client
from binance.enums import *

app = Flask(__name__)

# client = Client(config.API_KEY, config.API_SECRET, tld='us')
client = Client(config.API_KEY, config.API_SECRET)
# request_client = RequestClient(api_key = config.API_KEY, secret_key = config.API_SECRET)


def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        print(f"sending order {order_type} - {side} {quantity} {symbol}")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return order


@app.route('/')
def welcome():
    return render_template('index.html')


@app.route('/webhook', methods=['POST'])
def webhook():
    # print(request.data)
    data = json.loads(request.data)

    if data['passphrase'] != config.WEBHOOK_PASSPHRASE:
        return {
            "code": "error",
            "message": "Nice try, invalid passphrase"
        }

    side = data['strategy']['order_action'].upper()
    # account = request_client.get_account_information()
    quantity = 99.9 # 22/data['strategy']['order_price'] #data['strategy']['order_contracts']
    order_response = order(side, quantity, "DOGEUSDT")

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
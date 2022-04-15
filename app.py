import json, config
from flask import Flask, request, jsonify, render_template
from binance.client import Client
from binance.enums import *
import math

app = Flask(__name__)

client = Client(config.API_KEY, config.API_SECRET)

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


    symbol = "BTCUSDT"

    a = client.futures_get_all_orders(symbol=symbol)
    orderId = a[-1]['orderId']
    client.futures_cancel_order(symbol=symbol, orderId=orderId)


    side = data['strategy']['order_action'].upper() # buy, sell
    maxWithdrawAmount = float(client.futures_account()['maxWithdrawAmount'])
    leverage = 5
    print(maxWithdrawAmount)
    quantity = math.floor(maxWithdrawAmount * leverage / data['strategy']['order_price'] * 1000) / 1000
    print(quantity)
    order_type = "MARKET"

    print(f"sending order {side} {symbol} {order_type} {quantity} ")

    try:
        # client.futures_create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
        order_response = client.futures_create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False


    if order_response:
        print("order executed")
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
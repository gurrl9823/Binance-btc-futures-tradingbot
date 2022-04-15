import json, config
from flask import Flask, request, jsonify, render_template
from binance.client import Client
from binance.enums import *

app = Flask(__name__)

client = Client(config.API_KEY, config.API_SECRET)
# request_client = RequestClient(api_key = config.API_KEY, secret_key = config.API_SECRET)

def order(symbol, side, order_type=ORDER_TYPE_MARKET):
    try:
        print(f"sending order {order_type} - {side} {quantity} {symbol}")
        client.futures_cancel_order(symbol=symbol)
        # client.futures_create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)

        maxWithdrawAmount = float(client.futures_account().maxWithdrawAmount)
        quantity = maxWithdrawAmount / ['strategy']['order_price']

        order = client.futures_create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
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


    symbol = "BTCUSDT",

    client.futures_cancel_order(symbol=symbol)

    side = data['strategy']['order_action'].upper()
    maxWithdrawAmount = client.futures_account()['maxWithdrawAmount']
    quantity = maxWithdrawAmount / ['strategy']['order_price']
    order_type = "MARKET"

    print(f"sending order {order_type} - {side} {quantity} {symbol}")

    try:
        # client.futures_create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
        order_response = client.futures_create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False


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
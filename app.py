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

    # 현재 포지션의 코인 갯수
    a = client.futures_get_all_orders(symbol=symbol)
    executedQty = a[-1]['executedQty']
    print(executedQty)

    side = data['strategy']['order_action'].upper() # buy, sell

    order_type = "MARKET"



    # try:
    #     # 포지션 정리
    #     if x == long
    #         client.futures_create_order(symbol=symbol, side=side, type=order_type, quantity=executedQty)
    #
    #     # 최대 구매 가능 코인 계산
    #     maxWithdrawAmount = float(client.futures_account()['maxWithdrawAmount'])
    #     leverage = 15
    #     print(maxWithdrawAmount)
    #     quantity = math.floor(maxWithdrawAmount * leverage / data['strategy']['order_price'] * 1000) / 1000
    #     print(quantity)
    #
    #     # 포지션 진입
    #     order_response = client.futures_create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
    #     print(f"sending order {side} {symbol} {order_type} {quantity} ")
    #
    # except Exception as e:
    #     print("an exception occured - {}".format(e))
    #     return False


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
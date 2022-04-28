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
    # a = client.futures_get_all_orders(symbol=symbol)
    # executedQty = a[-1]['executedQty']
    # print('현재 포지션의 코인 개수 : ', executedQty)

    side = data['strategy']['order_action'].upper()  # buy, sell

    order_type = "MARKET"

    try:
        # 롱 포지션 정리
        if (data['strategy']['order_id'] == 'exit') and (data['strategy']['prev_market_position'] == 'long'):
            # order_response = client.futures_create_order(symbol=symbol, side=side, type='STOP_MARKET', stopPrice=data['strategy']['order_price'], closePosition='true')
            order_response = client.futures_create_order(symbol=symbol, side=side, type='STOP_MARKET', stopPrice=100, closePosition='true')
            print(f"sending order {side} {symbol} STOP_MARKET")
        # 숏 포지션 정리
        elif (data['strategy']['order_id'] == 'exit') and (data['strategy']['prev_market_position'] == 'short'):
            # order_response = client.futures_create_order(symbol=symbol, side=side, type='STOP_MARKET', stopPrice=data['strategy']['order_price'] - 100, closePosition='true')
            order_response = client.futures_create_order(symbol=symbol, side=side, type='STOP_MARKET', stopPrice=100, closePosition='true')
            print(f"sending order {side} {symbol} STOP_MARKET")
        # 포지션 진입
        else:
            # 최대 구매 가능 코인 계산
            # maxWithdrawAmount = math.floor(float(client.futures_account()['maxWithdrawAmount']) / 100) * 100
            maxWithdrawAmount = float(client.futures_account()['maxWithdrawAmount'])
            leverage = 15
            print("현재 구매 가능한 달러 : ", maxWithdrawAmount)
            quantity = math.floor(((maxWithdrawAmount * leverage) / data['strategy']['order_price']) * 1000) / 1000
            print("구매 가능한 코인 개수 : ", quantity)

            order_response = client.futures_create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
            print(f"sending order {side} {symbol} {order_type} {maxWithdrawAmount * 15}$ {quantity} ")

    except Exception as e:
        print("an exception occured - {}".format(e))
        order_response = False

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

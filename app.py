import json, config
from flask import Flask, request, jsonify, render_template
from binance.client import Client
from binance.enums import *
import math

app = Flask(__name__)

client = Client(config.API_KEY, config.API_SECRET)

global present_order_id
# present_order_id = ''

@app.route('/')
def welcome():
    return render_template('index.html')


@app.route('/webhook', methods=['POST'])
def webhook():
    global present_order_id
    # print(request.data)
    data = json.loads(request.data)
    print(data['passphrase'])



    if (data['passphrase'] != "don't sleep~") and (data['passphrase'] != "4h 497d 846%") and (data['passphrase'] != "30m 871d 40%") :
        print("Nice try, invalid passphrase")
        return {
            "code": "error",
            "message": "Nice try, invalid passphrase"
        }



    if data['passphrase'] == "don't sleep~" :
        return {
            "message": "don't sleep~"
        }





    if data['passphrase'] == "4h 497d 846%" :

        symbol = "BTCUSDT"

        # 현재 포지션의 코인 갯수
        # a = client.futures_get_all_orders(symbol=symbol)
        # executedQty = a[-1]['executedQty']
        # print('현재 포지션의 코인 개수 : ', executedQty)

        side = data['strategy']['order_action'].upper()  # buy, sell

        order_type = "MARKET"
        print(present_order_id)
        present_order_id = '1Short'
        print(present_order_id)
        # try:
        #     # 포지션 정리
        #     if ((data['strategy']['order_id'] == '1exit') or (data['strategy']['order_id'] == 'Close entry(s) order 1Long') or (data['strategy']['order_id'] == 'Close entry(s) order 1Short') or (data['strategy']['order_id'] == '1Long') or (data['strategy']['order_id'] == '1Short')) and ((present_order_id == '1Long') or (present_order_id == '1Short')):
        #         present_order_id = ''
        #         order_response = client.futures_create_order(symbol=symbol, side=side, type='STOP_MARKET',
        #                                                      stopPrice=100, closePosition='true')
        #         print(f"Close position : {data['strategy']['order_id']} {side} {symbol} STOP_MARKET")
        #
        #     # 포지션 진입
        #     if (data['strategy']['prev_market_position_size'] == 0) :
        #         present_order_id = data['strategy']['order_id']
        #         # 최대 구매 가능 코인 계산
        #         # maxWithdrawAmount = math.floor(float(client.futures_account()['maxWithdrawAmount']) / 100) * 100
        #         maxWithdrawAmount = float(client.futures_account()['maxWithdrawAmount']) * 0.99
        #         leverage = 3
        #         print("현재 구매 가능한 달러 : ", maxWithdrawAmount)
        #         quantity = math.floor(((maxWithdrawAmount * leverage) / data['strategy']['order_price']) * 1000) / 1000
        #         print("구매 가능한 코인 개수 : ", quantity)
        #
        #         order_response = client.futures_create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
        #         print(f"entry position : {data['strategy']['order_id']} {side} {symbol} {order_type} {maxWithdrawAmount * leverage}$ {quantity} ")
        #
        # except Exception as e:
        #     print("an exception occured - {}".format(e))
        #     order_response = False
        #
        # if order_response:
        #     print("order executed")
        #     return {
        #         "code": "success",
        #         "message": "order executed"
        #     }
        # else:
        #     print("order failed")
        #     return {
        #         "code": "error",
        #         "message": "order failed"
        #     }
        return {"message": "order failed"}





    if data['passphrase'] == "30m 871d 40%" :

        symbol = "BTCUSDT"

        side = data['strategy']['order_action'].upper()  # buy, sell

        order_type = "MARKET"

        try:
            # 포지션 정리
            if (data['strategy']['order_id'] == '2exit') and ((present_order_id == '2Long') or (present_order_id == '2Short')):
                present_order_id = ''
                order_response = client.futures_create_order(symbol=symbol, side=side, type='STOP_MARKET',
                                                             stopPrice=100, closePosition='true')
                print(f"Close position : {data['strategy']['order_id']} {side} {symbol} STOP_MARKET")
            # 포지션 진입
            elif data['strategy']['prev_market_position_size'] == 0:
                present_order_id = data['strategy']['order_id']
                # 최대 구매 가능 코인 계산
                # maxWithdrawAmount = math.floor(float(client.futures_account()['maxWithdrawAmount']) / 100) * 100
                maxWithdrawAmount = float(client.futures_account()['maxWithdrawAmount'])
                leverage = 3
                print("현재 구매 가능한 달러 : ", maxWithdrawAmount)
                quantity = math.floor(((maxWithdrawAmount * leverage) / data['strategy']['order_price']) * 1000) / 1000
                print("구매 가능한 코인 개수 : ", quantity)

                order_response = client.futures_create_order(symbol=symbol, side=side, type=order_type,
                                                             quantity=quantity)
                print(f"entry position : {data['strategy']['order_id']} {side} {symbol} {order_type} {maxWithdrawAmount * leverage}$ {quantity} ")

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




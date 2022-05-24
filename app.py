import json, config
# from binance_f import RequestClient
from flask import Flask, request, jsonify, render_template
from binance.client import Client
from binance.enums import *
import math

app = Flask(__name__)

client = Client(config.API_KEY, config.API_SECRET)
# request_client = RequestClient(api_key=config.API_KEY, secret_key=config.API_SECRET)

@app.route('/')
def welcome():
    return render_template('index.html')


@app.route('/webhook', methods=['POST'])
def webhook():
    # print(request.data)
    data = json.loads(request.data)
    print(data['passphrase'])

    s = client.futures_position_information()
    b = client.get_recent_trades(symbol='BTCUSDT')
    print(s)
    print(b[0]['qty'])

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



    symbol = "BTCUSDT"

    side = data['strategy']['order_action'].upper()  # buy, sell

    order_type = "MARKET"

    stopPrice = int(float(data['strategy']['order_price']) * 0.98)

    present_order_id = ''
    if data['strategy']['prev_market_position_size'] != 0:
        a = client.futures_get_all_orders(symbol=symbol)
        present_order_id = a[-1]['clientOrderId']
        print(present_order_id)







    if data['passphrase'] == "4h 497d 846%" :
        # 현재 포지션의 코인 갯수
        # a = client.futures_get_all_orders(symbol=symbol)
        # origQty = a[-1]['origQty']
        # print('현재 포지션의 코인 개수 : ', origQty)
        try:
            # 포지션 정리
            if ((data['strategy']['order_id'] == '1exit') or (data['strategy']['order_id'] == 'Close entry(s) order 1Long') or (data['strategy']['order_id'] == 'Close entry(s) order 1Short')) and (present_order_id == '4h_497d_846p'):

                # order_response = client.futures_create_order(symbol=symbol, side=side, type='STOP_MARKET', stopPrice=stopPrice, closePosition='true')
                # 현재 포지션의 코인 갯수
                a = client.futures_get_all_orders(symbol=symbol)
                origQty = a[-1]['origQty']
                print('현재 포지션의 코인 개수 : ', origQty)
                order_response = client.futures_create_order(symbol=symbol, side=side, type=order_type, quantity=origQty)
                print(f"Close position : {data['strategy']['order_id']} {side} {symbol} STOP_MARKET")

            # 포지션 진입
            # 무 포지션이어서 진입만 하는 경우
            elif (data['strategy']['prev_market_position_size'] == 0) or ((data['strategy']['prev_market_position_size'] != 0) and (present_order_id == '4h_497d_846p')):
                if (present_order_id == '4h_497d_846p'):
                    a = client.futures_get_all_orders(symbol=symbol)
                    origQty = a[-1]['origQty']
                    print('현재 포지션의 코인 개수 : ', origQty)
                    client.futures_create_order(symbol=symbol, side=side, type=order_type, quantity=origQty)

                # 최대 구매 가능 코인 계산
                maxWithdrawAmount = float(client.futures_account()['maxWithdrawAmount']) * 0.99
                leverage = 3
                print("현재 구매 가능한 달러 : ", maxWithdrawAmount)
                quantity = math.floor(((maxWithdrawAmount * leverage) / data['strategy']['order_price']) * 1000) / 1000
                print("구매 가능한 코인 개수 : ", quantity)

                order_response = client.futures_create_order(newClientOrderId='4h_497d_846p', symbol=symbol, side=side, type=order_type, quantity=quantity)
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




    if data['passphrase'] == "30m 871d 40%" :

        try:
            # 포지션 정리
            if (data['strategy']['order_id'] == '2exit') and (present_order_id == '30m_871d_40p'):
                order_response = client.futures_create_order(symbol=symbol, side=side, type='STOP_MARKET',
                                                             stopPrice=1000, closePosition='true')
                print(f"Close position : {data['strategy']['order_id']} {side} {symbol} STOP_MARKET")
            # 포지션 진입
            elif data['strategy']['prev_market_position_size'] == 0:
                present_order_id = data['strategy']['order_id']
                # 최대 구매 가능 코인 계산
                maxWithdrawAmount = float(client.futures_account()['maxWithdrawAmount'])
                leverage = 3
                print("현재 구매 가능한 달러 : ", maxWithdrawAmount)
                quantity = math.floor(((maxWithdrawAmount * leverage) / data['strategy']['order_price']) * 1000) / 1000
                print("구매 가능한 코인 개수 : ", quantity)

                order_response = client.futures_create_order(newClientOrderId='30m_871d_40p', symbol=symbol, side=side, type=order_type,
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
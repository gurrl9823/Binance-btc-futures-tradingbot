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
    print(data['passphrase'])


    # 예외처리
    if (data['passphrase'] != "don't sleep~") and (data['passphrase'] != "4h 497d 846%") and (data['passphrase'] != "30m 871d 40%") :
        print("Nice try, invalid passphrase")
        return {
            "code": "error",
            "message": "Nice try, invalid passphrase"
        }

    # heroku app 활성화 유지
    if data['passphrase'] == "don't sleep~":
        return {
            "message": "don't sleep~"
        }


    # 공통 처리

    symbol = "BTCUSDT"

    side = data['strategy']['order_action'].upper()  # buy, sell

    order_type = "MARKET"

    present_order_id = ''
    if data['strategy']['prev_market_position_size'] != 0:
        a = client.futures_get_all_orders(symbol=symbol)
        present_order_id = a[-1]['clientOrderId']
        print(present_order_id)





    # strategy 1
    if data['passphrase'] == "4h 497d 846%":
        try:
            # 포지션 정리
            if ((data['strategy']['order_id'] == '1exit') or (data['strategy']['order_id'] == 'Close entry(s) order 1Long') or (data['strategy']['order_id'] == 'Close entry(s) order 1Short')) and (present_order_id == '4h_497d_846p'):
                # 현재 포지션의 코인 개수
                position_info = client.futures_position_information()
                for symbolInfo in position_info:
                    if symbolInfo['symbol'] == 'BTCUSDT':
                        quantity = math.fabs(float(symbolInfo['positionAmt']))
                        break
                print('현재 포지션의 코인 개수 : ', quantity)
                order_response = client.futures_create_order(symbol=symbol, side=side,
                                                             type=order_type, quantity=quantity)
                print(f"Close position : {data['strategy']['order_id']} {side} {symbol} STOP_MARKET")

            # 포지션 진입
            elif (data['strategy']['prev_market_position_size'] == 0) or ((data['strategy']['prev_market_position_size'] != 0) and (present_order_id == '4h_497d_846p')):
                # 현재 포지션이 존재하는 경우 == 포지션을 스위치하는 경우 기존 포지션 정리
                if (present_order_id == '4h_497d_846p'):
                    # 현재 포지션의 코인 개수
                    position_info = client.futures_position_information()
                    for symbolInfo in position_info:
                        if symbolInfo['symbol'] == 'BTCUSDT':
                            quantity = math.fabs(float(symbolInfo['positionAmt']))
                            break
                    print('현재 포지션의 코인 개수 : ', quantity)
                    client.futures_create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)

                #포지션 진입
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





    # strategy 2
    if data['passphrase'] == "30m 871d 40%":
        try:
            # 포지션 정리
            if (data['strategy']['order_id'] == '2exit') and (present_order_id == '30m_871d_40p'):
                # 현재 포지션의 코인 개수
                position_info = client.futures_position_information()
                for symbolInfo in position_info:
                    if symbolInfo['symbol'] == 'BTCUSDT':
                        quantity = math.fabs(float(symbolInfo['positionAmt']))
                        break
                print('현재 포지션의 코인 개수 : ', quantity)
                order_response = client.futures_create_order(symbol=symbol, side=side,
                                                             type=order_type, quantity=quantity)
                print(f"Close position : {data['strategy']['order_id']} {side} {symbol} STOP_MARKET")

            # 포지션 진입
            elif data['strategy']['prev_market_position_size'] == 0:
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
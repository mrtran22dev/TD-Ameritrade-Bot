import json
import datetime


def get_rsi(length, json_object, avg_type):
    gain = []
    loss = []

    # find gains and loss after each close and put it into two list
    resp_len = len(json_object)
    for i in range(resp_len):
        if i != resp_len-1:
            x = json_object[i]['close'] - json_object[i + 1]['close']

            if x < 0:
                gain.append(abs(x))
                loss.append(0.0)
                # print('gain:', gain)
            elif x > 0:
                loss.append(x)
                gain.append(0.0)
                # print('loss', loss)
            else:
                loss.append(0.0)
                gain.append(0.0)
            # print(f'prev close: {jsonObject[i]["close"]} | current close: {jsonObject[i + 1]["close"]} | gain: {gain[i]} | loss: {loss[i]}')


########### INVOKE EMA/WILDER AVERAGE FUNCTION -> get_rs() -  TO CALC RS ###########

    rs = []
    ema_gain = get_rs(length, gain, avg_type)
    ema_loss = get_rs(length, loss, avg_type)
    for i in range(len(ema_gain)):                                  # CALCULATE RS
        rs.append(ema_gain[i] / ema_loss[i])


######################  CALC RSI AND PUT IN JSON OBJECT LIST  ######################

    rsi_list = []
    for i in range(len(rs)):
        date_time = datetime.datetime.fromtimestamp(json_object[i + length]["unixDateTime"] * .001)
        close = json_object[i + length]["close"]
        rsi = round(100 - 100 / (1 + rs[i]), 3)
        rsi_list.append({"dateTime": date_time, "close": close, "rsi": rsi})
    return rsi_list


######################### CALC EMA/WILDER AVERAGE #############################

def get_rs(length, gain_loss, avg_type):
    if avg_type.lower() == 'ema':                                   # ema average
        k = 2 / (length + 1)
    elif avg_type.lower() == 'wilder':
        k = 1 / length                                              # wilder average
    else:
        k = 1 / length                                              # else default to wilder avg

    ema_list = []
    summation = 0
    for i in range(length):
        summation = summation + gain_loss[i]
    first_ema = summation / length
    ema_list.append(first_ema)

    previous_ema = first_ema
    for i in range(length, len(gain_loss)):
        price_today = gain_loss[i]
        ema = price_today * k + previous_ema * (1 - k)
        ema_list.append(ema)
        previous_ema = ema

    return ema_list

##################### OTHER CHECKS ######################

    # print('emaGain', emaGain)
    # print('emaLoss', emaLoss)
    # print('gain', gain)
    # print('loss', loss)

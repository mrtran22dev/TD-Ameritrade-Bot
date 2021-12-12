import datetime
from datetime import date


def get_sma(length, json_object):
    if length < len(json_object):
        j = 0
        summation = 0
        sma_list = []
        for start in range(len(json_object)):
            if start <= len(json_object)-length:
                while j < length + start:
                    summation = summation + json_object[j]['close']
                    j += 1
                sma = summation / length
                sma_list.append({"dateTime": json_object[start]["dateTime"], "close": json_object[start]["close"], "sma": sma})
                j = start
                summation = 0
            else:
                break
        return sma_list
    else:
        print('Not enough data points for SMA')


def get_ema(length, json_object):
    k = 2/(length + 1)
    ema_list = []
    summation = 0

    for i in range(length):
        summation = summation + json_object[i]['close']
    first_ema = summation/length
    ema_list.append({"dateTime": json_object[length - 1]["dateTime"], "close": json_object[length - 1]["close"], "ema": first_ema})

    previous_ema = first_ema
    for i in range(length, len(json_object)):
        price_today = json_object[i]['close']
        ema = price_today * k + previous_ema * (1-k)
        ema_list.append({"dateTime": json_object[i]["dateTime"], "close": json_object[i]["close"], "ema": ema})
        previous_ema = ema

    return ema_list

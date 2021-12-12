import datetime
from datetime import date

def getSma(length, jsonObject):
    if (length < len(jsonObject)):
        j = 0
        sum = 0
        smaList = []
        for start in range(len(jsonObject)):
            if start <= len(jsonObject)-length:
                while j < length + start:
                    sum = sum + jsonObject[j]['close']
                    j += 1
                sma = sum / length
                smaList.append(sma)
                j = start
                sum = 0
            else:
                break
        return (smaList)
    else:
        print('Not enough data points for SMA')


def getEma(length, jsonObject):
    k = 2/(length + 1)
    emaList = []
    sum = 0

    for i in range(length):
        sum = sum + jsonObject[i]['close']
    firstEma = sum/length
    emaList.append({"dateTime": jsonObject[length - 1]["dateTime"], "close": jsonObject[length - 1]["close"], "ema": firstEma})

    previousEma = firstEma
    for i in range(length, len(jsonObject)):
        priceToday = jsonObject[i]['close']
        ema = priceToday * k + previousEma * (1-k)
        emaList.append({"dateTime": jsonObject[i]["dateTime"], "close": jsonObject[i]["close"], "ema": ema})
        previousEma = ema

    # CHECK: PRINT EMA LIST
    for i in range(len(emaList)):
        print(f'{emaList[i]["dateTime"]} | {emaList[i]["close"]} | {emaList[i]["ema"]}')
    return emaList

def getRs(length, gainLoss, avgType):
    if avgType.lower() == 'ema':
        k = 2/(length + 1)
    else:
        k = 1/length                                        # wilder average

    emaList = []
    sum = 0
    for i in range(length):
        sum = sum + gainLoss[i]
    firstEma = sum/length
    emaList.append(firstEma)

    previousEma = firstEma
    for i in range(length, len(gainLoss)):
        priceToday = gainLoss[i]
        ema = priceToday * k + previousEma * (1-k)
        emaList.append(ema)
        previousEma = ema
    return emaList
import datetime
import old_indicators1


def getRsi(length, jsonObject, avgType):
    gain = []
    loss = []

    # find gains and loss after each close and put it into two list
    resp_len = len(jsonObject)
    for i in range(resp_len):
        if i != resp_len-1:
            x = jsonObject[i]['close'] - jsonObject[i + 1]['close']

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

######################### EMA/WILDER AVG TO CALC RS #############################

    rs = []
    emaGain = old_indicators1.getRs(length, gain, avgType)
    emaLoss = old_indicators1.getRs(length, loss, avgType)
    for i in range(len(emaGain)):
        rs.append(emaGain[i] / emaLoss[i])                      # RS

######################  CALC RSI AND PUT IN JSON OBJECT LIST  ######################

    rsiList = []
    for i in range(len(rs)):
        dateTime = datetime.datetime.fromtimestamp(jsonObject[i + length]["unixDateTime"]*.001)
        close = jsonObject[i + length]["close"]
        rsi = round(100 - 100 / (1 + rs[i]), 3)
        rsiList.append({"dateTime": dateTime, "close": close, "rsi": rsi})
        print(f'from json > {rsiList[i]["dateTime"]} | {rsiList[i]["close"]} | {rsiList[i]["rsi"]}')
    return rsiList

##################### OTHER CHECKS ######################

    # print('emaGain', emaGain)
    # print('emaLoss', emaLoss)
    # print('gain', gain)
    # print('loss', loss)

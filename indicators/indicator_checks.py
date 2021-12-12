import indicators


# CHECK: PRINT SMA/EMA LIST
def moving_avg(ma_list):
    try:
        if ma_list[0]["sma"] is not None:
            print(f'Calculated SMA indicator data points')
            print(f'======================================================')
        for i in range(len(ma_list)):
            print(f'{ma_list[i]["dateTime"]}  |  CLOSE: {ma_list[i]["close"]}  |  SMA: {ma_list[i]["sma"]}')
        return ma_list
    except KeyError:
        print(f'Calculated EMA indicator data points')
        print(f'======================================================')
        for i in range(len(ma_list)):
            print(f'{ma_list[i]["dateTime"]}  |  CLOSE: {ma_list[i]["close"]}  |  EMA: {ma_list[i]["ema"]}')
        return ma_list


# CHECK: PRINT RSI LIST
def rsi(rsi_list):
    print(f'Calculated RSI indicator data points')
    print(f'======================================================')
    for i in range(len(rsi_list)):
        print(f'{rsi_list[i]["dateTime"]}  |  CLOSE: {rsi_list[i]["close"]}  |  RSI: {rsi_list[i]["rsi"]}')

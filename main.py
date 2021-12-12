import json
import Config
from apis.ApiHelper import ApiHelper
from strategies.Strategy import Strategy
from create_files import create_file
from indicators import indicators_calc, indicator_checks
from indicators import rsi

if __name__ == '__main__':
    print('Hi, Mike Trading Bot started ...\n')
    config = Config.Config('TSLA')
    print(f'TICKER: {config.symbol}')

    # ========================== GET API RESPONSE (RAW STRING) ================================

    apiHelper = ApiHelper(config)
    resp = apiHelper.get_data_pts()

    try:
        # print(resp.text)                                                          # CHECK: print/fetch response + etc
        json_resp = resp.json()                                                     # parse string RESPONSE to json object
        print(f'# of candles/data points: {len(json_resp["candles"])}\n')
    except AttributeError:
        print('error getting actual api response')
        print('proceeding to use dummy data ... \n')
        json_resp = json.loads('{"candles":[]}')

    if len(json_resp["candles"]) == 0:
        print(f'*** there are no data points retrieved for ticker: {config.symbol}')
        print(f'reading from test file: TSLA-10day-5min.json\n')
        with open(f'venv/data/json/TSLA-10day-5min.json',
                  'r') as file:                                                         # read data from json file and create jsonObject
            content = file.read()
        raw_data_json = json.loads(content)
    else:
        create_file.write_resp_to_txt_file(json_resp, f'venv/data/csv/{config.symbol}-10day-5min.txt')      # write response to text/csv file
        create_file.write_resp_to_json_file(json_resp, f'venv/data/json/{config.symbol}-10day-5min.json')   # write response to json file
        with open(f'venv/data/json/{config.symbol}-10day-5min.json', 'r') as file:                          # read data from json file and create jsonObject
            content = file.read()
        raw_data_json = json.loads(content)


    # ====================================== SMA CALC =====================================
    # print(indicators_calc.get_sma(14, raw_data_json))                             # print calculated SMA list
    sma_list = indicators_calc.get_sma(14, raw_data_json)
    # indicator_checks.moving_avg(sma_list)                                         # print SMA list by row


    # ============== RSI CALC + RSI ONLY TRADE STRATEGY (BASELINE/REFERENCE) ==============
    rsi_list = rsi.get_rsi(14, raw_data_json, 'wilder')                             # avg_type = ema/wilder
    baseline = Strategy('rsi_only_baseline', rsi_list, raw_data_json)
    indicator_checks.rsi(rsi_list)
    baseline.trade()


    # ======================= EMA CALC + EMA ONLY TRADE STRATEGY ==========================
    ema_list = indicators_calc.get_ema(14, raw_data_json)
    ema_only = Strategy('ema_only', ema_list, raw_data_json)
    # indicator_checks.moving_avg(ema_list)                                           # print EMA list by row
    # ema_only.trade()


    # ======================= RSI CALC + RSI ONLY TRADE STRATEGY ==========================
    rsi_list = rsi.get_rsi(14, raw_data_json, 'wilder')                             # avg_type = ema/wilder
    rsi_only_last_rsi = Strategy('rsi_only_use_last_rsi', rsi_list, raw_data_json)
    # indicator_checks.rsi(rsi_list)
    # rsi_only_last_rsi.trade()


    # ====================== EMA/RSI CALC + EMA+RSI TRADE STRATEGY ========================
    ema_list = indicators_calc.get_ema(14, raw_data_json)
    rsi_list = rsi.get_rsi(14, raw_data_json, 'wilder')
    ema_and_rsi50 = Strategy('ema_and_rsi50', ema_list, rsi_list, raw_data_json)
    # ema_and_rsi50.trade()


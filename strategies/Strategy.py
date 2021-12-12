from strategies import ema_only_trade, rsi_only_trade, ema_rsi_trade


class Strategy:
    def __init__(self, *args):
        if len(args) == 3:                                   # constructor 1 for 3 args
            self.strategy = args[0]
            self.indicator_values_list = args[1]
            self.raw_data_json = args[2]
            self.account = Account()
        elif len(args) == 4:                                 # constructor 2 for 4 args
            self.strategy = args[0]
            self.indicator_values_list1 = args[1]
            self.indicator_values_list2 = args[2]
            self.raw_data_json = args[3]
            self.account = Account()

    def trade(self):
        if self.strategy == 'ema_only':
            ema_only_trade.ema_only(self.indicator_values_list, self.raw_data_json, self.account)
        elif self.strategy == 'rsi_only_baseline':
            rsi_only_trade.rsi_only_baseline(self.indicator_values_list, self.raw_data_json, self.account)
        elif self.strategy == 'rsi_only_use_last_rsi':
            rsi_only_trade.rsi_only_use_last_rsi(self.indicator_values_list, self.raw_data_json, self.account)
        elif self.strategy == 'ema_and_rsi50':
            ema_rsi_trade.ema_and_rsi50(self.indicator_values_list1, self.indicator_values_list2, self.raw_data_json, self.account)
        else:
            print(f'no strategy found for: {self.strategy}')


class Account:
    def __init__(self):
        self.BALANCE = 3000.00
        self.POSITION_TOTAL = 0.0
        self.SHARES = 0
        self.TRADE_LOG = []
        self.TRADE_LOG.append({'BALANCE': self.BALANCE})
        self.LAST_RSI = 0.0
        self.LAST_EMA = 0.0
        self.LAST_CLOSE = 0.0

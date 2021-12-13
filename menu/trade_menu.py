from indicators import indicator_checks


class Menu:
    def __init__(self, ema_list, rsi_list, s1, s2, s3, s4):
        self.ema_list = ema_list
        self.rsi_list = rsi_list
        self.strategy1 = s1
        self.strategy2 = s2
        self.strategy3 = s3
        self.strategy4 = s4

    def open_menu(self):
        print(f'+-----------------------------------------------+')
        print(f'|               Trading Strategies              |')
        print(f'+-----------------------------------------------+')
        print(f'|   1. Baseline - trade on RSI=50 level         |')
        print(f'|   2. EMA only - trade w/ EMA indicator        |')
        print(f'|   3. RSI only - trade based on last RSI level |')
        print(f'|   4. EMA + RSI - trade w/ EMA + RSI level     |')
        print(f'+-----------------------------------------------+')
        trade = input('|   select a trading strategy (1,2,3,4): ')

        if trade == '1':
            print(f'+-----------------------------------------------+\n')
            indicator_checks.rsi(self.rsi_list)
            self.strategy1.trade()
        elif trade == '2':
            print(f'+-----------------------------------------------+\n')
            indicator_checks.moving_avg(self.ema_list)
            self.strategy2.trade()
        elif trade == '3':
            print(f'+-----------------------------------------------+\n')
            indicator_checks.rsi(self.rsi_list)
            self.strategy3.trade()
        elif trade == '4':
            print(f'+-----------------------------------------------+\n')
            indicator_checks.rsi(self.rsi_list)
            self.strategy4.trade()
        else:
            print(f'|   default trading strategy selected: 1        |')
            print(f'+-----------------------------------------------+\n')
            indicator_checks.rsi(self.rsi_list)
            self.strategy1.trade()

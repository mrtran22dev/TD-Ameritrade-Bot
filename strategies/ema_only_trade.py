from strategies import trade_log
from strategies import trade_actions


def ema_only(ema_list, json_object, account):
    print('\nEMA only trading strategy started. printing real-time txns ...')
    print('==================================================================')

    for i in range(len(ema_list)):
        ema = ema_list[i]['ema']
        close = ema_list[i]['close']

        if account.BALANCE <= 0:
            print('GAME OVER :(')
            break
        elif close > ema and account.BALANCE/close >= 1 and account.SHARES > 0:         #1 HOLD
            print('hold, do nothing')
        elif close <= ema and account.SHARES > 0:                                       #3 SELL
            trade_actions.sell(close, ema, account)
        elif close > ema and account.BALANCE/close >= 1:                                #2 BUY
            trade_actions.buy(close, ema, account)
        else:
            print(f'do nothing: {ema} | bal: {account.BALANCE/close} | shares: {account.SHARES}')
    trade_log.print_trade_log(account)


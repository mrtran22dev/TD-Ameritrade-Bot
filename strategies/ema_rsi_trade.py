from strategies import trade_actions, trade_log


# Set RSI=50
def ema_and_rsi50(ema_list, rsi_list, json_object, account):
    print('\nEMA and RSI=50 trading strategy started. printing real-time txns ...')
    print('======================================================================')
    ema_list.pop(0)

    for i in range(len(ema_list)):
        # print(rsiList[i]['rsi'])
        ema = ema_list[i]['ema']
        rsi = rsi_list[i]['rsi']
        close = ema_list[i]['close']

        if account.BALANCE <= 0:
            print('GAME OVER :(')
            break
        elif rsi > 50 and close > ema and account.BALANCE/close >= 1 and account.SHARES > 0:  # 1 HOLD
            total = account.BALANCE + account.POSITION_TOTAL
            print(f'hold, do nothing -  $: {total} | bal: {account.BALANCE} | pos_tot: {account.POSITION_TOTAL} | '
                  f'shares: {account.SHARES} | rsi: {rsi}')
        elif rsi <= 50 and close <= ema and account.SHARES > 0:                               # 3 SELL
            trade_actions.sell(close, rsi, account)
        elif rsi > 50 and close > ema and account.BALANCE/close >= 1:                         # 2 BUY
            trade_actions.buy(close, rsi, account)
        else:
            total = account.BALANCE + account.POSITION_TOTAL
            print(f'do nothing - $: {total} | bal: {account.BALANCE} | pos_tot: {account.POSITION_TOTAL} | '
                  f'shares: {account.SHARES} | rsi: {rsi}')
    trade_log.print_trade_log(account)

from strategies import trade_log, trade_actions


# *** BASELINE/REFERENCE - Trade using close price above/below RSI=50 only
def rsi_only_baseline(rsi_list, json_object, account):
    print('\nRSI only "baseline" trading strategy started. printing real-time txns ...')
    print('============================================================================')
    for i in range(len(rsi_list)):
        # print(rsiList[i]['rsi'])
        rsi = rsi_list[i]['rsi']
        close = rsi_list[i]['close']

        if account.BALANCE <= 0:
            print('GAME OVER :(')
            break
        elif rsi > 50 and account.BALANCE/close >= 1 and account.SHARES > 0:            # 1 HOLD
            total = account.BALANCE + account.POSITION_TOTAL
            print(f'hold, do nothing -  $: {total} | bal: {account.BALANCE} | pos_tot: {account.POSITION_TOTAL} '
                  f'| shares: {account.SHARES} | rsi: {rsi}')
        elif rsi > 50 and account.BALANCE/close >= 1:                                   # 2 BUY
            trade_actions.buy(close, rsi, account)
        elif rsi <= 50 and account.SHARES > 0:                                          # 3 SELL
            trade_actions.sell(close, rsi, account)
        else:
            total = account.BALANCE + account.POSITION_TOTAL
            print(f'do nothing - $: {total} | bal: {account.BALANCE} | pos_tot: {account.POSITION_TOTAL} '
                  f'| shares: {account.SHARES} | rsi: {rsi}')
    trade_log.print_trade_log(account)


# RSI only trade #2 - use last RSI value
def rsi_only_use_last_rsi(rsi_list, json_object, account):
    print('\nRSI only trading strategy using last RSI started. printing real-time txns ...')
    print('==================================================================================')
    account.LAST_RSI = 0.0

    for i in range(len(rsi_list)):
        # print(rsiList[i]['rsi'])
        rsi = rsi_list[i]['rsi']
        close = rsi_list[i]['close']

        if account.BALANCE <= 0:
            print('GAME OVER :(')
            break
        elif rsi > account.LAST_RSI+8 and account.SHARES > 0:
            print(f'{rsi} | {account.LAST_RSI}')
            trade_actions.sell(close, rsi, account)
        elif rsi > 50 and account.BALANCE / close >= 1 and account.SHARES > 0:  # 1 HOLD
            total = account.BALANCE + account.POSITION_TOTAL
            account.LAST_RSI = rsi
            print(f'hold, do nothing -  $: {total} | bal: {account.BALANCE} | pos_tot: {account.POSITION_TOTAL} '
                  f'| shares: {account.SHARES} | rsi: {rsi}')
        elif rsi >= 65 and account.BALANCE / close >= 1:                        # 2 BUY
            print('do nothing')
        elif 65 > rsi > 50 and account.BALANCE / close >= 1:                    # 2 BUY
            trade_actions.buy(close, rsi, account)
        elif rsi <= 50 and account.SHARES > 0:                                  # 3 SELL
            trade_actions.sell(close, rsi, account)
        else:
            total = account.BALANCE + account.POSITION_TOTAL
            account.LAST_RSI = rsi
            print(f'do nothing - $: {total} | bal: {account.BALANCE} | pos_tot: {account.POSITION_TOTAL} '
                  f'| shares: {account.SHARES} | rsi: {rsi}')
    trade_log.print_trade_log(account)

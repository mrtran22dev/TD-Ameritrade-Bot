
def buy(close, rsi, account):
    print(f'BUY (ACCT BEFORE) - start_bal: {account.BALANCE} | start_pos_tot: {account.POSITION_TOTAL} | start_sh: {account.SHARES} | close: {close} | rsi: {rsi}')
    # if BALANCE >= close:
    buy_shares = int(account.BALANCE/close)                                     # TODO exception for close = $0
    account.SHARES = account.SHARES + buy_shares
    # total_price = SHARES * close
    account.POSITION_TOTAL = round(account.SHARES * close, 2)
    account.BALANCE = round(account.BALANCE - account.POSITION_TOTAL, 2)            #total_price
    account.TRADE_LOG.append({'BUY': -account.POSITION_TOTAL})                      #-total_price})
    total = account.BALANCE + account.POSITION_TOTAL
    account.LAST_RSI = rsi
    print(f'BUY (ACCT AFTER) - $: {total} | end_bal: {account.BALANCE} | end_pos_tot: {account.POSITION_TOTAL} | end_sh: {account.SHARES}')
    return account


def sell(close, rsi, account):
    print(f'SELL (ACCT BEFORE) - start_bal: {account.BALANCE} | start_pos_tot: {account.POSITION_TOTAL} | start_sh: {account.SHARES} | close: {close} | rsi: {rsi}')
    # total_price = SHARES * close
    account.POSITION_TOTAL = round(account.SHARES * close, 2)
    account.SHARES = 0
    account.BALANCE = round(account.BALANCE + account.POSITION_TOTAL, 2)            #total_price
    account.TRADE_LOG.append({'SELL': +account.POSITION_TOTAL})                     #+total_price})
    account.POSITION_TOTAL = 0
    total = account.BALANCE + account.POSITION_TOTAL
    account.LAST_RSI = 0
    print(f'SELL (ACCT AFTER) - $: {total} | end_bal: {account.BALANCE} | end_pos_tot: {account.POSITION_TOTAL} | end_sh: {account.SHARES}')
    return account

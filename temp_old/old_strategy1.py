
# class Strategy:
#     def __init__(self, initial, position):
#         self.initial = 3000.00
#         self.position = 0

# global BALANCE
# global POSITION
BALANCE = 3000.00
POSITION_TOTAL = 0.0
SHARES = 0
TRADE_LOG = []
TRADE_LOG.append({'BALANCE': BALANCE})
LAST_RSI = 0.0
LAST_EMA = 0.0
LAST_CLOSE = 0.0


def rsiOnly(rsiList, jsonObject):
    print('RSI only trade ...')
    global BALANCE, SHARES, POSITION_TOTAL, LAST_RSI
    LAST_RSI = 0.0

    for i in range(len(rsiList)):
        # print(rsiList[i]['rsi'])
        rsi = rsiList[i]['rsi']
        close = rsiList[i]['close']

        if BALANCE <= 0:
            print('GAME OVER :(')
            break
        elif rsi > LAST_RSI+8 and SHARES > 0:
            print(f'{rsi} | {LAST_RSI}')
            sell(close, rsi)
        elif rsi > 50 and BALANCE / close >= 1 and SHARES > 0:  # 1 HOLD
            total = BALANCE + POSITION_TOTAL
            LAST_RSI = rsi
            print(f'hold, do nothing -  $: {total} | bal: {BALANCE} | pos_tot: {POSITION_TOTAL} | sh: {SHARES} | rsi: {rsi}')
        elif rsi >= 65 and BALANCE / close >= 1:                # 2 BUY
            print('do nothing')
        elif 65 > rsi > 50 and BALANCE / close >= 1:            # 2 BUY
            buy(close, rsi)
        elif rsi <= 50 and SHARES > 0:                          # 3 SELL
            sell(close, rsi)
        else:
            total = BALANCE + POSITION_TOTAL
            LAST_RSI = rsi
            print(f'do nothing - $: {total} | bal: {BALANCE} | pos_tot: {POSITION_TOTAL} | sh: {SHARES} | rsi: {rsi}')


        ######################### BASELINE #################################
        # if BALANCE <= 0:
        #     print('GAME OVER :(')
        #     break
        # elif rsi > 50 and BALANCE/close >= 1 and SHARES > 0:            # 1 HOLD
        #     total = BALANCE + POSITION_TOTAL
        #     print(f'hold, do nothing -  $: {total} | bal: {BALANCE} | pos_tot: {POSITION_TOTAL} | sh: {SHARES} | rsi: {rsi}')
        # elif rsi > 50 and BALANCE/close >= 1:                           # 2 BUY
        #     buy(close, rsi)
        # elif rsi <= 50 and SHARES > 0:                                  # 3 SELL
        #     sell(close, rsi)
        # else:
        #     total = BALANCE + POSITION_TOTAL
        #     print(f'do nothing - $: {total} | bal: {BALANCE} | pos_tot: {POSITION_TOTAL} | sh: {SHARES} | rsi: {rsi}')
        #####################################################################

    print_trade_log()


def emaOnly(emaList, jsonObject):
    print('EMA only trade ...')
    global BALANCE, SHARES, POSITION_TOTAL, LAST_EMA

    for i in range(len(emaList)):
        # print(rsiList[i]['rsi'])
        ema = emaList[i]['ema']
        close = emaList[i]['close']

        if BALANCE <= 0:
            print('GAME OVER :(')
            break
        elif close > ema and BALANCE/close >= 1 and SHARES > 0:                 #1 HOLD
            print('hold, do nothing')
        elif close <= ema and SHARES > 0:                                       #3 SELL
            sell(close, ema)
        elif close > ema and BALANCE/close >= 1:                                #2 BUY
            buy(close, ema)
        else:
            print(f'do nothing: {ema} | {BALANCE/close} | {SHARES}')
    print_trade_log()

def emaAndRsi(emaList, rsiList, jsonObject):
    print('EMA and RSI trade ...')
    global BALANCE, SHARES, POSITION_TOTAL, LAST_RSI, LAST_EMA, LAST_CLOSE
    emaList.pop(0)

    for i in range(len(emaList)):
        # print(rsiList[i]['rsi'])
        ema = emaList[i]['ema']
        rsi = rsiList[i]['rsi']
        close = emaList[i]['close']

        ######################## BASELINE #################################
        if BALANCE <= 0:
            print('GAME OVER :(')
            break
        elif rsi > 50 and close > ema and BALANCE/close >= 1 and SHARES > 0:  # 1 HOLD
            total = BALANCE + POSITION_TOTAL
            print(f'hold, do nothing -  $: {total} | bal: {BALANCE} | pos_tot: {POSITION_TOTAL} | sh: {SHARES} | rsi: {rsi}')
        elif rsi <= 50 and close <= ema and SHARES > 0:                         # 3 SELL
            sell(close, rsi)
            pass
        elif rsi > 50 and close > ema and BALANCE/close >= 1:                   # 2 BUY
            buy(close, rsi)
        else:
            total = BALANCE + POSITION_TOTAL
            print(f'do nothing - $: {total} | bal: {BALANCE} | pos_tot: {POSITION_TOTAL} | sh: {SHARES} | rsi: {rsi}')
        ####################################################################
    print_trade_log()


######################## TRADE ACTIONS #################################
def buy(close, rsi):
    global BALANCE, SHARES, POSITION_TOTAL, LAST_RSI
    print(f'BUY (ACCT BEFORE) - start_bal: {BALANCE} | start_pos_tot: {POSITION_TOTAL} | start_sh: {SHARES} | close: {close} | rsi: {rsi}')

    # if BALANCE >= close:
    buy_shares = int(BALANCE/close)                          # exception for close = $0
    SHARES = SHARES + buy_shares
    # total_price = SHARES * close
    POSITION_TOTAL = round(SHARES * close, 2)
    BALANCE = round(BALANCE - POSITION_TOTAL, 2)              #total_price
    TRADE_LOG.append({'BUY': -POSITION_TOTAL})      #-total_price})
    total = BALANCE + POSITION_TOTAL
    LAST_RSI = rsi
    print(f'BUY (ACCT AFTER) - $: {total} | end_bal: {BALANCE} | end_pos_tot: {POSITION_TOTAL} | end_sh: {SHARES}')


def sell(close, rsi):
    global BALANCE, SHARES, POSITION_TOTAL, LAST_RSI
    print(f'SELL (ACCT BEFORE) - start_bal: {BALANCE} | start_pos_tot: {POSITION_TOTAL} | start_sh: {SHARES} | close: {close} | rsi: {rsi}')
    # total_price = SHARES * close
    POSITION_TOTAL = round(SHARES * close, 2)
    SHARES = 0
    BALANCE = round(BALANCE + POSITION_TOTAL, 2)                #total_price
    TRADE_LOG.append({'SELL': +POSITION_TOTAL})                 #+total_price})
    POSITION_TOTAL = 0
    total = BALANCE + POSITION_TOTAL
    LAST_RSI = 0
    print(f'SELL (ACCT AFTER) - $: {total} | end_bal: {BALANCE} | end_pos_tot: {POSITION_TOTAL} | end_sh: {SHARES}')


def print_trade_log():
    global BALANCE, SHARES, POSITION_TOTAL, TRADE_LOG
    total = 0.0
    # for i in TRADE_LOG:
    #     print(i)
    #     print(f'$: {i["TRADE"]}')
    #     total = total + float(i['TRADE'])
    # print(f'return: {total}')

    print(f'start: {TRADE_LOG[0]["BALANCE"]}')
    initial = TRADE_LOG[0]["BALANCE"]
    total = TRADE_LOG[0]["BALANCE"]

    i = 1
    while i < len(TRADE_LOG):
        try:
            print(TRADE_LOG[i]['BUY'])
            total = total + TRADE_LOG[i]['BUY']
        except:
            print(TRADE_LOG[i]['SELL'])
            total = total + TRADE_LOG[i]['SELL']
        i += 1

    print('==========================================')
    print(f'BALANCE: ${total}')
    if SHARES > 0:
        share_total = TRADE_LOG[len(TRADE_LOG)-1]["BUY"]*(-1)
        print(f'SHARES: {SHARES} -> ${share_total}')
    else:
        print(f'SHARES: {SHARES}')

    if (SHARES > 0):
        total = total - TRADE_LOG[len(TRADE_LOG)-1]['BUY']
        print(f'strategy1 > RETURN: ${total} ({((total - initial) * 100/initial):.2f}%)')
    else:
        print(f'strategy1 > RETURN: ${total} ({((total - initial) * 100/initial):.2f}%)')


    # for i in TRADE_LOG:
    # # print(f'return: {total}')
    #     # print(i.get('BALANCE'))
    #     try:
    #         print(f'ff {i["TRADE"]}')
    #     except:
    #         print(i['SELL'])
    #     # except Exception as e:
    #     #     print(float(TRADE_LOG[i]['SELL']))

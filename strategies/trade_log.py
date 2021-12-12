import logging

# logging.basicConfig(level=logging.INFO)                 # Set level to DEBUG to print log on console
# logger = logging.getLogger('TradeLogger')

def print_trade_log(account):
    logging.basicConfig(level=logging.INFO)                 # Set level to DEBUG to print log on console
    logger = logging.getLogger('TradeLogger')
    total = 0.0

    # for i in TRADE_LOG:
    #     print(i)
    #     print(f'$: {i["TRADE"]}')
    #     total = total + float(i['TRADE'])
    # print(f'return: {total}')

    initial = account.TRADE_LOG[0]["BALANCE"]
    total = account.TRADE_LOG[0]["BALANCE"]

    i = 1
    while i < len(account.TRADE_LOG):
        try:
            logger.debug(f'balance (buy): {account.TRADE_LOG[i]["BUY"]}')
            total = total + account.TRADE_LOG[i]['BUY']
        except:
            logger.debug(f'balance (sell): {account.TRADE_LOG[i]["SELL"]}')
            total = total + account.TRADE_LOG[i]['SELL']
        i += 1

    print('==========================================')
    print(f'START BALANCE: {account.TRADE_LOG[0]["BALANCE"]}')
    print(f'END BALANCE: ${total}')
    if account.SHARES > 0:
        share_total = account.TRADE_LOG[len(account.TRADE_LOG)-1]["BUY"]*(-1)
        print(f'SHARES HODL: {account.SHARES} -> ${share_total}')
    else:
        print(f'SHARES HODL: {account.SHARES}')

    if account.SHARES > 0:
        total = total - account.TRADE_LOG[len(account.TRADE_LOG)-1]['BUY']
        print(f'RETURN: ${total} ({((total - initial) * 100/initial):.2f}%)')
    else:
        print(f'RETURN: ${total} ({((total - initial) * 100/initial):.2f}%)')


    # for i in TRADE_LOG:
    # # print(f'return: {total}')
    #     # print(i.get('BALANCE'))
    #     try:
    #         print(f'ff {i["TRADE"]}')
    #     except:
    #         print(i['SELL'])
    #     # except Exception as e:
    #     #     print(float(TRADE_LOG[i]['SELL']))

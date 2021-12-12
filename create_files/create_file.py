import datetime


# WRITE TO JSON FILE
def write_resp_to_json_file(json_resp, filename):
    with open(filename, 'w') as write_file:
        write_file.write('[\n')

    with open(filename, 'a') as write_file:                             # loop and write closing prices to file
        # for x in jsonResp['candles']:
        for i in range(len(json_resp['candles'])):
            unixdatetime = json_resp['candles'][i]['datetime']
            date_time = datetime.datetime.fromtimestamp(unixdatetime*.001)
            close = json_resp['candles'][i]['close']
            if i != len(json_resp['candles'])-1:
                write_file.write(
                    f'  {{"unixDateTime": {unixdatetime}, "dateTime": "{date_time}", "close": {close}}},\n')
            else:
                write_file.write(
                    f'  {{"unixDateTime": {unixdatetime}, "dateTime": "{date_time}", "close": {close}}}\n')

    with open(filename, 'a') as write_file:
        write_file.write(']')


# WRITE TO TXT/CSV FILE
def write_resp_to_txt_file(json_resp, filename):
    with open(filename, 'a') as write_file:                               # loop and write closing prices to file
        for x in json_resp['candles']:
            unixdatetime = x['datetime']
            unix_string = str(unixdatetime)[:-3]
            date_time = datetime.datetime.fromtimestamp(int(unix_string))
            write_file.write(str(x['datetime']) + ', ' + str(date_time) + ', ' + str(x['close']) + '\n')

    # for x in jsonResp['candles']:                                       # loop and print timedate + closing prices
    #     unixdatetime = x['datetime']
    #     unix_string = str(unixdatetime)[:-3]
    #     dateTime = datetime.datetime.fromtimestamp(int(unix_string))
    #     print(x['datetime'], ', ', dateTime, ', ', x['close'])
import json


class Config:
    def __init__(self, symbol):                                     # constructor
        config_path = 'config.json'
        with open(config_path, 'r') as file:                        # read data from json file and create jsonObject
            content = file.read()
        self.config = json.loads(content)

        self.symbol = symbol
        self.endpoint = self.config['endpoint']['prod']
        self.access_token = self.config['accessToken']
        self.api_key = self.config['apiKey']
        self.token_type = 'Bearer'
        self.market_data = '/v1/marketdata/' + symbol + '/pricehistory'
        self.payload = {'Authorization': 'Bearer ' + self.access_token}
        self.query_string = '?apikey=' + self.api_key + '&periodType=day&period=10&frequencyType=minute&frequency=5&needExtendedHoursData=true'
        self.full_path = self.endpoint + self.market_data + self.query_string

import requests


class ApiHelper:
    def __init__(self, config):
        self.full_endpoint_path = config.full_path
        self.payload = config.payload

    def get_data_pts(self):
        resp = requests.get(self.full_endpoint_path,
                            data=self.payload)            # or this works too `resp = requests.get(fullPath, data=json.dumps(payload))`
        print(f'status code: {resp.status_code}')
        if resp.status_code == 200:
            return resp

    # TODO - add buy/sell trade, account balance, etc api requests

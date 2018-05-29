import sys
import http.client
import urllib
import json
import hashlib
import hmac
import time

class IncoreXAPI:
    def __init__(self, API_KEY, API_SECRET, API_URL = 'api.incorex.com', API_VERSION = 'v1'):
        self.API_URL = API_URL
        self.API_VERSION = API_VERSION
        self.API_KEY = API_KEY
        self.API_SECRET = bytes(API_SECRET, encoding='utf-8')

    def sha512(self, data):
        H = hmac.new(key = self.API_SECRET, digestmod = hashlib.sha512)
        H.update(data.encode('utf-8'))
        return H.hexdigest()

    def api_query(self, api_method, params = {}):
        params['nonce'] = int(round(time.time() * 1000))
        params =  urllib.parse.urlencode(params)

        sign = self.sha512(params)
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "Key": self.API_KEY,
            "Sign": sign
        }
        conn = http.client.HTTPSConnection(self.API_URL)
        conn.request("POST", "/" + self.API_VERSION + "/" + api_method, params, headers)
        response = conn.getresponse().read()

        conn.close()

        try:
            obj = json.loads(response.decode('utf-8'))
            if 'error' in obj and obj['error']:
                print(obj['error'])
                raise sys.exit()
            return obj
        except json.decoder.JSONDecodeError:
            print('Error while parsing response:', response)
            raise sys.exit()

# Example
# YOUR_API_KEY - TODO replace with your api key from profile page
# YOUR_API_SECRET - TODO replace with your api secret from profile page
IncoreXAPI_instance = IncoreXAPI('YOUR_API_KEY', 'YOUR_API_SECRET')
result = IncoreXAPI_instance.api_query('user_info')

# result = IncoreXAPI_instance.api_query('trades', {'pair': 'BTC_USD'})
# result = IncoreXAPI_instance.api_query('order_book', {'pair': 'BTC_USD', 'limit': 100})
# result = IncoreXAPI_instance.api_query('ticker')
# result = IncoreXAPI_instance.api_query('pair_settings')
# result = IncoreXAPI_instance.api_query('currency')

# result = IncoreXAPI_instance.api_query('user_info')
# result = IncoreXAPI_instance.api_query('order_create', {'pair': 'BTC_USD', 'quantity': 2, 'price': 100, 'type': 'sell'})
# result = IncoreXAPI_instance.api_query('order_cancel', {'order_id': 123456})
# result = IncoreXAPI_instance.api_query('user_open_orders')
# result = IncoreXAPI_instance.api_query('user_trades', {'pair': 'BTC_USD', 'limit': 100, 'offset': 0})
# result = IncoreXAPI_instance.api_query('user_cancelled_orders')
# result = IncoreXAPI_instance.api_query('order_trades', {'order_id': 123456})
# result = IncoreXAPI_instance.api_query('required_amount', {'pair': 'BTC_USD', 'quantity': 2})
# result = IncoreXAPI_instance.api_query('deposit_address')
# result = IncoreXAPI_instance.api_query('withdraw_get_txid', {'task_id': 123456})
# result = IncoreXAPI_instance.api_query('create_xvoucher', {'currency': 'USD', 'amount': 100.00})
# result = IncoreXAPI_instance.api_query('activate_xvoucher', {'code': '123456'})
# result = IncoreXAPI_instance.api_query('wallet_history', {'date': 1525122000})
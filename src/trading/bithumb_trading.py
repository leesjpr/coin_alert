import sys
from xcoin_api_client import *
#from single_instance import SingleInstance

CURRENCY = 'KRW'

class Bithumb:
    def __init__(self, key_file_path):
        self._secret_key = None
        self._connect_key = None
        self.valid_keys = False
        try:
            self._read_api_keys(key_file_path)
        except Exception, e:
            print str(e)


    def _read_api_keys(self, path):
        fp = open(path, 'r')
        keys = {}

        for ln in fp.readlines():
            ln.replace('\n', '')
            key, value = ln.split(':')
            keys[key] = value.strip()

        self._connect_key = keys['connect_key']
        self._secret_key = keys['secret_key']

        self.valid_keys = True


    #def _call_api(self, api_type, api_uri, coin_type):
    def call_api(self, api_type, api_uri, coin_type):
        rg_params = {}
        rg_params['order_currency'] = coin_type
        rg_params['payment_currency'] = CURRENCY

        api = XCoinAPI(self._connect_key, self._secret_key)
        result = api.xcoinApiCall(api_uri, rg_params)

        print result


    def wallet_status(self):
        pass


    def trading_buy(self):
        pass


    def trading_self(self):
        pass




if __name__ == "__main__":
#    pass
    bithumb = Bithumb('../../cfg/api_keys')

    if bithumb.valid_keys:
        print "success"

    bithumb.call_api('trade', '/info/balance', 'xmr')


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
    def call_api(self, api_type, api_uri, coin_type, rg_params):
        success = False
        result = None
        try:
            api = XCoinAPI(self._connect_key, self._secret_key)
            result = api.xcoinApiCall(api_uri, rg_params)
            status = result['status']

            if status == 0000:
                success = True
            elif status == 5100:
                result = "Bad Request"
            elif status == 5200:
                result = "Not Member"
            elif status == 5300:
                result = "Invalid Apikey"
            elif status == 5302:
                result = "Method Not Allowed"
            elif status == 5400:
                result = "Database Fail"
            elif status == 5500:
                result = "Invalid Parameter"
            elif status == 5600:
                result = "CUSTEM NOTICE"
            elif status == 5900:
                result = "Unknown Error"

        except Exception, e:
            print 'failed call api', str(e)

        return (success, result)


    def information_account_status(self, coin_type):
        rg_params = {}
        rg_params['currency'] = coin_type

        flag, result = call_api(rg_params)
        if flag:
            status_code = result['status']
            if status_code == 0000:
                created = result['created']
                account_id = result['account_id']
                trade_fee = result['trade_fee']
                balance = result['balance']

        else:
            pass


    def informatin_wallet_status(self, coin_type):
        rg_params = {}
        rg_params['currency'] = coin_type

        call_api(rg_params)


    def informatin_user_transaction(self, coin_type):
        rg_params = {}
        rg_params['currency'] = coin_type
        rg_params['offset'] = None
        rg_params['count'] = None
        rg_params['seasrchGb'] = None

        call_api(rg_params)


    def trading_buy(self, coin_type):
        rg_params = {}
        rg_params['currency'] = None
        rg_params['units'] = None

        call_api(rg_params)


    def trading_sell(self, coin_type):
        rg_params = {}
        rg_params['currency'] = None
        rg_params['units'] = None

        call_api(rg_params)



if __name__ == "__main__":
#    pass
    bithumb = Bithumb('../../cfg/api_keys')

    bithumb.call_api('trade', '/info/account', 'BCH')


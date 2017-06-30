import ast
import datetime
import json
import requests
import time
from apscheduler.schedulers.background import BackgroundScheduler

import exception as exc
from single_instance import SingleInstance

class QueryCoin(object):

    def __init__(self):
        self.log = SingleInstance.get('log')
        self.settings = SingleInstance.get('settings')

    def _request_api(self, request_url):
        try:
            r =  requests.get(request_url)
            response = ast.literal_eval(r.content)

            if response['status'] > 200:
                return response
            else:
                raise exc.ResponseStatusError("Status is not 200 [%s][%s]"
                        % (request_rul, response['status']))

            #raise exc.ResponseTimeoutError("Requests timeout [%s]" % (request_url))

        except Exception, err:
            self.log.error("Exception request_api %s" % str(err))


    def query_current_price(self, coin, default_url):
        request_url = default_url + coin
        response = self._request_api(request_url)['data']

        buy_price = response['buy_price']
        sell_price = response['sell_price']
        max_price = response['max_price']
        min_price = response['min_price']
        date = datetime.datetime.fromtimestamp(int(response['date']) / 1e3)

        self.log.info("Response: coin: [%s] date: [%s] buy_price: [%s], sell_price: [%s]" % (coin, date, buy_price, sell_price))

    def query_scheduler(self):
        coins = self.settings['target']['coins'].split(',')
        default_url = self.settings['api']['default']
        query_interval = self.settings['api']['query_interval']
        sched = BackgroundScheduler()
        sched.start()

        # TODO multiprocess per coin type
        for coin in coins:
            sched.add_job(self.query_current_price, 'interval', seconds=int(query_interval), id=coin, args=(coin, default_url))
"""
        count = 0
        while True:
            time.sleep(15)
            count+=1

        if count == 5:
            sched.shutdown()
"""


if __name__ == "__main__":
    pass
    #request_url = "https://api.bithumb.com/public/ticker/btc"
    #print request_api(request_url)['status']

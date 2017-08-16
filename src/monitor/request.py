import ast
import datetime
from datetime import timedelta
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

            if response['status'] == "0000":
                return response
            else:
                raise exc.ResponseStatusError("Status is not 0000 [%s][%s]"
                        % (request_url, response['status']))

        except Exception, err:
            self.log.error("Exception request_api %s" % str(err))
            return {}


    def query_all_price(self, default_url):
        request_url = default_url + "ALL"
        response = self._request_api(request_url)['data']
        date = datetime.datetime.fromtimestamp(int(response['date']) / 1e3)
        try:
            if len(response) > 0:
                del response['date']
                for coin, detail  in response.iteritems():
                    buy_price = detail['buy_price']
                    sell_price = detail['sell_price']
                    max_price = detail['max_price']
                    min_price = detail['min_price']
                    self.log.info("Response: coin:[%7s] date:[%10s] buy_price:[%10s] sell_price:[%10s]"\
                            % (coin, date, buy_price, sell_price))

                    self.insert_price_into_redis(coin, date, detail)
            else:
                raise exception()
        except Exception, err:
            self.log.error("Exception parsing --> %s" % str(err))


    def insert_price_into_redis(self, coin, date, detail):
        redis = SingleInstance.get('redis')
        day = date.strftime("%Y%m%d")
        hour = date.strftime("%H")
        time = date.strftime("%M%S")


        value = {}
        key = "monitor:%s:%s:%s" % (coin, day, hour)
        value[time] = json.dumps(detail)

        try:
            redis.hmset(key, value)

        except Exception, err:
            print str(err)

        alert_target = self.settings['target']['coins'].split(",")
        notibot = SingleInstance.get('notibot')

        if coin.lower() in alert_target:
            notibot.default_notification(date, coin, detail)


    def query_scheduler(self):
        coins = self.settings['target']['coins'].split(',')
        default_url = self.settings['api']['default']
        query_interval = int(self.settings['api']['query_interval'])
        sched = BackgroundScheduler()

        # TODO multiprocess per coin type
        sched.add_job(self.query_all_price, 'interval', \
                seconds=query_interval, \
                id="monitoring", args=[default_url])

        sched.start()
        try:
            while True:
                time.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            scheduler.shutdown()


if __name__ == "__main__":
    pass
    #request_url = "https://api.bithumb.com/public/ticker/btc"
    #print request_api(request_url)['status']

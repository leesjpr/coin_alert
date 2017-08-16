import telegram
from single_instance import SingleInstance

class NotificationBot(object):
    def __init__(self):
        self.settings = SingleInstance.get('settings')
        self.log = SingleInstance.get('log')
        self._token = self.settings['telegram']['token']
        self._chat_id = self.settings['telegram']['chat_id']
        self.initialize_bot()
        self.tlg_bot = None
        self.redis = SingleInstance.get('redis')


    def initialize_bot(self):
        try:
            self.tlg_bot = telegram.Bot(token=self._token)
            self.log.info("Bot creation success!! token: %s" % (self._token))
        except Exception , err:
            self.log.error("Bot creation failure!! --> %s" % str(err))


    def send_message(self, msg):
        self.tlg_bot.sendMessage(chat_id = self.chat_id, text=msg)


    def default_notification(self, date, coin, price_info):
        noti_targets = self.settings['target']['coins']
        interval = self.settings['alert']['default']

        time_bucket = {}

        time_bucket['day'] = date.strftime("%Y%m%d")
        time_bucket['hour'] = date.strftime("%H")
        time_bucket['minut'] = date.strftime("%M")
        time_bucket['second'] = date

        msg = "[Default price notification]\n \
                [[coin]]\n\
                10%s: 10%s\n\
                10%s: 10%s\n\
                10%s: 10%s\n\
                10%s: 10%s\n"\
                % ("max price", price_info["max_price"], "min price", \
                    price_info["min_price"], "buy price", \
                    price_info["buy_price"],"sell price", \
                        price_info["sell_price"])

        alert_time = None

        if interval == 'day':
            if alert_time != time_bucket['day']:
                self.send_message(msg)
                alert_time = time_bucket['day']
        elif interval == 'hour':
            if alert_time != time_bucket['hour']:
                self.send_message(msg)
                alert_time = time_bucket['hour']
        elif interval == 'minut':
            if alert_time != time_bucket['minut']:
                self.send_message(msg)
                alert_time = time_bucket['minut']
        elif interval == 'second':
            if alert_time != time_bucket['second']:
                self.send_message(msg)
                alert_time = time_bucket['second']







if __name__ == "__main__":
    pass








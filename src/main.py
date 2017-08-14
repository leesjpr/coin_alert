import ConfigParser
import getopt
import io
import sys

import common.exception as exc
import common.log_util
from common.request import QueryCoin
from common.single_instance import SingleInstance



def usage():
    print 'python %s -s ~/setting.ini' % sys.argv[0]
    sys.exit(2)


def arg_read():
    if len(sys.argv) < 2:
        print sys.argv
        usage()

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hs', ['help', 'setting='])
        if len(opts) < 1:
            raise getopt.GetoptError("arg is empty")
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)

    try:
        setting_file = None
        for o, a in opts:
            if o in ['-h', 'help']:
                usage()
            elif o in ['-s', '--setting']:
                setting_file = args
            else:
                raise ArgumentParsingError("unhandled option")

        return setting_file
    except ArgumentParsingError, err:
        log_util.logging.error(str(e))



def read_setting(file_path):
    settings = dict()
    try:
        config = ConfigParser.ConfigParser()
        config.read(file_path)

        sections = config.sections()

        if len(sections) != 0:
            for section in sections:
                settings[section] = {}
                options = config.options(section)
                for option in options:
                    settings[section][option] = config.get(section, option)

        coins = settings['target']['coins'].split(',')
        for coin in coins:
            coin_options = config.options(coin)
            for coin_option in coin_options:
                settings[coin][coin_option] = config.get(coin, coin_option)

        SingleInstance.set('settings', settings)
    except exc.ConfigParsingError, err:
        log_util.logging.error(str(err))


if __name__ == '__main__':
    settings_file = arg_read()
    read_setting(settings_file)
    settings = SingleInstance.get('settings')
    log_conf = settings['logging']['config']

    try:
        base_log = log_util.BaseLogger(log_conf)
    except Exception, err:
        log_util.logging.error(':%s' % str(err))
        sys.exit(1)

    SingleInstance.set('log', base_log)
    query = QueryCoin()
    query.query_scheduler()

import ConfigParser
import getopt
import io
import sys

import log_util
import exception as exc
from single_instance import SingleInstance


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
        log_conf = config.get('logging', 'config')
        targets = config.get('target', 'coins').replace(' ', '').split(',')

        settings['logging'] = log_conf

        for target in targets:
            options = config.options(target)
            settings[target] = dict()
            for option in options:
                settings[target][option] = config.get(target, option)

        SingleInstance.set('settings', settings)
    except exc.configParsingError, err:
        log_util.logging.error(str(err))





if __name__ == '__main__':
    settings_file = arg_read()
    read_setting(settings_file)
    settings = SingleInstance.get('settings')
    log_conf = settings['logging']

    try:
        base_log = log_util.BaseLogger(log_conf)
    except Exception, err:
        log_util.logging.error(':%s' % str(err))
        sys.exit(1)

    SingleInstance.set('log', base_log)

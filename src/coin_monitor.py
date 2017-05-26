import ConfigParser
import getopt
import io
import sys


def usage():
    print 'python %s -s ~/setting.ini' % sys.argv[0]
    sys.exit(2)


def arg_read():
    if len(sys.argv) < 2:
        print sys.argv
        usage()

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hs', ['help', 'setting='])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)

    setting_file = None
    for o, a in opts:
        if o in ['-h', 'help']:
            usage()
        elif o in ['-s', '--setting']:
            setting_file = args
        else:
            assert False, "unhandled option"

    return setting_file


def read_setting(file_path):
    config = ConfigParser.ConfigParser()
    config.read(file_path)

    targets = config.get('target', 'coin').replace(' ', '').split(',')

    set_dic = {}

    for target in targets:
        set_dic[target]









if __name__ == '__main__':
    setting_file = arg_read()
    read_setting(setting_file)

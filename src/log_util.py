import logging
import logging.config
import sys
import os

class BaseLogger(object):
    def __init__(self, config_file):
        self.config_file = config_file
        self.logger = self.get_logger()
        self.info('::: Initialized the base logger :::')
        self.file_nm = None
        self.line_no = None
        self.func_nm = None


    def get_logger(self):
        try:
            if self.config_file is not None and \
                self.config_file != '' and \
                os.path.isfile(self.config_file) == True:
                logging.config.fileConfig(self.config_file)
                logger = logging.getLogger()

                return logger
            else:
                raise Exception ('Base logger configuration file path is invalid')
        except Exception, err:
            print 'Failed generation base logger : %s' % str(err)
            sys.exit(1)


    def find_caller(self):
        self.file_nm, self.line_no, self.func_nm = self.logger.findCaller()

        if len(self.file_nm.split('/')) > 2:
            self.file_nm = self.file_nm.split('/')[-1]

    def debug(self, log_msg):
        self.find_caller()
        self.logger.debug('[%s(%s)]:%s' % (self.file_nm, self.line_no, log_msg))


    def info(self, log_msg):
        self.find_caller()
        self.logger.info('[%s(%s)]:%s' % (self.file_nm, self.line_no, log_msg))


    def warn(self, log_msg):
        self.find_caller()
        self.logger.warn('[%s(%s)]:%s' % (self.file_nm, self.line_no, log_msg))


    def error(self, log_msg):
        self.find_caller()
        self.logger.error('[%s(%s)]:%s' % (self.file_nm, self.line_no, log_msg))


    def critical(self, log_msg):
        self.find_caller()
        self.logger.critical('[%s(%s)]:%s' % (self.file_nm, self.line_no, log_msg))


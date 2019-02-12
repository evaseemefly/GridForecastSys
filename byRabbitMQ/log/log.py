import logging
import logging.config
from os import path
# logging.config.fileConfig('logging_conf.ini')
# 需要制定配置文件的具体路径，否则会报KeyError: 'formatters'的错误
log_file_path=path.join(path.dirname(path.abspath(__file__)),'logging_conf.ini')


# logger=logging.getLogger('simpleExample')

class MyLog:
    # 日志配置（读取指定的配置文件）
    # __log_config=logging.config.fileConfig(log_file_path,disable_existing_loggers=False)
    __log_config = logging.config.fileConfig(log_file_path)
    # logger
    __file_info_log=logging.getLogger('myInfo')
    __file_warn_log=logging.getLogger('myError')
    @staticmethod
    def addInfo(msg):
        '''
            静态方法，info写入
        :param msg:
        :return:
        '''
        MyLog.__file_info_log.info(msg)

    @staticmethod
    def addWarn(msg):
        '''
            静态方法，warn写入
        :param msg:
        :return:
        '''
        MyLog.__file_warn_log.warn(msg)
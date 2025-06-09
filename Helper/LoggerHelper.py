
import logging
from settings import DeBug
from logging.handlers import RotatingFileHandler,TimedRotatingFileHandler
from .ConfigHelper import Configer
from typing import cast

#  当前项目的日志系统,比较方便管理项目本身的输出日志信息
class Logger():
    def __init__(self):
        self.configer = Configer()
        self.log_path = cast(str,self.configer.get_config_value('Log_Path'))
        self.logger = logging.getLogger()
        # 确保只配置一次避免多个 日志 初始化配置
        if not self.logger.hasHandlers():
            handlers = [ # 多个 handlers 表示多个 log 处理器， 这会对同一个相同日志信息，打印两次，不是特别好
                # RotatingFileHandler(self.log_path, maxBytes=1e6),  # 1MB,单个日志最大为 1MB，并且按天保存，最多5份，也就是最近 5天的
                TimedRotatingFileHandler(
                    self.log_path,
                    when='midnight',       # 每天午夜时分轮转
                    interval=1,            # 每 1 天轮转
                    backupCount=5          # 保留 5 个备份日志文件，也就是最近五天的
                )
            ]
            if DeBug:
                handlers.append(logging.StreamHandler() )  # type: ignore # 终端日志输出
            logging.basicConfig(
                # filename=self.log_path,  # 日志的文件 ， 同时文件如果不存在就自动创建
                level=logging.DEBUG,    # 记录所有级别的日志信息，也就是下面所有的方法的打印结果，比如 error, bebug
                format='%(asctime)s - %(levelname)s - %(message)s', # 单行日志的记录格式
                handlers=handlers
            )
    
    # 自定义方法，提供 debug, info, warning, error, critical 等常用日志输出
    def debug(self, message):
        self.logger.debug(message)
    
    def info(self, message):
        self.logger.info(message)
    
    def warning(self, message):
        self.logger.warning(message)
    
    def error(self, message):
        self.logger.error(message)
    
    def critical(self, message):
        self.logger.critical(message)

     
    
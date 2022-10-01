import logging
import logging.config
import os
import yaml
from commons.path import LOG_PATH, CONFIG_PATH


class MyLog:
    def __init__(self, file_name, config_path=CONFIG_PATH, handel_name='server', level=logging.INFO):
        """
        自定义日志对象
        :param config_path: 自定义日志配置文件
        :param file_name: 自定义日志的日志名称
        :param handel_name: 自定义的handler的名称， 如果自己定义了一个handler在config文件里面的话，可以修改此值，否则不要修改
        :param level: 自定义的日志等级
        """

        self.config_path = config_path
        self.file_name = LOG_PATH + file_name
        self.handler = handel_name
        self.level = level

    def setup_logging(self, env_key='LOG_CFG'):
        """
        | **@author:** Prathyush SP
        | Logging Setup
        """
        value = os.getenv(env_key, None)
        if value:
            self.config_path = value
        if os.path.exists(self.config_path):
            with open(self.config_path, 'rt', encoding="utf-8") as f:
                try:
                    config = yaml.safe_load(f.read())
                    logconfig = config['logConfig']
                    logconfig['handlers']['file']['filename'] = self.file_name
                    logging.config.dictConfig(logconfig)
                except Exception as e:
                    print(e)
                    print('Error in Logging Configuration. Using default configs')
                    logging.basicConfig(level=self.level)
        else:
            logging.basicConfig(level=self.level)
            print('Failed to load configuration file. Using default configs')

    def get_loger(self):
        self.setup_logging()
        loger = logging.getLogger(self.handler)
        return loger


if __name__ == '__main__':
    logger = MyLog('../config.yaml','tjk.log').get_loger()
    logger.info("testssss")


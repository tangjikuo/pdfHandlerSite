# 相关相关路径
import os

# 项目的根路径
ROOT = os.path.abspath(os.path.join(os.path.relpath(__file__), '../..'))

# 配置文件路径
CONFIG_PATH = os.path.join(ROOT, 'config.yaml')

# 日志文件件
LOG_PATH = os.path.join(ROOT, 'logs')

if __name__ == '__main__':
    print(ROOT)
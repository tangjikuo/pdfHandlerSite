import yaml
from yaml import safe_load

from dao.database import SessionLocal
from commons.path import CONFIG_PATH


def get_config_dict(path, env):
    with open(path, 'rb') as f:
        conf = safe_load(f.read())
        f.close()
    return conf[env]


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_config(route: str):
    """获取config.yaml中的参数 通过以下方式获取：
    example: get_config('env.mysql.host') 获取mysql的host"""
    with open(CONFIG_PATH, 'rt') as f:
        config = yaml.safe_load(f.read())
        try:
            route_list = route.split('.')
            res_dict = config
            if route_list:
                for r in route_list:
                    res_dict = res_dict[r]
            else:
                raise ValueError("传入的路径格式不正确")
        except Exception as e:
            print(e)
            return {}
        return res_dict


if __name__ == '__main__':
    pass
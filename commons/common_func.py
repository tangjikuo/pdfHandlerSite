from yaml import safe_load

from dao.database import SessionLocal


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


if __name__ == '__main__':
    pass

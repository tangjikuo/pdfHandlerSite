from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:123456@10.0.0.5:3306/testdb'

engine = create_engine(SQLALCHEMY_DATABASE_URL, encoding='utf8', echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

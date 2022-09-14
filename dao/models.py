from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey, BLOB
from database import Base, engine
from datetime import datetime


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(length=32), index=True)
    password = Column(String(length=125))
    status = Column(Integer, default=0, comment='用户状态：0正常 1删除')
    money = Column(Float, comment='用户账户的余额')
    create_time = Column(DateTime, default=datetime.now())
    update_time = Column(DateTime)


class Files(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    file_name = Column(String(125), comment="修改后的文件名称")
    tax_code = Column(String(25), nullable=False, default='915001080542963889', comment='公司税号')
    invoice_code = Column(String(20), nullable=False, comment='发票代码')
    invoice_number = Column(String(10), nullable=False, comment='发票号码')
    invoice_date = Column(String(10), nullable=False, comment='发票日期')
    check_code = Column(String(6), nullable=False, comment='校验码后六位')
    invoice_money = Column(Float, nullable=False, comment='发票金额')
    user_id = Column(Integer, ForeignKey('user.id'), comment='用户id')
    create_time = Column(DateTime, default=datetime.now())
    update_time = Column(DateTime)
    file_content = Column(BLOB, comment='生成的文件')


Base.metadata.create_all(bind=engine)

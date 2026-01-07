from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float
from sqlalchemy.orm import declarative_base


db = create_engine('sqlite:///banco.db')

Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String(100), nullable=False)
    email = Column('email', String, nullable=False, unique=True)
    password = Column('password', String, nullable=False)
    phone_number = Column('phone_number', String, nullable=False)
    account_balance = Column('account_balance', Float, default=0.0)
    account_holder = Column('account_holder', Boolean, default=True)
    admin_account = Column('admin', Boolean, default=False)

    def __init__(self, name, email, password, phone_number, account_balance, account_holder=True, admin_account=False):
        self.name = name
        self.email = email
        self.password = password
        self.phone_number = phone_number
        self.account_balance = account_balance
        self.account_holder = account_holder
        self.admin_account = admin_account
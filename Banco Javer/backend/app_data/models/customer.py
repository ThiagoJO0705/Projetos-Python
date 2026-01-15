from sqlalchemy import Column, Integer, String, Boolean, Float, Numeric
from sqlalchemy.orm import relationship
from app.database import Base
from decimal import Decimal

class Customer(Base):
    __tablename__ = "customers"

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String, nullable=False)
    email = Column('email', String, nullable=False, unique=True)
    password = Column('password', String, nullable=False)
    phone_number = Column('phone_number', String, nullable=False, unique=True)
    cpf = Column('cpf',String, nullable=False, unique=True)
    account_balance = Column('account_balance', Numeric(precision=10, scale=2), default=0.0)
    is_account_holder = Column('is_account_holder', Boolean, default=True)
    is_active = Column('is_active', Boolean, default=True)
    is_admin = Column('is_admin', Boolean, default=False)
    transactions = relationship("Transaction", back_populates="customer", foreign_keys="[Transaction.customer_id]")

    def __init__(self, name, email, password, phone_number, cpf, account_balance=0.0, is_account_holder=True, is_active=True, is_admin=False):
        self.name = name
        self.email = email
        self.password = password
        self.phone_number = phone_number
        self.cpf = cpf
        self.account_balance = round(float(account_balance or 0), 2)
        self.is_account_holder = is_account_holder
        self.is_active = is_active
        self.is_admin = is_admin
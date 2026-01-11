from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy.orm import relationship
from app.database import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    phone_number = Column(String, nullable=False, unique=True)
    cpf = Column(String, nullable=False, unique=True)
    account_balance = Column(Float, default=0.0)
    is_account_holder = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    transactions = relationship("Transaction", back_populates="customer", foreign_keys="[Transaction.customer_id]")

    @property
    def score(self):
        if self.account_balance > 0:
            return round(self.account_balance * 0.1, 2)
        return 0.0


    def __init__(self, name, email, password, phone_number, cpf, account_balance=0.0, is_account_holder=True, is_active=True, is_admin=False):
        self.name = name
        self.email = email
        self.password = password
        self.phone_number = phone_number
        self.cpf = cpf
        self.account_balance = account_balance
        self.is_account_holder = is_account_holder
        self.is_active = is_active
        self.is_admin = is_admin
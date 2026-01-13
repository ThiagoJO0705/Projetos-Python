from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.dbconfig import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    phone_number = Column(String, nullable=False, unique=True)
    transactions = relationship('Transaction', back_populates='owner')

    def __init__(self, name, email, password, phone_number):
        self.name = name
        self.email = email
        self.password = password
        self.phone_number = phone_number
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Enum
from app.schemas.enums import TransactionType
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    asset_id = Column(Integer, ForeignKey('assets.id'), nullable=False)
    quantity = Column(Numeric(precision=10, scale=2), nullable=False)
    price = Column(Numeric(precision=10, scale=2), nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    owner = relationship('User', back_populates='transactions')
    asset = relationship('Asset')

    def __init__(self, user_id, asset_id, quantity, price, type, timestamp):
        self.user_id = user_id
        self.asset_id = asset_id
        self.quantity = quantity
        self.price = price
        self.type = type
        self.timestamp = timestamp
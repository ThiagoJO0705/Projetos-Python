from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from app.schemas.enums import TransactionType, TransactionDirection

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    customer_id = Column('customer_id', Integer, ForeignKey("customers.id"), nullable=False)
    type = Column('type', Enum(TransactionType), nullable=False)
    direction = Column('direction',Enum(TransactionDirection), nullable=False)
    amount = Column('amount', Float, nullable=False)
    related_customer_id = Column('related_customer_id', Integer, ForeignKey("customers.id"), nullable=True)
    description = Column('description', String(255), nullable=True)
    created_at = Column('created_at', DateTime, server_default=func.current_timestamp(), nullable=False)
    customer = relationship("Customer", back_populates="transactions", foreign_keys=[customer_id])
    related_customer = relationship("Customer", foreign_keys=[related_customer_id])

    def __init__(self, customer_id, type, amount, direction, related_customer_id = None, description = None):
        self.customer_id = customer_id
        self.type = type
        self.amount = amount 
        self.direction = direction
        self.related_customer_id = related_customer_id
        self.description = description
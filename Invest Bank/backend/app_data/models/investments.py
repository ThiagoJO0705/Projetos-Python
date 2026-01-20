import uuid
from sqlalchemy import Column, Numeric, Uuid, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app_data.app.dbconfig import Base
from datetime import datetime

class Investment(Base):
    __tablename__ = "investments"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    customer_id = Column(Uuid, ForeignKey("customers.id"), nullable=False)
    asset_id = Column(Uuid, ForeignKey("assets.id"), nullable=False)
    quantity = Column(Numeric(precision=16, scale=8), nullable=False)
    purchase_price = Column(Numeric(precision=10, scale=2), nullable=False)
    application_date = Column(DateTime, nullable=False, server_default=func.now())
    is_active = Column(Boolean, default=True)
    customer = relationship("Customer", back_populates="investments")
    asset = relationship("Asset", back_populates="investments")

    def __init__(self, customer_id, asset_id, quantity, purchase_price, is_active=True):
        self.customer_id = customer_id
        self.asset_id = asset_id
        self.quantity = quantity
        self.purchase_price = purchase_price
        self.is_active = is_active
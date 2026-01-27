import uuid
from sqlalchemy import Column, String, Numeric, Uuid, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app_data.app.dbconfig import Base
from app_data.schemas.enums import InvestmentType

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    ticker = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    type = Column(Enum(InvestmentType), nullable=False)
    current_price = Column(Numeric(precision=10, scale=2), default=0.0)
    currency = Column(String, default='BRL')
    last_updated = Column(DateTime, nullable=False, server_default=func.now())
    investments = relationship("Investment", back_populates="asset")

    def __init__(self, ticker, name, type, current_price=0.0, currency='BRL'):
        self.ticker = ticker
        self.name = name
        self.type = type
        self.current_price = current_price
        self.currency = currency
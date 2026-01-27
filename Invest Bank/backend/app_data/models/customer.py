import uuid
from sqlalchemy import Column, Integer, String, Boolean, Numeric, Uuid, DateTime, Enum
from app_data.app.dbconfig import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app_data.schemas.enums import InvestorProfile

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    phone_number = Column(String, nullable=False, unique=True)
    cpf = Column(String, nullable=False, unique=True)
    investor_profile = Column(Enum(InvestorProfile), nullable=False)
    total_assets = Column(Numeric(precision=10, scale=2), default=0.0)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    is_active = Column(Boolean, default=True)
    investments = relationship("Investment", back_populates="customer", cascade="all, delete-orphan")

    def __init__(self, name, email, password, phone_number, cpf, investor_profile, total_assets=0.0, is_active=True):
        self.name = name
        self.email = email
        self.password = password
        self.phone_number = phone_number
        self.cpf = cpf
        self.investor_profile = investor_profile
        self.total_assets = total_assets
        self.is_active = is_active 
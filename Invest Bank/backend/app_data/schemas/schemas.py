from pydantic import BaseModel, EmailStr
from datetime import datetime
from decimal import Decimal
from .enums import InvestorProfile, InvestmentType
from typing import Optional
import uuid


class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    phone_number: str
    cpf: str
    is_active: bool = True
    is_admin: bool = False
    investor_profile: InvestorProfile = InvestorProfile.UNDEFINED

    class Config:
        from_attributes = True

class CustomerCreate(CustomerBase):
    password: str  
    total_assets: Decimal = Decimal('0.00')  
    account_balance: Decimal = Decimal('0.00')

    class Config:
        from_attributes = True

class CustomerResponse(CustomerBase):
    id: uuid.UUID
    total_assets: Decimal

    class Config:
        from_attributes = True

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    investor_profile: Optional[InvestorProfile] = None
    total_assets: Optional[Decimal] = None
    is_active: Optional[bool] = None

    class Config:
        from_attributes = True

class CustomerAuthResponse(CustomerResponse):
    password: str
    
    class Config:
        from_attributes = True

class AssetBase(BaseModel):
    ticker: str
    name: str
    type: InvestmentType
    current_price: Decimal

    class Config:
        from_attributes = True

class AssetResponse(AssetBase):
    id: uuid.UUID
    last_updated: datetime

    class Config:
        from_attributes = True

class AssetUpdate(BaseModel):
    ticker: Optional[str] = None
    name: Optional[str] = None
    type: Optional[InvestmentType] = None

    class Config:
        from_attributes = True

class InvestmentBase(BaseModel):
    customer_id: uuid.UUID
    asset_id: uuid.UUID
    quantity: Decimal
    purchase_price: Decimal
    is_active: bool = True

    class Config:
        from_attributes = True

class InvestmentResponse(InvestmentBase):
    id: uuid.UUID
    application_date: datetime
    asset: Optional[AssetResponse] = None
    customer: Optional[CustomerResponse] = None

    class Config:
        from_attributes = True

class InvestmentUpdate(BaseModel):
    quantity: Optional[Decimal] = None
    purchase_price: Optional[Decimal] = None
    is_active: Optional[bool] = None

    class Config:
        from_attributes = True
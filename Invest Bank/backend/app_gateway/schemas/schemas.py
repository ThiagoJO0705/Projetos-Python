import uuid
from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal
from typing import Optional
from app_data.schemas.enums import InvestorProfile, InvestmentType

class CustomerUpdate(BaseModel):
    investor_profile: Optional[InvestorProfile] = None

    class Config:
        from_attributes = True

class AssetResponse(BaseModel):
    id: uuid.UUID
    ticker: str
    name: str
    type: InvestmentType
    current_price: Decimal
    last_updated: datetime
    currency: str

    class Config:
        from_attributes = True

class InvestmentCreate(BaseModel):
    ticker: str = Field(..., example="PETR4.SA")
    quantity: Decimal = Field(..., gt=0)
    purchase_price: Optional[Decimal] = None 
    purchase_date: Optional[str] = Field(None, example="2023-05-15")

    class Config:
        from_attributes = True

class InvestmentUpdate(BaseModel):
    quantity: Optional[Decimal] = None
    is_active: Optional[bool] = None

    class Config:
        from_attributes = True

class InvestmentResponse(BaseModel):
    id: uuid.UUID
    customer_id: uuid.UUID
    asset_id: uuid.UUID
    quantity: Decimal
    purchase_price: Decimal
    application_date: datetime
    is_active: bool
    current_value_usd: Decimal
    current_value_brl: Decimal
    asset: Optional[AssetResponse] = None

    class Config:
        from_attributes = True
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from .enums import AssetType, TransactionType
from datetime import datetime


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone_number: str

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone_number: str

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True

class AssetSchema(BaseModel):
    name: str
    ticker: str
    type: AssetType

    class Config:
        from_attributes = True

class SearchResponse(BaseModel):
    ticker: str
    long_name: Optional[str]
    short_name: str
    stock_exchange: str
    type: AssetType

    class Config:
        from_attributes = True

class AssetPrice(BaseModel):
    ticker: str
    price: float
    currency: str

    class Config:
        from_attributes = True

class TickerSchema(BaseModel):
    ticker: str

    class Config:
        from_attributes = True
        
class TransactionCreate(BaseModel):
    ticker: str = Field(..., example="PETR4.SA")
    quantity: float = Field(..., gt=0)
    price: float = Field(..., gt=0)
    type: TransactionType
    timestamp: Optional[datetime] = None

class TransactionResponse(BaseModel):
    id: int
    ticker: str
    quantity: float
    price: float
    type: TransactionType
    timestamp: datetime

    class Config:
        from_attributes = True

class AssetPerformance(BaseModel):
    ticker: str
    quantity: float
    average_price: float
    current_price: float
    total_invested: float
    current_value: float
    profit_loss: float
    profit_loss_pct: float

    class Config:
        from_attributes = True

class ProfileDashboard(BaseModel):
    user_email: str
    total_transactions: int
    total_invested: float 
    current_balance: float 
    overall_profit_loss: float 
    status: str 
    assets: List[AssetPerformance]

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone_number: Optional[str] = None

    class Config:
        from_attributes = True
from pydantic import BaseModel, EmailStr
from typing import Optional
from .enums import AssetType

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
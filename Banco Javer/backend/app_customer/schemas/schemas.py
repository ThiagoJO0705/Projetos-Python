from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.schemas.enums import TransactionType
from decimal import Decimal

class CustomerCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone_number: str
    cpf: str


    class Config:
        from_attributes = True

class CustomerResponse(BaseModel):
    id: int
    name: str
    email: str
    phone_number: str
    cpf: str
    account_balance: Decimal
    score: Decimal
    is_account_holder: bool
    is_active: bool
    is_admin: bool

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    cpf: Optional[str] = None
    is_account_holder: Optional[bool] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None

    class Config:
        from_attributes = True


class PixSending(BaseModel):
    pix_key: str
    pix_amount: Decimal

    class Config:
        from_attributes = True


class TransactionSchema(BaseModel):
    id: int
    amount: Decimal
    type: str
    direction: str
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class TransactionResponse(BaseModel):
    message: str
    new_balance: Decimal
    new_score: Decimal
    extract: TransactionSchema

    class Config:
        from_attributes = True


class PaymentRequest(BaseModel):
    amount: Decimal
    method: TransactionType
    description: str

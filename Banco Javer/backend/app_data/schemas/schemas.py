from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from .enums import TransactionDirection, TransactionType

class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    phone_number: str
    cpf: str
    is_account_holder: bool = True
    is_active: bool = True
    is_admin: bool = False

class CustomerCreate(CustomerBase):
    password: str  
    account_balance: Decimal = Decimal('0.00')

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    cpf: Optional[str] = None
    is_account_holder: Optional[bool] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None

class CustomerResponse(CustomerBase):
    id: int
    account_balance: Decimal
    

class TransactionCreate(BaseModel):
    customer_id: int
    type: TransactionType
    direction: TransactionDirection
    amount: Decimal
    related_customer_id: Optional[int] = None
    description: Optional[str] = None


class TransactionResponse(BaseModel):
    id: int
    customer_id: int
    type: TransactionType
    direction: TransactionDirection
    amount: Decimal
    related_customer_id: Optional[int]
    description: Optional[str]
    created_at: datetime


from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

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
    account_balance: float
    score: float
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
    pix_amount: float

    class Config:
        from_attributes = True


class TransactionResponse(BaseModel):
    id: int
    amount: float
    type: str
    direction: str
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class PixResponse(BaseModel):
    message: str
    new_balance: float
    new_score: float
    extract: TransactionResponse # Aqui usamos o schema de transação que você já tem

    class Config:
        from_attributes = True
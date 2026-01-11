from pydantic import BaseModel, EmailStr
from typing import Optional

class CustomerCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone_number: str
    cpf: str
    account_balance: float = 0.0

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
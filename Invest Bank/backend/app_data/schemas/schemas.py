from pydantic import BaseModel, EmailStr
from decimal import Decimal
from .enums import InvestorProfile
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
    account_balance: Decimal
    total_assets: Decimal
    class Config:
        from_attributes = True
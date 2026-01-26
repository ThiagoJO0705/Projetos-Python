from pydantic import BaseModel, EmailStr
from typing import Optional
from app_data.schemas.enums import InvestorProfile

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    investor_profile: Optional[InvestorProfile] = None

    class Config:
        from_attributes = True
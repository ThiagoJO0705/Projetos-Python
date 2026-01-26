from pydantic import BaseModel, EmailStr
from typing import Optional
from app_data.schemas.enums import InvestorProfile

class CustomerUpdate(BaseModel):
    investor_profile: Optional[InvestorProfile] = None

    class Config:
        from_attributes = True
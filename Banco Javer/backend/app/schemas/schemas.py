from pydantic import BaseModel
from typing import Optional, List

class CustomerSchema(BaseModel):
    name: str
    email: str
    password: str
    phone_number: str
    account_balance: float
    is_account_holder: Optional[bool]
    is_admin: Optional[bool]

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True
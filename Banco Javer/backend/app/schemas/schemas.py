from pydantic import BaseModel
from pydantic import BaseModel, EmailStr

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
    is_account_holder: bool
    is_admin: bool

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True
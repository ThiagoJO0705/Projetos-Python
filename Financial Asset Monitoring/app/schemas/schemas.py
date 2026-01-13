from pydantic import BaseModel, EmailStr

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